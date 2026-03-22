---
name: feishu
description: 飞书云文档、多维表格和云空间操作。当用户提到"飞书"、"多维表格"、"bitable"、"数据表"、"飞书文档"、"知识库"、"wiki"，或需要创建/管理飞书文档和多维表格时使用此 Skill。
---

# 飞书操作 Skill

通过 CLI 脚本操作飞书云文档、多维表格和云空间。

**参考文档**（详细字段类型、Markdown 格式、错误码等）：
- `references/bitable-guide.md` — 多维表格完整指南（字段类型、筛选、批量操作、错误码）
- `references/create-doc-guide.md` — 文档创建指南（**Lark-flavored Markdown 完整格式规范**）
- `references/fetch-doc-guide.md` — 文档读取指南
- `references/update-doc-guide.md` — 文档更新指南（7种更新模式、定位方式）

## 调用方式

```bash
python3 <skill_dir>/scripts/feishu.py <command> [args...]
```

> `<skill_dir>` 为本 Skill 解压后的根目录。首次使用前需 `pip install requests`。

## 工具名映射

参考文档中使用的是 OpenClaw 工具名，对应关系如下：

| OpenClaw 工具名 | 本 Skill CLI 命令 |
|-----------------|-------------------|
| `feishu_mcp_create_doc` | `create_doc <title> [folder_token]` |
| `feishu_mcp_fetch_doc` | `get_doc <document_id>` |
| `feishu_mcp_update_doc` / `feishu_doc_add_blocks` | `add_blocks <document_id> <children_json> [block_id]` |
| `feishu_bitable_app` create | `create_bitable <name> [folder_token]` |
| `feishu_bitable_app` get | `get_bitable <app_token>` |
| `feishu_bitable_app_table` create | `create_table <app_token> <name> [fields_json]` |
| `feishu_bitable_app_table` list | `list_tables <app_token>` |
| `feishu_bitable_app_table` delete | 对应 `delete` 但需要自行扩展 |
| `feishu_bitable_app_table_field` list | `list_fields <app_token> <table_id>` |
| `feishu_bitable_app_table_field` create | `create_field <app_token> <table_id> <name> <type> [property_json]` |
| `feishu_bitable_app_table_record` list | `list_records <app_token> <table_id> [filter_json] [page_size]` |
| `feishu_bitable_app_table_record` create | `create_record <app_token> <table_id> <fields_json>` |
| `feishu_bitable_app_table_record` batch_create | `batch_create_records <app_token> <table_id> <records_json>` |
| `feishu_bitable_app_table_record` update | `update_record <app_token> <table_id> <record_id> <fields_json>` |
| `feishu_bitable_app_table_record` delete | `delete_record <app_token> <table_id> <record_id>` |

## 首次使用初始化

首次使用本 Skill 时，必须完成以下初始化流程：

### 1. 检查身份状态

运行 `whoami` 查看当前身份。如果返回 `tenant` 模式，需要登录用户身份。

### 2. 登录用户身份

运行 `login` 发起 OAuth 授权。浏览器会自动打开飞书授权页面，用户点击"同意授权"即可。

如果授权页面提示**权限不足**（如 `Missing permissions`），说明飞书应用尚未开通对应的用户身份权限，需要引导用户按下面步骤操作：

### 3. 开通应用权限（仅首次需要）

