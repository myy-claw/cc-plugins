#!/usr/bin/env python3
"""
飞书 CLI 工具 - 文档 & 多维表格操作
基于 larksuite/openclaw-lark 官方插件的 API 模式

用法:
  python3 feishu.py <command> [options]

环境变量（可选，覆盖默认凭据）:
  FEISHU_APP_ID                  飞书应用 App ID
  FEISHU_APP_SECRET              飞书应用 App Secret

Auth:
  login                          OAuth 登录（用个人账号操作飞书）
  logout                         退出登录（回到应用身份模式）
  whoami                         查看当前身份

Document:
  create_doc <title> [folder]    创建文档
  get_doc <document_id>          获取文档内容
  add_blocks <doc_id> <json> [block_id]  向文档追加内容块
  insert_image <doc_id> <path>   向文档插入本地图片

Bitable:
  create_bitable <name> [folder] 创建多维表格
  get_bitable <app_token>        获取多维表格信息
  create_table <app_token> <name> [fields_json]  创建数据表
  list_tables <app_token>        列出数据表
  list_fields <app_token> <table_id>             列出字段
  create_field <app_token> <table_id> <name> <type> [property_json]  创建字段
  list_records <app_token> <table_id> [filter_json] [page_size]      查询记录
  create_record <app_token> <table_id> <fields_json>                 创建记录
  batch_create_records <app_token> <table_id> <records_json>         批量创建记录
  update_record <app_token> <table_id> <record_id> <fields_json>    更新记录
  delete_record <app_token> <table_id> <record_id>                  删除记录

Drive:
  list_files [folder_token] [page_size]  列出云空间文件
  delete_file <file_token> <type>        删除文件（type: docx/bitable/sheet/file）

Wiki:
  list_wiki_spaces               列出知识库
  create_wiki_space <name> [desc]  创建知识库
  list_wiki_nodes <space_id> [parent_node_token]  列出节点
  create_wiki_node <space_id> <title> [parent] [type]  创建文档节点

Debug:
  token                          获取当前 access_token
"""

import sys
import os
import json
import time
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import requests

# ---------------------------------------------------------------------------
# Config — 加载 .env 文件，环境变量优先
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")

if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                if not os.environ.get(_key.strip()):
                    os.environ[_key.strip()] = _val.strip()

APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
SHARED_FOLDER = os.environ.get("FEISHU_SHARED_FOLDER", "")

# 环境变量检查 — 缺少凭证时立即报错，避免运行到一半才失败
_missing = []
if not APP_ID:
    _missing.append("FEISHU_APP_ID")
if not APP_SECRET:
    _missing.append("FEISHU_APP_SECRET")
if _missing:
    print(json.dumps({
        "error": f"缺少必要的环境变量: {', '.join(_missing)}",
        "hint": "请通过以下任一方式配置：\n"
                f"方式一：在 {ENV_FILE} 中设置\n"
                "  FEISHU_APP_ID=cli_xxxxxxxx\n"
                "  FEISHU_APP_SECRET=xxxxxxxx\n"
                "方式二：export 环境变量\n"
                "  export FEISHU_APP_ID=cli_xxxxxxxx\n"
                "  export FEISHU_APP_SECRET=xxxxxxxx\n"
                "App ID 和 App Secret 可在 https://open.feishu.cn/app 后台的应用凭证页面找到。",
    }, ensure_ascii=False, indent=2))
    sys.exit(1)

BASE_URL = "https://open.feishu.cn/open-apis"
REDIRECT_URI = "http://localhost:9876/callback"
TOKEN_FILE = os.path.join(SCRIPT_DIR, ".feishu_user_token.json")

# ---------------------------------------------------------------------------
# OAuth - 用户身份登录
# ---------------------------------------------------------------------------
_auth_code = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        _auth_code = params.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ 授权成功！请回到终端继续操作。可以关闭此页面。".encode("utf-8"))

    def log_message(self, format, *args):
        pass  # 静默日志


