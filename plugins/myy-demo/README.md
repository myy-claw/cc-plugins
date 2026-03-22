# myy-demo

示例插件 - 包含问候、时间和笑话等趣味 skills。

## 包含的 Skills

| Skill | 调用方式 | 说明 |
|-------|---------|------|
| hello | `/myy-demo:hello` | 简单的 Hello World 问候 |
| time | `/myy-demo:time` | 报告当前日期和时间 |
| joke | `/myy-demo:joke` | 讲一个程序员笑话 |

## 安装

此插件作为 `myy-cc-plugins` 市场的一部分发布，安装市场后即可使用：

```
/plugin marketplace add myy-claw/cc-plugins
```

也可单独加载进行本地测试：

```
claude --plugin-dir ./plugins/myy-demo
```
