# myy-cc-plugins

myy-claw 的 Claude Code 插件市场。

## 安装

```
/plugin marketplace add myy-claw/plugin-myy-dev
```

## 插件列表

| 插件 | 说明 | 版本 |
|------|------|------|
| [myy-hello](./plugins/myy-hello) | 示例插件 - Hello World skill | 1.0.0 |

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
