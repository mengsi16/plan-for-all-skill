---
name: writing-plans
description: "将设计文档转化为可执行的实现计划 — 产出 detail_plan.md，自动触发 step-split.py 拆分为 task_plan.md"
---

# Writing Plans — 实现计划生成

将设计文档（spec）转化为详细的实现计划。

**前置条件：** 设计文档已保存在 `docs/plan-for-all/specs/YYYY-MM-DD-<feature>-design.md`

---

## 核心概念

| 文件 | 用途 |
|------|------|
| `detail_plan.md` | 完整存档，包含所有细节 |
| `step_subplan_*.md` | 按 Phase 拆分，执行时读取 |
| `task_plan.md` | 统筹视图，跟踪所有 Phase 和 Step |

---

## Step 1: 读取设计文档

读取 `docs/plan-for-all/specs/` 下的最新设计文档：
- 理解架构决策
- 识别需要构建的组件
- 确定技术栈

---

## Step 2: 创建 Detail Plan

```markdown
# [项目名称] 实现计划

**Goal:** [一句话目标]
**Architecture:** [2-3 句架构]
**Tech Stack:** [技术栈]

---

## Chunk 1: [Phase 1 名称]

### 组件/模块 1.1

**文件:**
- Create: `src/file.ts`
- Modify: `src/existing.ts:1-20`

**Step 1:** [具体操作，2-5 分钟]
**Step 2:** [具体操作]
...

### 组件/模块 1.2
...

## Chunk 2: [Phase 2 名称]
...
```

**保存到：** `docs/plan-for-all/plans/YYYY-MM-DD-<feature>-detail.md`

---

## Step 3: 子任务分解（Step Decomposition）

当 `detail_plan.md` 写入后，对每个 Chunk 调用 `step-decomposition` skill 进行智能分解：

1. 读取 `detail_plan.md` 中的所有 Chunk
2. 对每个 Chunk，使用 `step-decomposition` skill 生成 `step_subplan_phase{N}.md`
3. 汇总生成 `task_plan.md`

### 使用 step-decomposition skill

对每个 Chunk，填充 Few-Shot 模板：

```markdown
## 模块：[Chunk 名称]

[Chunk 的完整描述]

## 约束
- 每个 Step 耗时 2-5 分钟
- Step 必须可直接执行
- 包含 TDD 循环
```

模型将输出完整的 Step Subplan，保存到：
- `docs/plan-for-all/plans/step_subplans/step_subplan_phase{N}.md`

### 生成 task_plan.md

汇总所有 Phase 和 Step 的元信息，生成统筹视图：

---

## Step 4: 生成辅助文件

创建 `findings.md` 和 `progress.md`：

**findings.md:**
```markdown
# Findings - [项目名称]

## 设计决策
1. [决策点]: [选择] - [原因]
2. ...

## 技术参考
- [技术 A]: 用于 X
- [技术 B]: 用于 Y
```

**progress.md:**
```markdown
# Progress - [项目名称]

## YYYY-MM-DD

### 规划阶段
- [x] 完成设计文档
- [x] 完成实现计划
```

---

## Step 5: 等待用户确认

> "计划已生成并保存到 `task_plan.md`。
>
> 文件结构：
> - `docs/plan-for-all/specs/` — 设计文档
> - `docs/plan-for-all/plans/` — 实现计划详情
> - `task_plan.md` — 统筹视图
> - `findings.md` — 研究发现
> - `progress.md` — 进度日志
>
> 说"开始执行"我将通过 TDD 循环逐步实现。"
>


## 与执行阶段的衔接

用户说"开始执行"后：

```
task_plan.md (已创建)
    ↓
EXECUTE Phase (TDD 循环)
    ↓
Hook: PreToolUse → 读取当前 step_subplan
Hook: PostToolUse → 更新 task_plan.md
```

---

## Detail Plan 结构规范

### Header (必需)

```markdown
# [Feature] 实现计划

**Goal:** [一句话]
**Architecture:** [架构描述]
**Tech Stack:** [技术栈]
```

### Chunk 分隔

使用 `## Chunk N: [Phase 名称]` 分隔每个 Phase。
每个 Chunk 包含该 Phase 的所有组件和步骤。

### Step 粒度

每个 Step 应该是 2-5 分钟的操作：
- "创建 X 文件"
- "实现 Y 函数"
- "添加 Z 测试"

### TDD 嵌入（可选）

如果使用 TDD，在 Step 中嵌入：

```markdown
- [ ] **RED:** 写失败的测试
- [ ] **GREEN:** 实现最小代码
- [ ] **REFACTOR:** 清理代码
```
