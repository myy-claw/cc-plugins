# myy-demo-a

示例插件 A - 包含问候、时间和笑话等趣味 skills。

## 包含的 Skills

| Skill | 调用方式 | 说明 |
|-------|---------|------|
| hello | `/myy-demo-a:hello` | 简单的 Hello World 问候 |
| time | `/myy-demo-a:time` | 报告当前日期和时间 |
| joke | `/myy-demo-a:joke` | 讲一个程序员笑话 |

## 安装

此插件作为 `myy-cc-plugins` 市场的一部分发布，安装市场后即可使用：

```
/plugin marketplace add myy-claw/plugin-myy-dev
```

也可单独加载进行本地测试：

```
claude --plugin-dir ./plugins/myy-demo-a
```
