# myy-demo-b

示例插件 B - 文本总结、翻译。

## 包含的 Skills

| Skill | 调用方式 | 说明 |
|-------|---------|------|
| summarize | `/myy-demo-b:summarize` | 将文本或文件内容总结为简洁的要点 |
| translate | `/myy-demo-b:translate` | 中英文互译，支持代码注释和文档翻译 |

## 安装

此插件作为 `myy-cc-plugins` 市场的一部分发布：

```
/plugin marketplace add myy-claw/plugin-myy-dev
```

也可单独加载进行本地测试：

```
claude --plugin-dir ./plugins/myy-demo-b
```
