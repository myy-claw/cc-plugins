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
|   o  myy-demo-a  · myy-cc-plugins                                       |
|      示例插件 A - 问候、时间、笑话                                       |
|                                                                          |
|   o  myy-demo-b  · myy-cc-plugins                                       |
|      示例插件 B - 文本总结、翻译                                         |
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
> /myy-demo-a:hello                # Hello World 问候
> /myy-demo-a:joke                 # 讲个程序员笑话
> /myy-demo-b:summarize            # 文本总结
> /myy-demo-b:translate            # 中英互译
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
