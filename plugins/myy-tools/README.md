# myy-tools

实用工具集插件 - 文本处理与辅助工具。

## 包含的 Skills

| Skill | 调用方式 | 说明 |
|-------|---------|------|
| summarize | `/myy-tools:summarize` | 将文本或文件内容总结为简洁的要点 |
| translate | `/myy-tools:translate` | 中英文互译，支持代码注释和文档翻译 |

## 安装

此插件作为 `myy-cc-plugins` 市场的一部分发布：

```
/plugin marketplace add myy-claw/plugin-myy-dev
```

也可单独加载进行本地测试：

```
claude --plugin-dir ./plugins/myy-tools
```
