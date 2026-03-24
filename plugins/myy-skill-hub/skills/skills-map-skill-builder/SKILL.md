---
name: skills-map-skill-builder
description: >
  专门用于 skills-map 门户项目的实践案例制作。仅在用户明确要求为 skills-map 门户制作、补充或更新 Skill 实践案例时触发。
  典型触发语句："为 skills-map 制作实践案例"、"给门户补充 xlsx 的案例"、"用 skills-map-skill-builder 跑一下"。
  不要在普通的文档制作、表格生成、PPT 创建等日常任务中触发，那些应该直接使用对应的 Skill。
---

# 制作实践案例

为 skills-map 门户制作实践案例。每个案例 = 对话示例 .md + 真实产物文件。

## 执行流程

### 第一步：了解目标 Skill

1. 通过 Skill 工具调用目标 Skill（如 `Skill: xlsx`），加载其完整指令。阅读指令了解技术栈、输出格式和后处理要求。Skill 工具对同一 skill 只加载一次，后续按加载的指令执行。
2. 读取 `skills/{skill-id}/GUIDE.md`，获取 scenarios 列表和已有案例，避免重复。
3. 查看 `skills/{skill-id}/examples/` 目录，确认已有哪些案例。

### 第二步：规划 + 用户确认

规划 3 个案例（或用户指定数量），输出规划表：

| 序号 | 案例标题 | 角色 | 场景标签 | 产物文件 |
|------|----------|------|----------|----------|

要求：
- scenario 必须从 GUIDE.md 的 scenarios 列表中选取
- 与已有案例不重复
- 场景贴合地产 ERP 实际工作，难度适中

**输出规划表后，等用户确认再继续。**

### 第三步：生成产物文件

严格按照第一步加载的 Skill 指令生成每个产物。关键：
- 使用 Skill 指定的技术栈和工具链，不要自创实现
- 如果 Skill 指令有后处理步骤（公式重算、环境变量等），必须执行
- 每个文件生成后检查：文件存在且大小合理

保存到：`skills/{skill-id}/assets/{案例标题}.{ext}`

### 第四步：编写案例 Markdown

保存到：`skills/{skill-id}/examples/{案例标题}.md`

**Frontmatter：**
```yaml
---
title: 案例标题
scenario: 场景标签（匹配 GUIDE.md 中 scenarios 的值）
brief: 一句话描述（20字以内）
files:
  - name: 产物文件名.ext
    type: 文件扩展名
    label: 产物中文描述
---
```

**正文两个部分：**

`## 对话示例` — 用 `**用户**：` 和 `**AI**：` 标记（中文冒号）。用户的话自然口语化，包含具体业务数据；AI 回复展示产物关键特征。1-2 轮对话，不超过 3 轮。不用 emoji。

`## 操作步骤` — 4-5 步，用户视角。

### 第五步：验证 + 更新数据

检查每个案例：
1. 产物文件存在且非空
2. frontmatter 的 scenario 在 GUIDE.md scenarios 列表中
3. 对话使用 `**用户**：` / `**AI**：` 标记（中文冒号）
4. 无 emoji

运行 `python3 generate-portal-data.py`，确认输出计数符合预期。

### 第六步：提交

向用户确认后 git commit。

## 批量执行

为多个 Skill 生成案例时，用 Agent 工具并行。每个 agent 需自行读取目标 Skill 的 SKILL.md（子 agent 中 Skill 工具不可用）。所有 agent 完成后统一运行数据管道。

## 注意事项

- Python 用 `python3`（macOS 上 `python` 不可用）
- 不要用 emoji，这是门户设计规范
