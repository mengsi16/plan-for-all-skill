---
name: plan-for-all
description: |
  自包含的项目规划技能，包含三个阶段：
  1. Brainstorming — 需求探索与设计
  2. Writing Plans — 计划生成
  3. Execute — TDD 驱动执行 + Hook 护航
  支持文件持久化、上下文恢复、多步骤任务跟踪。
user-invocable: true
allowed-tools: "Read, Write, Edit, Bash, Glob, Grep, TaskCreate, TaskUpdate, Agent"
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: "if [ -f task_plan.md ]; then echo '[plan-for-all] 检测到活跃计划。请读取 task_plan.md、progress.md 和 findings.md 恢复上下文。'; fi"
  PreToolUse:
    - matcher: "Read|Glob|Grep"
      hooks:
        - type: command
          command: "if [ -f task_plan.md ]; then echo '[plan-for-all] === 当前 task_plan.md ==='; cat task_plan.md 2>/dev/null | head -60; fi"
    - matcher: "Bash|Edit|Write"
      hooks:
        - type: command
          command: |
            if grep -q 'in_progress' task_plan.md 2>/dev/null; then
              CURRENT_SUBPLAN=$(grep -A2 'in_progress' task_plan.md | grep 'step_subplan' | head -1 | sed 's/.*[\(\)\[\]]*\([step_subplan^]*\)[\)\]\`].*/\1/' | tr -d '`');
              if [ -n "$CURRENT_SUBPLAN" ] && [ -f "$CURRENT_SUBPLAN" ]; then
                echo '[plan-for-all] === 当前执行 Step ===';
                cat "$CURRENT_SUBPLAN" 2>/dev/null | head -80;
              else
                echo '[plan-for-all] === 当前 task_plan.md 状态 ===';
                grep -B2 -A5 'in_progress' task_plan.md 2>/dev/null;
              fi
            fi
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: |
            if echo "$FILE" 2>/dev/null | grep -q "docs/plan-for-all/plans/.*detail.md$"; then
              echo '[plan-for-all] 检测到 detail plan 已更新';
              echo '[plan-for-all] 请对每个 Phase 调用 step-decomposition skill 提取 step_subplan';
              echo '[plan-for-all] 然后汇总生成 task_plan.md';
            fi
            if [ -f task_plan.md ]; then
              echo '[plan-for-all] task_plan.md 已更新，请更新 progress.md 记录本次操作';
            fi
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            if echo "$CURRENT_COMMAND" 2>/dev/null | grep -q "git commit"; then
              DATE=$(date '+%Y-%m-%d %H:%M');
              echo -e "\n## $DATE - 提交完成" >> progress.md;
              echo '```bash' >> progress.md;
              echo "$CURRENT_COMMAND" >> progress.md 2>/dev/null || true;
              echo '```' >> progress.md;
            fi
  Stop:
    - hooks:
        - type: command
          command: |
            SD="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/superpowers/5.0.2/skills/step-planning/scripts}";
            if [ -f "task_plan.md" ]; then
              echo '[plan-for-all] 会话即将结束，检查任务完成状态...';
              COMPLETE=$(grep -c '\[x\]' task_plan.md 2>/dev/null || echo 0);
              TOTAL=$(grep -c '\- \[' task_plan.md 2>/dev/null || echo 0);
              echo "进度: $COMPLETE / $TOTAL 个 Step 完成";
              if [ "$COMPLETE" = "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
                echo '[plan-for-all] 所有 Step 已完成！';
              fi
            fi
---

# Plan-For-All — 自包含项目规划系统

像 Manus 一样用文件持久化记忆，像 TDD 一样用小步执行。

## 三大阶段

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: BRAINSTORMING                                 │
│  需求探索 → 逐个提问 → 方案推荐 → 设计确认                 │
│  产出: docs/plan-for-all/specs/YYYY-MM-DD-*-design.md   │
│  技能: skills/brainstorming/SKILL.md                    │
├─────────────────────────────────────────────────────────┤
│  Phase 2: WRITING PLANS                                 │
│  设计文档 → detail_plan.md → step_decomposition → task_plan.md
│  产出: task_plan.md, findings.md, progress.md           │
│  技能: skills/writing-plans/SKILL.md                    │
├─────────────────────────────────────────────────────────┤
│  Phase 3: EXECUTE                                       │
│  TDD RED-GREEN-REFACTOR → Hook 护航 → 逐步完成           │
│  PreToolUse Hook → 自动读取当前 step                     │
│  PostToolUse Hook → 自动更新状态                         │
└─────────────────────────────────────────────────────────┘
```

---

## 第一步：检查上下文

**每次会话开始时**，检查是否存在 `task_plan.md`：

```bash
if [ -f task_plan.md ]; then
  # 读取规划文件恢复上下文
  cat task_plan.md
  cat findings.md
  cat progress.md
fi
```

根据是否有 `task_plan.md` 决定进入哪个阶段：
- **无 task_plan.md** → Phase 1 (Brainstorming)
- **有 task_plan.md，无 in_progress** → Phase 2 (Writing Plans) 或等待用户说"开始执行"
- **有 task_plan.md，有 in_progress** → Phase 3 (Execute)

---

## Phase 1: Brainstorming

**触发词：** "设计一个 X"、"规划一个项目"、"帮我梳理需求"

**执行：**
1. 读取 `skills/brainstorming/SKILL.md` 获取详细流程
2. 检查项目上下文（现有文件、git 历史）
3. 逐个提问收敛需求
4. 提出 2-3 个方案并推荐
5. 呈现设计方案，获得用户分步批准
6. 将设计文档写入 `docs/plan-for-all/specs/YYYY-MM-DD-<feature>-design.md`
7. 完成后提示用户进入 Planning 阶段

**产出：**
- `docs/plan-for-all/specs/YYYY-MM-DD-<feature>-design.md`

---

## Phase 2: Writing Plans

**触发词：** "开始规划"、"写计划"、"制定实现方案"

**执行：**
1. 读取 `skills/writing-plans/SKILL.md` 获取详细流程
2. 读取设计文档
3. 创建 `detail_plan.md`（完整实现计划）
4. 对每个 Phase 调用 `step-decomposition` skill 提取 `step_subplan_*.md`，汇总生成 `task_plan.md`
5. 创建 `findings.md` 和 `progress.md`
6. 告知用户计划已就绪，等待"开始执行"

**产出：**
- `docs/plan-for-all/plans/YYYY-MM-DD-<feature>-detail.md`
- `docs/plan-for-all/plans/step_subplans/step_subplan_phase*.md`
- `task_plan.md`
- `findings.md`
- `progress.md`

---

## Phase 3: Execute

**触发词：** "开始执行"、"开始写代码"、"开始实现"

**执行：**
1. 读取 `task_plan.md` 找到 `in_progress` 的 Phase
2. 读取对应的 `step_subplan_*.md`
3. 按 TDD 循环执行每个 Step：
   - **RED**: 写一个失败的测试
   - **GREEN**: 实现最小代码让测试通过
   - **REFACTOR**: 清理代码
   - 提交（可选）
4. Step 完成后，更新 `task_plan.md` 状态
5. 重复直到所有 Phase 完成

**Hook 机制：**
- **PreToolUse Hook**: 每次执行 Bash/Edit/Write 前，自动读取当前 step_subplan
- **PostToolUse Hook**: 每次写入后，自动提示更新 task_plan.md

---

## 文件结构

```
project/
├── task_plan.md              # 统筹视图（Hook 自动读取）
├── findings.md               # 研究发现
├── progress.md               # 进度日志
├── docs/
│   └── plan-for-all/
│       ├── specs/            # 设计文档
│       │   └── YYYY-MM-DD-*-design.md
│       └── plans/            # 实现计划
│           ├── YYYY-MM-DD-*-detail.md
│           └── step_subplans/
│               └── step_subplan_phase*.md
└── [项目代码文件]
```

---

## 五问恢复测试

| 问题 | 答案来源 |
|------|---------|
| 我在哪里？ | `task_plan.md` 中的当前 Phase + `step_subplan_*.md` |
| 我要去哪里？ | `task_plan.md` 剩余 Phase 列表 |
| 目标是什么？ | `task_plan.md` 的 Goal 声明 |
| 我学到了什么？ | `findings.md` |
| 我要做什么？ | 当前 `step_subplan_*.md` 的当前 Step |

---

## 核心规则

| 规则 | 说明 |
|------|------|
| 先创建计划 | 永远不要在没有 `task_plan.md` 的情况下执行复杂任务 |
| 两步操作规则 | 每 2 次查看/搜索操作后，保存关键发现到文件 |
| 决策前先读 | 做重大决策前，读取计划文件 |
| 行动后更新 | 完成阶段后标记状态，记录错误 |
| 记录所有错误 | 在 `progress.md` 中记录错误和解决方案 |
| 永不重复失败 | 失败后换方案，不重复同样的失败操作 |

---

## 三次失败协议

```
第1次: 诊断并修复
第2次: 替代方案
第3次: 重新思考
3次后: 向用户求助
```

---

## Skill 结构

```
plan-for-all/
├── SKILL.md                  # 本文件（主技能入口）
├── skills/
│   ├── brainstorming/        # 需求探索阶段
│   │   └── SKILL.md
│   ├── writing-plans/       # 计划生成阶段
│   │   └── SKILL.md
│   └── step-decomposition/  # 子任务分解（LLM 提取 step_subplan）
│       └── SKILL.md
├── scripts/
│   └── session-catchup.py    # 会话恢复
└── templates/
    ├── task_plan.md
    ├── step_subplan.md
    ├── findings.md
    └── progress.md
```
