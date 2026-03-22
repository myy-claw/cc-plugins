# myy-cc-plugins

myy-claw 的 Claude Code 插件市场。

## 使用指引

### Step 1: 添加市场

在 Claude Code 中执行：

```
/plugin marketplace add myy-claw/cc-plugins
```

### Step 2: 发现插件

执行 `/plugin`，切换到 **Discover** 标签页，搜索 `myy` 即可看到市场中的所有插件。

### Step 3: 安装插件

选择需要的插件，按 Enter 查看详情，选择安装范围：

- **Install for you (user scope)** — 安装到你的用户级别，所有项目可用
- **Install for all collaborators (project scope)** — 安装到项目级别，团队协作者共享
- **Install for you, in this repo only (local scope)** — 仅当前仓库可用

### Step 4: 使用 Skill

安装后通过 `/<plugin-name>:<skill-name>` 调用，例如：

```
/myyclaw-dev:feishu
/myy-demo-a:hello
/myy-demo-b:summarize
```

## 插件列表

| 插件 | 说明 | 版本 |
|------|------|------|
| [myy-demo-a](./plugins/myy-demo-a) | 示例插件 A - 问候、时间、笑话 | 1.0.0 |
| [myy-demo-b](./plugins/myy-demo-b) | 示例插件 B - 文本总结、翻译 | 1.0.0 |
| [myyclaw-dev](./plugins/myyclaw-dev) | 开发团队工具集 - 飞书文档管理 | 1.0.0 |

## 添加新插件

1. 在 `plugins/` 目录下创建新的插件目录
2. 添加 `.claude-plugin/plugin.json` 插件清单
3. 在 `skills/` 目录下创建 skill 定义
4. 在根目录 `.claude-plugin/marketplace.json` 的 `plugins` 数组中注册新插件
5. 更新本 README 的插件列表

## 目录结构

```
cc-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace 清单
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json       # 插件清单
│       ├── skills/
│       │   └── <skill-name>/
│       │       └── SKILL.md      # Skill 定义
│       └── README.md
├── README.md
└── LICENSE
```

## 许可证

MIT
