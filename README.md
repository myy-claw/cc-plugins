# myy-cc-plugins

myy-claw 的 Claude Code 插件市场。

## 使用指引

### Step 1: 添加市场

在 Claude Code 中执行以下命令，将本市场添加到你的插件源：

```
> /plugin marketplace add myy-claw/cc-plugins
    Successfully added marketplace: myy-cc-plugins
```

### Step 2: 发现插件

执行 `/plugin`，切换到 **Discover** 标签页，搜索关键词即可浏览市场中的插件：

```
+--------------------------------------------------------------------------+
| Plugins [Discover]  Installed   Marketplaces   Errors                    |
|--------------------------------------------------------------------------|
| Discover plugins                                                         |
| +----------------------------------------------------------------------+ |
| | > myy                                                                | |
| +----------------------------------------------------------------------+ |
|                                                                          |
|   o  myy-demo    · myy-cc-plugins                                       |
|      示例插件 - 问候、时间、笑话                                         |
|                                                                          |
| > *  myyclaw-dev  · myy-cc-plugins                                       |
|      myyclaw 开发团队工具集 - 飞书文档管理、开发规范等                   |
|                                                                          |
| i to install · type to search · Space to toggle · Enter to details       |
+--------------------------------------------------------------------------+
```

### Step 3: 安装插件

选中插件后按 **空格键** 勾选要安装的插件（`o` 变为 `*`），然后按 **Enter** 进入详情页，选择安装范围：

```
+--------------------------------------------------------------------------+
| Plugin details                                                           |
|                                                                          |
| myyclaw-dev                                                              |
| from myy-cc-plugins                                                      |
| Version: 1.0.0                                                           |
|                                                                          |
| myyclaw 开发团队工具集 - 飞书文档管理、开发规范等                        |
|                                                                          |
| > Install for you (user scope)            <-- 所有项目可用               |
|   Install for all collaborators (project scope)  <-- 团队共享            |
|   Install for you, in this repo only (local scope)  <-- 仅当前仓库      |
|   Back to plugin list                                                    |
|                                                                          |
| Enter to select · Esc to back                                            |
+--------------------------------------------------------------------------+
```

### Step 4: 使用 Skill

安装完成后，通过 `/<plugin-name>:<skill-name>` 调用：

```
> /myyclaw-dev:feishu              # 飞书文档管理
> /myy-demo:hello                  # Hello World 问候
> /myy-demo:time                   # 当前时间
> /myy-demo:joke                   # 讲个程序员笑话
```

### Step 5: 更新插件

插件发布新版本后，执行 `/plugin` 切换到 **Installed** 标签页，选中要更新的插件按 **Enter** 进入详情页：

```
+--------------------------------------------------------------------------+
| Plugins   Discover   [Installed]   Marketplaces   Errors                 |
|--------------------------------------------------------------------------|
|                                                                          |
| myyclaw-dev @ myy-cc-plugins                                            |
| Scope: user                                                              |
| Version: 1.0.0                                                           |
| myyclaw 开发团队工具集 - 飞书文档管理、开发规范等                        |
|                                                                          |
| Author: myy-claw                                                         |
| Status: Enabled                                                          |
|                                                                          |
| Installed components:                                                    |
| · Skills: feishu                                                         |
|                                                                          |
|   Disable plugin                                                         |
|   Mark for update                                                        |
| > Update now                        <-- 选择此项立即更新                  |
|   Uninstall                                                              |
|   Back to plugin list                                                    |
|                                                                          |
| ctrl+p to navigate · Enter to select · Esc to back                      |
+--------------------------------------------------------------------------+
```

选择 **"Update now"** 后会提示更新成功：

```
✓ Updated myyclaw-dev. Run /reload-plugins to apply.
```

最后执行 `/reload-plugins` 使更新生效：

```
> /reload-plugins
  Reloaded: 10 plugins · 12 commands · 11 agents · 1 hook · 2 plugin MCP servers
```

> **提示**：更新后必须执行 `/reload-plugins`，新的 Skill 内容才会在当前会话中生效。

## 插件列表

| 插件 | 说明 | 版本 |
|------|------|------|
| [myy-demo](./plugins/myy-demo) | 示例插件 - 问候、时间、笑话、视频处理 | 1.0.0 |
| [myyclaw-dev](./plugins/myyclaw-dev) | 开发团队工具集 - 飞书文档管理 | 1.1.0 |
| [myy-skill-hub](./plugins/myy-skill-hub) | 技能市场维护 - skills-map 门户案例制作 | 1.0.0 |

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
