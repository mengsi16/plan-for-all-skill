<div align="center">

# Plan-For-All

*像 Manus 一样用文件持久化记忆，像 TDD 一样用小步执行。*

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.com/claude-code)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Claude-Code-Skill** | **Manus-Style** | **MIT License** | **TDD-Driven** | **Hook-Powered** | **Disk-Persistent**

</div>

---

<div align="center">

**🌐 Language / 语言**

[**简体中文**](README.md) | [English](README_en.md)

</div>

---

## 痛点

你是否经历过这些崩溃时刻？

| 场景 | 结果 |
|------|------|
| Claude Code Plan Mode 上下文被压缩 | 辛辛苦苦梳理的需求全部丢失，ToDo 永远无法完成 |
| brainstorming + writing-plans 输出一大段计划 | 疯狂冲击上下文，导致 Claude Code 回退到默认工具调用，忘记使用你指定的 skills |
| 长任务执行到一半会话中断 | 再次打开时完全不记得做到了哪里，一切从头开始 |

**Plan-For-All** 汲取 planning-with-files（Manus 思想）的核心——将计划写入磁盘，彻底杜绝上下文压缩导致的计划丢失。借鉴 superpowers 的需求设计与计划拆解理念，并将其真正落实为小文件形式（step_subplan），避免大段计划内容涌入上下文。

---

## 核心思想

Plan-For-All 将大段的计划拆解成一个个小计划，基于 `task_plan.md` 文档进行统筹，每进行到下一阶段自动读取小计划的内容，始终让 **计划是最新状态**，让 **上下文是干净状态**。

```
┌────────────────────────────────────────────────────────────┐
│  传统方式: 全部塞进上下文 → 压缩丢失                         │
│  Plan-For-All: 计划写入磁盘 → 按需读取 → 上下文永远干净      │
└────────────────────────────────────────────────────────────┘
```

---

## 工作流程

```
Phase 1: BRAINSTORMING          Phase 2: WRITING PLANS         Phase 3: EXECUTE
┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│  需求探索 → 设计确认   │ ──► │  detail_plan →      │ ──► │  TDD 小步执行        │
│  产出 design.md      │       │  step_subplan →     │       │  Hook 自动读取当前步 │
│                      │       │  task_plan.md        │       │  自动更新状态        │
└─────────────────────┘       └─────────────────────┘       └─────────────────────┘
```

---

## 使用示例

### 示例一：待办网站（Todo-Web with Login）

**输入：**

```
我想要一个待办网站，有登录功能。
```

**自动发生的事：**

```
[plan-for-all] 检测到新项目，进入 Phase 1: BRAINSTORMING
```

```
Q1: 这个待办网站是给自己用还是给别人用？
  A: 个人使用 / B: 团队协作 / C: 公开访问
```

你选择后，AI 继续逐个提问（技术栈、数据存储、设计风格等），然后给出 2-3 个方案并推荐。

设计确认后，AI 将设计文档写入：
```
docs/plan-for-all/specs/YYYY-MM-DD-todo-web-design.md
```

你输入"开始规划"后，进入 Phase 2：

```
AI 创建 detail_plan.md，包含所有 Chunk（认证、数据库、前端组件等）
AI 对每个 Chunk 调用 step-decomposition skill
AI 汇总生成 task_plan.md
```

完成后你看到：

```
✅ 计划已就绪！

- docs/plan-for-all/specs/YYYY-MM-DD-todo-web-design.md
- docs/plan-for-all/plans/YYYY-MM-DD-todo-web-detail.md
- docs/plan-for-all/plans/step_subplans/step_subplan_phase1.md  (认证)
- docs/plan-for-all/plans/step_subplans/step_subplan_phase2.md  (待办 CRUD)
- task_plan.md  ← 统筹视图
- findings.md   ← 研究发现
- progress.md    ← 进度日志

说"开始执行"，我将通过 TDD 循环逐步实现。
```

你输入"开始执行"后，进入 Phase 3：

```
[plan-for-all] === 当前执行 Step ===
## Step 1.1: 配置 NextAuth + Google Provider

### TDD 循环
- [ ] RED: 写失败的测试
- [ ] GREEN: 运行测试验证失败
- [ ] GREEN: 写最小实现代码
- [ ] GREEN: 运行测试验证通过
- [ ] COMMIT: 提交
```

每当你执行 Bash/Edit/Write 操作时，Hook 自动读取当前 step 并显示。完成后更新 `task_plan.md` 状态，自动进入下一个 Step。

