---
name: hello
description: 一个简单的 Hello World 示例 skill，用于演示插件基本用法
---

# Hello Skill

你好！我是 myy-demo 插件的示例 skill。

## 使用方式

用户可以通过 `/myy-demo:hello` 调用此 skill。

## 行为

当被调用时，向用户打招呼。如果用户提供了参数，使用参数内容进行个性化问候。

### 指令

- 如果 `$ARGUMENTS` 为空，回复："你好！我是 myy-demo 示例插件。很高兴见到你！"
- 如果 `$ARGUMENTS` 不为空，回复："你好，$ARGUMENTS！欢迎使用 myy-demo 示例插件！"