告知用户前往 [飞书开放平台](https://open.feishu.cn/app) 后台，对应用进行以下配置：

1. **安全设置** → **重定向 URL**：添加 `http://localhost:9876/callback`
2. **权限管理** → 搜索并开通以下权限（同时开通**应用权限**和**用户权限**两栏）：

| 权限标识 | 说明 | 用途 |
|----------|------|------|
| `docx:document` | 云文档读写 | 创建/读取/编辑文档 |
| `drive:drive` | 云空间文件管理 | 列出/删除文件、指定文件夹 |
| `bitable:app` | 多维表格读写 | 创建/管理多维表格和数据 |
| `wiki:wiki` | 知识库读写 | 知识库空间和节点操作 |

3. **版本管理与发布** → 创建版本并发布（或请管理员审批发布）

完成后重新运行 `login`，授权成功会显示用户名和 open_id。

### 4. 验证

登录成功后运行 `whoami` 确认返回 `user` 模式，再运行 `list_files` 验证权限正常。

## 身份与认证

| 命令 | 说明 |
|------|------|
| `whoami` | 查看当前身份（user 或 tenant） |
| `login` | OAuth 登录，切换到用户个人账号 |
| `logout` | 退出登录，回到应用身份 |

**策略：**
- **必须使用 user 模式**：执行任何操作前，先 `whoami` 确认身份为 `user`。如果是 `tenant` 模式，必须先执行 `login` 切换到用户身份，不得直接以应用身份创建文档或表格（应用身份创建的内容用户在飞书中看不到）。
- 只有用户明确表示允许使用应用身份时，才可在 `tenant` 模式下操作。
- `login` 命令会启动本地回调服务器并打开浏览器，需要等待用户完成授权（超时 120s），调用时设置足够的 timeout。
- Token 2小时有效，过期自动刷新（30天），无需反复登录。
- API 返回 token expired 或权限错误时，先 `whoami` 检查，必要时重新 `login`。

## 完整命令列表

### 云空间

| 命令 | 参数 | 说明 |
|------|------|------|
| `list_files` | `[folder_token] [page_size]` | 列出文件（默认根目录） |
| `delete_file` | `<file_token> <file_type>` | 删除文件（type: docx/bitable/sheet/file） |

### 文档

| 命令 | 参数 | 说明 |
|------|------|------|
| `create_doc` | `<title> [folder_token]` | 创建文档 |
| `get_doc` | `<document_id>` | 获取文档内容 |
| `add_blocks` | `<document_id> <children_json> [block_id]` | 向文档追加内容块 |
| `insert_image` | `<document_id> <file_path>` | 向文档插入本地图片 |

### 多维表格

| 命令 | 参数 | 说明 |
|------|------|------|
| `create_bitable` | `<name> [folder_token]` | 创建多维表格 App |
| `get_bitable` | `<app_token>` | 获取信息 |
| `create_table` | `<app_token> <name> [fields_json]` | 创建数据表 |
| `list_tables` | `<app_token>` | 列出数据表 |
| `list_fields` | `<app_token> <table_id>` | 列出字段 |
| `create_field` | `<app_token> <table_id> <name> <type> [property_json]` | 创建字段 |
| `list_records` | `<app_token> <table_id> [filter_json] [page_size]` | 查询记录 |
| `create_record` | `<app_token> <table_id> <fields_json>` | 创建记录 |
| `batch_create_records` | `<app_token> <table_id> <records_json>` | 批量创建（≤500条） |
| `update_record` | `<app_token> <table_id> <record_id> <fields_json>` | 更新记录 |
| `delete_record` | `<app_token> <table_id> <record_id>` | 删除记录 |

### 知识库

| 命令 | 参数 | 说明 |
|------|------|------|
| `list_wiki_spaces` | | 列出知识库 |
| `create_wiki_space` | `<name> [description]` | 创建知识库 |
| `list_wiki_nodes` | `<space_id> [parent_node_token]` | 列出节点 |
| `create_wiki_node` | `<space_id> <title> [parent_node_token] [obj_type]` | 创建文档 |

## 典型工作流

### 在指定文件夹创建文档

```bash
python3 feishu.py list_files            # 找到 folder_token
python3 feishu.py create_doc "标题" <folder_token>
```

### 创建多维表格（完整流程）

```bash
# 1. 创建 App
python3 feishu.py create_bitable "项目跟踪"

# 2. 创建数据表 + 字段
python3 feishu.py create_table <app_token> "任务列表" \
  '[{"field_name":"任务名","type":1},{"field_name":"状态","type":3,"property":{"options":[{"name":"待办"},{"name":"进行中"},{"name":"已完成"}]}},{"field_name":"截止日期","type":5}]'

# 3. 写入前先查字段（确认 type/ui_type）
python3 feishu.py list_fields <app_token> <table_id>

# 4. 批量写入
python3 feishu.py batch_create_records <app_token> <table_id> \
  '[{"fields":{"任务名":"需求评审","状态":"进行中","截止日期":1711900800000}}]'
```

## 关键注意事项

1. **写记录前先 list_fields** — 确认字段 type，避免格式错误
2. **日期必须用毫秒时间戳** — 如 `1711900800000`，不能用字符串
3. **复选框(7)和超链接(15)** — 创建字段时不能传 property
4. **单选 vs 多选** — 单选用 `"string"`，多选用 `["a","b"]`
5. **批量操作** — 每次最多 500 条，同表串行执行
6. **默认表有空行** — `create_bitable` 自带的默认表有空记录，先删再插
7. **JSON shell 转义** — 用**单引号**包裹 JSON 参数
8. **权限错误** — 先 `whoami`，必要时 `login`
9. **block 属性名与官方文档不一致**（`add_blocks` 踩坑重点）：
   - block_type 12（无序列表）→ 属性名 `"bullet"`（**不是** `"bulleted_list"`）
   - block_type 13（有序列表）→ 属性名 `"ordered"`（**不是** `"ordered_list"`）
   - 所有文本类 block 的 elements 和根级都需要 `"style": {}`
10. **图片不能用 add_blocks 插入** — 必须用 `insert_image` 命令（三步流程：创建空图片块 → 上传素材 → 绑定）

## 配置方式

支持两种配置方式（环境变量优先级高于配置文件）：

### 方式一：`.env` 文件（推荐团队分发）

将 `.env` 放在 `scripts/` 目录下：

```env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_SHARED_FOLDER=xxx
```

团队内部分发时只需发这个 `.env` 文件即可。`FEISHU_SHARED_FOLDER` 配置后，`create_doc` 和 `create_bitable` 默认创建到该文件夹。

### 方式二：环境变量（优先级高于 .env）

| 变量名 | 说明 |
|--------|------|
| `FEISHU_APP_ID` | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret |
| `FEISHU_SHARED_FOLDER` | 默认共享文件夹 folder_token |