def cmd_login():
    """OAuth 登录，获取 user_access_token"""
    global _auth_code
    _auth_code = None

    # 启动本地回调服务器
    server = HTTPServer(("localhost", 9876), OAuthCallbackHandler)
    thread = Thread(target=server.handle_request, daemon=True)
    thread.start()

    # 打开浏览器授权
    auth_url = (
        f"https://open.feishu.cn/open-apis/authen/v1/authorize"
        f"?app_id={APP_ID}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&scope=bitable:app%20docx:document%20drive:drive%20wiki:wiki"
    )
    print(f"正在打开浏览器进行飞书授权...")
    print(f"如果浏览器没有自动打开，请手动访问：\n{auth_url}\n")
    webbrowser.open(auth_url)

    # 等待回调
    thread.join(timeout=120)
    server.server_close()

    if not _auth_code:
        print(json.dumps({"error": "授权超时或失败"}, ensure_ascii=False))
        sys.exit(1)

    # 用 code 换 user_access_token
    # 先获取 app_access_token
    app_resp = requests.post(f"{BASE_URL}/auth/v3/app_access_token/internal", json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    })
    app_token = app_resp.json().get("app_access_token")

    resp = requests.post(f"{BASE_URL}/authen/v1/oidc/access_token", json={
        "grant_type": "authorization_code",
        "code": _auth_code,
    }, headers={
        "Authorization": f"Bearer {app_token}",
        "Content-Type": "application/json",
    })
    data = resp.json()
    if data.get("code") != 0:
        print(json.dumps({"error": data.get("msg"), "code": data.get("code")}, ensure_ascii=False))
        sys.exit(1)

    token_data = data["data"]
    token_info = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "expire": time.time() + token_data.get("expires_in", 7200) - 60,
        "refresh_expire": time.time() + token_data.get("refresh_expires_in", 2592000) - 60,
        "name": token_data.get("name", ""),
        "en_name": token_data.get("en_name", ""),
        "open_id": token_data.get("open_id", ""),
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_info, f, ensure_ascii=False, indent=2)

    out({"message": "登录成功", "user": token_info["name"] or token_info["en_name"], "open_id": token_info["open_id"]})


def cmd_logout():
    """退出登录"""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    out({"message": "已退出登录，切换回应用身份模式"})


def cmd_whoami():
    """查看当前身份"""
    token_info = _load_user_token()
    if token_info:
        out({"mode": "user", "name": token_info.get("name"), "open_id": token_info.get("open_id")})
    else:
        out({"mode": "tenant", "app_id": APP_ID})


# ---------------------------------------------------------------------------
# Token 管理 - 优先用户身份，回退应用身份
# ---------------------------------------------------------------------------
_tenant_cache = {"token": None, "expire": 0}


def _load_user_token():
    """加载并刷新用户 token"""
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        info = json.load(f)

    # token 未过期
    if time.time() < info.get("expire", 0):
        return info

    # token 过期但 refresh_token 未过期，刷新
    if time.time() < info.get("refresh_expire", 0):
        app_resp = requests.post(f"{BASE_URL}/auth/v3/app_access_token/internal", json={
            "app_id": APP_ID,
            "app_secret": APP_SECRET,
        })
        app_token = app_resp.json().get("app_access_token")

        resp = requests.post(f"{BASE_URL}/authen/v1/oidc/refresh_access_token", json={
            "grant_type": "refresh_token",
            "refresh_token": info["refresh_token"],
        }, headers={
            "Authorization": f"Bearer {app_token}",
            "Content-Type": "application/json",
        })
        data = resp.json()
        if data.get("code") == 0:
            td = data["data"]
            info["access_token"] = td["access_token"]
            info["refresh_token"] = td["refresh_token"]
            info["expire"] = time.time() + td.get("expires_in", 7200) - 60
            info["refresh_expire"] = time.time() + td.get("refresh_expires_in", 2592000) - 60
            with open(TOKEN_FILE, "w") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            return info

    # 全部过期，删除文件
    os.remove(TOKEN_FILE)
    return None


