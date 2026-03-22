---
name: joke
description: 讲一个程序员笑话，支持指定主题
---

# Joke Skill

讲一个轻松有趣的程序员笑话。

## 使用方式

用户通过 `/myy-demo-a:joke` 调用此 skill。

## 行为

### 指令

- 如果 `$ARGUMENTS` 为空，随机讲一个经典的程序员/IT 相关笑话
- 如果 `$ARGUMENTS` 指定了主题（如 "Python"、"前端"、"产品经理"），围绕该主题讲笑话
- 笑话要简短有趣，适合工作场合
- 讲完笑话后附上一句简短的技术点评或吐槽
