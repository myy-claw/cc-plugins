# Claude Code Plugin Marketplace - 开发规范

## 项目概览

本仓库是 **myy-claw** 的 Claude Code 插件市场（Marketplace），托管于 `https://github.com/myy-claw/cc-plugins`。用户通过以下命令安装：

```
/plugin marketplace add myy-claw/cc-plugins
```

## 仓库结构

```
cc-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace 清单（注册所有插件）
├── plugins/
│   └── <plugin-name>/            # 每个插件一个独立目录
│       ├── .claude-plugin/
│       │   └── plugin.json       # 插件清单
│       ├── skills/
│       │   └── <skill-name>/
│       │       └── SKILL.md      # Skill 定义文件
│       └── README.md             # 插件说明
├── CLAUDE.md                     # 本文件
├── README.md
└── LICENSE
```

## 插件开发规范

### 命名规则

- **插件名**：使用 `myy-` 前缀 + 小写短横线命名，如 `myy-hello`、`myy-tools`
- **Skill 名**：小写短横线命名，如 `hello`、`code-review`
- **调用格式**：`/<plugin-name>:<skill-name>`，如 `/myy-hello:hello`

### 新增插件步骤

1. 在 `plugins/` 下创建插件目录 `plugins/<plugin-name>/`
2. 创建插件清单 `plugins/<plugin-name>/.claude-plugin/plugin.json`
3. 在 `plugins/<plugin-name>/skills/<skill-name>/` 下创建 `SKILL.md`
4. 创建 `plugins/<plugin-name>/README.md` 说明插件用途和包含的 skills
5. 在根目录 `.claude-plugin/marketplace.json` 的 `plugins` 数组中注册
6. 更新根目录 `README.md` 的插件列表

### plugin.json 格式

```json
{
  "name": "<plugin-name>",
  "version": "<semver>",
  "description": "插件简短描述",
  "author": {
    "name": "myy-claw"
  }
}
```

### marketplace.json 注册格式

在 `plugins` 数组中添加：

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "插件简短描述",
  "version": "<semver>",
  "keywords": ["keyword1", "keyword2"]
}
```

### SKILL.md 编写规范

```markdown
---
name: <skill-name>
description: 简短描述该 skill 的用途（一句话）
---

# <Skill 标题>

## 使用方式
说明如何调用，包含 `$ARGUMENTS` 的用法。

## 行为
描述 skill 被调用时的具体行为和指令。
```

**关键要素：**
- frontmatter 中 `name` 和 `description` 为必填
- 使用 `$ARGUMENTS` 引用用户传入的参数
- 行为描述要清晰、具体，Claude 会严格按照 SKILL.md 中的指令执行
- 避免在 skill 中硬编码敏感信息

### 版本管理

- 遵循语义化版本 [SemVer](https://semver.org/)：`MAJOR.MINOR.PATCH`
- 新增 skill → MINOR 版本递增
- 修复 skill 行为 → PATCH 版本递增
- 不兼容变更（重命名/删除 skill）→ MAJOR 版本递增
- plugin.json 和 marketplace.json 中的版本号保持一致

## Git 提交规范

使用 Conventional Commits 风格：

- `feat: 新增 xxx 插件/skill`
- `fix: 修复 xxx skill 的 xxx 问题`
- `docs: 更新文档`
- `refactor: 重构 xxx`
- `chore: 杂项维护`

## 本地测试

单个插件本地加载测试：

```bash
claude --plugin-dir ./plugins/<plugin-name>
```

然后在会话中调用 `/<plugin-name>:<skill-name>` 验证行为。

## 安全与合规规范（必须遵守）

### 禁止提交的内容

以下内容**严禁出现在 git 跟踪的文件中**，违反将导致安全风险：

1. **密钥和凭据**
   - API Key、Secret、Token（如 `sk-xxx`、`cli_xxx`、`APP_SECRET` 的值）
   - OAuth 令牌、refresh_token
   - 数据库连接字符串、密码
   - 任何 `.env` 文件中的实际值

2. **本地路径**
   - 绝对路径（如 `/Users/xxx/...`、`C:\Users\xxx\...`）
   - 用户主目录路径
   - 脚本中应使用相对路径或 `<skill_dir>` 占位符

3. **客户信息和内部资料**
   - 客户名称、项目名称、业务数据
   - 内部知识库结构、产品方案文档
   - 测试数据中的真实业务信息
   - 截图、图片中包含的客户内容

### .gitignore 必须包含

```
.env
.feishu_user_token.json
test/
__pycache__/
*.pyc
.DS_Store
```

### 提交前检查

每次 `git add` 前，确认以下事项：
- `git diff --cached` 中无密钥、凭据、本地路径
- 不包含 test/ 目录下的文件
- 不包含 .env 或其他配置文件中的敏感值
- 新增的 .gitignore 规则已生效

### 敏感文件的处理方式

| 文件类型 | 处理方式 |
|---------|---------|
| `.env` | 放在本地，gitignore 忽略，README 中说明配置项 |
| `test/` | 放在本地，gitignore 忽略，仅用于本地测试 |
| 配置模板 | 可提交 `.env.example`（只含变量名，不含值） |
| token 缓存文件 | gitignore 忽略 |

## 其他注意事项

- 每个插件保持独立，不要跨插件引用文件
- SKILL.md 是给 Claude 读的指令，要写得像 prompt，清晰准确
- 输出语言默认为中文
