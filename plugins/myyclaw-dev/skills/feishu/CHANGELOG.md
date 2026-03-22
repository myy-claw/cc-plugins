# Changelog - feishu skill

从 feishu-skill 独立仓库迁移而来的变更记录。

## 1627e7d - refactor: 配置改为 .env 文件方式

**日期**: 2026-03-22

- 替换 feishu-config.json 为标准 .env 格式
- 脚本内置轻量 .env 解析，无需额外依赖
- 环境变量优先级高于 .env 文件

## 22885b0 - feat: 支持 feishu-config.json 配置文件

**日期**: 2026-03-22

- 配置文件注入环境变量（app_id/app_secret/shared_folder）
- create_doc/create_bitable 默认使用 shared_folder
- 环境变量优先级高于配置文件
- .gitignore 排除 feishu-config.json（含敏感凭据）

## 9cd7de3 - docs: 分发前检查修复

**日期**: 2026-03-22

- SKILL.md: 移除硬编码绝对路径，改为 `<skill_dir>` 占位
- SKILL.md: 补充 insert_image 命令文档
- SKILL.md: 补充 block 属性名坑点说明（bullet/ordered）
- SKILL.md: 补充环境变量配置说明
- feishu.py: 更新 docstring，补全所有命令（drive/wiki/insert_image）

## 75b1b31 - feat: 新增 insert_image 命令，支持向文档插入图片

**日期**: 2026-03-22

- 三步流程：创建空图片块 → 上传图片素材 → 绑定素材到图片块
- 用法：`python3 feishu.py insert_image <document_id> <file_path>`

## 3e61cad - feat: 初始化飞书 skill 项目

**日期**: 2026-03-22

- SKILL.md: 飞书文档/多维表格 CLI 操作指南，含 OAuth 认证流程
- scripts/feishu.py: 飞书 API CLI 工具（文档、多维表格、知识库、云空间）
- references/: 多维表格、文档创建/读取/更新参考文档
- test/: MyyClaw 知识库结构和 OpenClaw README 测试文件