def get_token():
    """获取 access_token：优先 user，回退 tenant"""
    user_info = _load_user_token()
    if user_info:
        return user_info["access_token"]

    # 回退到 tenant_access_token
    now = time.time()
    if _tenant_cache["token"] and now < _tenant_cache["expire"]:
        return _tenant_cache["token"]

    resp = requests.post(f"{BASE_URL}/auth/v3/tenant_access_token/internal", json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    })
    data = resp.json()
    if data.get("code") != 0:
        print(json.dumps({"error": data.get("msg"), "code": data.get("code")}, ensure_ascii=False))
        sys.exit(1)

    _tenant_cache["token"] = data["tenant_access_token"]
    _tenant_cache["expire"] = now + data.get("expire", 7200) - 60
    return _tenant_cache["token"]


def headers():
    return {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}


def api(method, path, **kwargs):
    """统一 API 调用"""
    url = f"{BASE_URL}/{path}"
    resp = requests.request(method, url, headers=headers(), **kwargs)
    data = resp.json()
    if data.get("code") != 0:
        print(json.dumps({"error": data.get("msg"), "code": data.get("code"), "url": path}, ensure_ascii=False, indent=2))
        sys.exit(1)
    return data.get("data", {})


def out(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Document commands
# ---------------------------------------------------------------------------
def cmd_create_doc(title, folder_token=None):
    body = {"title": title}
    folder = folder_token or SHARED_FOLDER
    if not folder:
        print(json.dumps({
            "error": "未指定目标文件夹，且 FEISHU_SHARED_FOLDER 环境变量为空",
            "hint": f"请在 {ENV_FILE} 中设置 FEISHU_SHARED_FOLDER=<folder_token>，"
                    "或在命令中传入 folder_token 参数。",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    body["folder_token"] = folder
    data = api("POST", "docx/v1/documents", json=body)
    doc = data.get("document", {})
    out({
        "document_id": doc.get("document_id"),
        "title": doc.get("title"),
        "url": f"https://feishu.cn/docx/{doc.get('document_id')}",
        "message": "文档创建成功",
    })


def cmd_get_doc(document_id):
    data = api("GET", f"docx/v1/documents/{document_id}/raw_content", params={"lang": 0})
    out({"content": data.get("content"), "message": "获取成功"})


def cmd_add_blocks(document_id, children_json, block_id=None):
    """向文档追加内容块。block_id 默认等于 document_id（文档根块）"""
    if block_id is None:
        block_id = document_id
    children = json.loads(children_json)
    data = api("POST", f"docx/v1/documents/{document_id}/blocks/{block_id}/children",
               json={"children": children})
    out({
        "children": data.get("children", []),
        "document_id": document_id,
        "message": "内容块添加成功",
    })


# ---------------------------------------------------------------------------
# Bitable commands
# ---------------------------------------------------------------------------
def cmd_create_bitable(name, folder_token=None):
    body = {"name": name}
    folder = folder_token or SHARED_FOLDER
    if not folder:
        print(json.dumps({
            "error": "未指定目标文件夹，且 FEISHU_SHARED_FOLDER 环境变量为空",
            "hint": f"请在 {ENV_FILE} 中设置 FEISHU_SHARED_FOLDER=<folder_token>，"
                    "或在命令中传入 folder_token 参数。",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    body["folder_token"] = folder
    data = api("POST", "bitable/v1/apps", json=body)
    app = data.get("app", {})
    out({
        "app_token": app.get("app_token"),
        "name": app.get("name"),
        "url": app.get("url", f"https://feishu.cn/base/{app.get('app_token')}"),
        "message": "多维表格创建成功",
    })


def cmd_get_bitable(app_token):
    data = api("GET", f"bitable/v1/apps/{app_token}")
    out({"app": data.get("app")})


def cmd_create_table(app_token, table_name, fields_json=None):
    table = {"name": table_name}
    if fields_json:
        table["fields"] = json.loads(fields_json)
    data = api("POST", f"bitable/v1/apps/{app_token}/tables", json={"table": table})
    out({"table_id": data.get("table_id"), "message": "数据表创建成功"})


def cmd_list_tables(app_token):
    data = api("GET", f"bitable/v1/apps/{app_token}/tables")
    out({"tables": data.get("items", []), "total": data.get("total")})


def cmd_list_fields(app_token, table_id):
    data = api("GET", f"bitable/v1/apps/{app_token}/tables/{table_id}/fields")
    out({"fields": data.get("items", []), "total": data.get("total")})


def cmd_create_field(app_token, table_id, field_name, field_type, property_json=None):
    body = {"field_name": field_name, "type": int(field_type)}
    if property_json and int(field_type) not in (7, 15):
        body["property"] = json.loads(property_json)
    data = api("POST", f"bitable/v1/apps/{app_token}/tables/{table_id}/fields", json=body)
    out({"field": data.get("field"), "message": "字段创建成功"})


def cmd_list_records(app_token, table_id, filter_json=None, page_size=None):
    body = {}
    if filter_json:
        body["filter"] = json.loads(filter_json)
    params = {}
    if page_size:
        params["page_size"] = int(page_size)
    data = api("POST", f"bitable/v1/apps/{app_token}/tables/{table_id}/records/search",
               json=body, params=params)
    out({
        "records": data.get("items", []),
        "total": data.get("total"),
        "has_more": data.get("has_more"),
    })


def cmd_create_record(app_token, table_id, fields_json):
    fields = json.loads(fields_json)
    data = api("POST", f"bitable/v1/apps/{app_token}/tables/{table_id}/records",
               json={"fields": fields})
    out({"record": data.get("record"), "message": "记录创建成功"})


def cmd_batch_create_records(app_token, table_id, records_json):
    records = json.loads(records_json)
    data = api("POST", f"bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create",
               json={"records": records})
    out({
        "records": data.get("records", []),
        "total": len(data.get("records", [])),
        "message": "批量创建成功",
    })


def cmd_update_record(app_token, table_id, record_id, fields_json):
    fields = json.loads(fields_json)
    data = api("PUT", f"bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}",
               json={"fields": fields})
    out({"record": data.get("record"), "message": "记录更新成功"})


def cmd_delete_record(app_token, table_id, record_id):
    api("DELETE", f"bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}")
    out({"message": "记录删除成功"})


# ---------------------------------------------------------------------------
# Media upload
# ---------------------------------------------------------------------------
def cmd_insert_image(document_id, file_path):
    """向文档插入图片（三步：创建空图片块 → 上传图片 → 绑定素材）"""
    import mimetypes

    # Step 1: 创建空图片块
    data1 = api("POST", f"docx/v1/documents/{document_id}/blocks/{document_id}/children",
                json={"children": [{"block_type": 27, "image": {}}]})
    block_id = data1["children"][0]["block_id"]

    # Step 2: 上传图片到该图片块
    fname = os.path.basename(file_path)
    mime = mimetypes.guess_type(file_path)[0] or "image/png"
    size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/drive/v1/medias/upload_all",
            headers={"Authorization": f"Bearer {get_token()}"},
            files={
                "file_name": (None, fname),
                "parent_type": (None, "docx_image"),
                "parent_node": (None, block_id),
                "size": (None, str(size)),
                "file": (fname, f, mime),
            },
        )
    data2 = resp.json()
    if data2.get("code") != 0:
        print(json.dumps({"error": data2.get("msg"), "code": data2.get("code")}, ensure_ascii=False, indent=2))
        sys.exit(1)
    file_token = data2["data"]["file_token"]

    # Step 3: 绑定素材到图片块
    resp3 = requests.patch(
        f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{block_id}",
        headers=headers(),
        json={"replace_image": {"token": file_token}},
    )
    data3 = resp3.json()
    if data3.get("code") != 0:
        print(json.dumps({"error": data3.get("msg"), "code": data3.get("code")}, ensure_ascii=False, indent=2))
        sys.exit(1)

    img = data3.get("data", {}).get("block", {}).get("image", {})
    out({
        "block_id": block_id,
        "file_token": file_token,
        "width": img.get("width"),
        "height": img.get("height"),
        "message": "图片插入成功",
    })


# ---------------------------------------------------------------------------
# Wiki (知识库) commands
# ---------------------------------------------------------------------------
def cmd_list_files(folder_token=None, page_size=None):
    """列出云空间文件（默认根目录）"""
    params = {"page_size": int(page_size) if page_size else 50}
    if folder_token:
        params["folder_token"] = folder_token
    data = api("GET", "drive/v1/files", params=params)
    files = data.get("files", [])
    out({
        "files": [{"token": f.get("token"), "name": f.get("name"), "type": f.get("type"),
                    "url": f.get("url")} for f in files],
        "total": len(files),
        "has_more": data.get("has_more", False),
    })


def cmd_delete_file(file_token, file_type):
    """删除云空间文件。file_type: docx, bitable, sheet, file 等"""
    api("DELETE", f"drive/v1/files/{file_token}", params={"type": file_type})
    out({"message": f"文件 {file_token} 删除成功", "type": file_type})


def cmd_create_wiki_space(name, description=""):
    body = {"name": name}
    if description:
        body["description"] = description
    data = api("POST", "wiki/v2/spaces", json=body)
    space = data.get("space", {})
    out({
        "space_id": space.get("space_id"),
        "name": space.get("name"),
        "message": "知识库创建成功",
    })


def cmd_list_wiki_spaces():
    data = api("GET", "wiki/v2/spaces", params={"page_size": 50})
    spaces = data.get("items", [])
    out({
        "spaces": [{"space_id": s.get("space_id"), "name": s.get("name"), "description": s.get("description")} for s in spaces],
        "total": len(spaces),
    })


def cmd_list_wiki_nodes(space_id, parent_node_token=None):
    params = {"page_size": 50}
    if parent_node_token:
        params["parent_node_token"] = parent_node_token
    data = api("GET", f"wiki/v2/spaces/{space_id}/nodes", params=params)
    nodes = data.get("items", [])
    out({
        "nodes": [{"node_token": n.get("node_token"), "obj_token": n.get("obj_token"),
                    "obj_type": n.get("obj_type"), "title": n.get("title"),
                    "has_child": n.get("has_child")} for n in nodes],
        "total": len(nodes),
    })


def cmd_create_wiki_node(space_id, title, parent_node_token=None, obj_type="docx"):
    """在知识库中创建文档节点"""
    body = {
        "obj_type": obj_type,
        "title": title,
    }
    if parent_node_token:
        body["parent_node_token"] = parent_node_token
    data = api("POST", f"wiki/v2/spaces/{space_id}/nodes", json=body)
    node = data.get("node", {})
    out({
        "node_token": node.get("node_token"),
        "obj_token": node.get("obj_token"),
        "obj_type": node.get("obj_type"),
        "title": node.get("title"),
        "url": f"https://feishu.cn/wiki/{node.get('node_token')}",
        "message": "知识库文档创建成功",
    })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
COMMANDS = {
    "login": cmd_login,
    "logout": cmd_logout,
    "whoami": cmd_whoami,
    "token": lambda: out({"token": get_token()}),
    "create_doc": cmd_create_doc,
    "get_doc": cmd_get_doc,
    "add_blocks": cmd_add_blocks,
    "create_bitable": cmd_create_bitable,
    "get_bitable": cmd_get_bitable,
    "create_table": cmd_create_table,
    "list_tables": cmd_list_tables,
    "list_fields": cmd_list_fields,
    "create_field": cmd_create_field,
    "list_records": cmd_list_records,
    "create_record": cmd_create_record,
    "batch_create_records": cmd_batch_create_records,
    "update_record": cmd_update_record,
    "delete_record": cmd_delete_record,
    "insert_image": cmd_insert_image,
    "list_files": cmd_list_files,
    "delete_file": cmd_delete_file,
    "create_wiki_space": cmd_create_wiki_space,
    "list_wiki_spaces": cmd_list_wiki_spaces,
    "list_wiki_nodes": cmd_list_wiki_nodes,
    "create_wiki_node": cmd_create_wiki_node,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    args = sys.argv[2:]
    try:
        COMMANDS[cmd](*args)
    except TypeError as e:
        print(f"参数错误: {e}")
        sys.exit(1)
