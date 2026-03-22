---
name: time
description: 报告当前日期和时间，支持自定义格式
---

# Time Skill

报告当前的日期和时间信息。

## 使用方式

用户通过 `/myy-demo-a:time` 调用此 skill。

## 行为

### 指令

- 如果 `$ARGUMENTS` 为空，以友好的方式告诉用户当前的日期和时间，包含星期几
- 如果 `$ARGUMENTS` 包含 "倒计时" 或 "countdown"，计算从今天到用户指定日期的天数差
- 如果 `$ARGUMENTS` 包含其他内容，尝试按用户要求的格式或时区回答时间相关问题