---

### 示例二：科学计算器

**输入：**

```
帮我规划一个科学计算器，支持三角函数、对数、阶乘。
```

**自动发生的事：**

```
Phase 1: AI 提问（精度要求？历史记录？界面风格？键盘布局？）
     → 产出设计文档

Phase 2: AI 生成 detail_plan.md
     Chunk 1: 基础运算（加减乘除、括号）
     Chunk 2: 科学函数（sin/cos/tan/log/ln）
     Chunk 3: 阶乘与特殊运算
     → 拆分为 step_subplan_phase1.md, step_subplan_phase2.md, step_subplan_phase3.md
     → 汇总到 task_plan.md

Phase 3: TDD 循环执行
     Step 1.1: 实现 Calculator 类骨架
     Step 1.2: 实现基础四则运算
     Step 1.3: 实现括号优先级处理
     Step 2.1: 实现三角函数
     ...
```

---

## 文件说明

| 文件 | 作用 |
|------|------|
| `task_plan.md` | 统筹视图 — 记录所有 Phase 和 Step 的状态 |
| `step_subplan_phaseN.md` | 执行文件 — 当前 Phase 的完整 TDD 步骤 |
| `detail_plan.md` | 存档文件 — 完整的原始实现计划 |
| `findings.md` | 研究发现 — 技术选型决策、参考资料 |
| `progress.md` | 进度日志 — 会话记录、错误记录 |

---

## Hook 自动化

Plan-For-All 通过 Hook 实现全程护航：

| 时机 | Hook | 自动化内容 |
|------|------|-----------|
| 会话开始 | `UserPromptSubmit` | 检测 task_plan.md 是否存在 |
| 读取文件时 | `PreToolUse` | 自动显示当前 task_plan.md 内容 |
| 执行操作前 | `PreToolUse` | 自动读取并显示当前 step_subplan |
| 写入 plan 后 | `PostToolUse` | 提示调用 step-decomposition |
| git commit 时 | `PostToolUse` | 自动记录到 progress.md |
| 会话结束 | `Stop` | 显示完成进度 |

---

## 计划并非完美

Plan-For-All 的计划基于设计文档和 AI 的推理生成，但在实际执行中总会遇到一些意想不到的小问题。这些小问题：

> 交由强大的 token 比较贵的 **ChatGPT 5.4x High** 和 **Claude Opus 4.6** 来修补即可。

Plan-For-All 负责的是 **大方向不迷失、小步不停歇**，具体的技术细节和边界情况处理交给更强大的模型完成。

---

## 安装与使用

在 Claude Code 中加载 plan-for-all skill：

将项目下载并解压，放置到 ~/.claude/skills 目录下面即可。

调用
```
/plan-for-all 需求
```

---

## 核心规则

| 规则 | 说明 |
|------|------|
| 先创建计划 | 永远不要在没有 task_plan.md 的情况下执行复杂任务 |
| 两步操作规则 | 每 2 次查看/搜索操作后，保存关键发现到文件 |
| 决策前先读 | 做重大决策前，读取计划文件 |
| 行动后更新 | 完成阶段后标记状态，记录错误 |
| 记录所有错误 | 在 progress.md 中记录错误和解决方案 |
| 三次失败协议 | 诊断修复 → 替代方案 → 重新思考 → 向用户求助 |

---

## 五问恢复测试

每次会话开始时，用这五个问题快速恢复上下文：

| 问题 | 答案来源 |
|------|---------|
| 我在哪里？ | `task_plan.md` 中当前 Phase + `step_subplan_*.md` |
| 我要去哪里？ | `task_plan.md` 剩余 Phase 列表 |
| 目标是什么？ | `task_plan.md` 的 Goal 声明 |
| 我学到了什么？ | `findings.md` |
| 我要做什么？ | 当前 `step_subplan_*.md` 的当前 TDD 步骤 |

---

## 致谢

Plan-For-All 的诞生离不开以下开源项目的启发：

- **[superpowers](https://github.com/Cluade-code/superpowers)** — 提供了强大的 brainstorming 和 writing-plans 技能体系，让需求探索和计划生成变得系统化
- **[planning-with-files](https://github.com/ClaudiaAI/Claudia)** — 提出的 Manus 思想——将计划写入磁盘、用文件持久化记忆——是 Plan-For-All 核心思想的来源

特别感谢 Manus 项目提出的核心理念：**把上下文留给真正重要的内容，计划交给磁盘。**
