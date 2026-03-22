# myyclaw-dev

myyclaw 开发团队工具集，用于管理团队飞书文档、开发规范等。

## 包含的 Skills

| Skill | 调用方式 | 说明 |
|-------|---------|------|
| feishu | `/myyclaw-dev:feishu` | 飞书云文档、多维表格和云空间操作 |

## 飞书 Skill 功能

- 云文档：创建、读取、编辑飞书文档
- 多维表格：创建表格、管理字段、增删改查记录
- 云空间：文件管理、文件夹操作
- 知识库：知识库和节点管理
- OAuth 用户身份认证

### 首次使用

1. 在 `plugins/myyclaw-dev/skills/feishu/scripts/` 目录下配置 `.env` 文件
2. 安装依赖：`pip install requests`
3. 在 Claude Code 中调用 `/myyclaw-dev:feishu`，按提示完成 OAuth 登录

## 安装

此插件作为 `myy-cc-plugins` 市场的一部分发布：

```
/plugin marketplace add myy-claw/cc-plugins
```

也可单独加载进行本地测试：

```
claude --plugin-dir ./plugins/myyclaw-dev
```
