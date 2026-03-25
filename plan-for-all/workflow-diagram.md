# Plan-For-All 完整工作流程

## 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Plan-For-All 三阶段                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐         │
│  │     Phase 1          │     │     Phase 2           │     │     Phase 3          │         │
│  │   BRAINSTORMING      │ ──► │   WRITING PLANS      │ ──► │   EXECUTE            │         │
│  │                      │     │                      │     │                      │         │
│  │  需求探索 → 设计确认    │     │  detail_plan → step_subplan │     │  TDD RED-GREEN-REFACTOR │
│  │  产出 design.md       │     │  → task_plan.md       │     │  Hook 护航执行        │         │
│  └──────────────────────┘     └──────────────────────┘     └──────────────────────┘         │
│                                                                             │
│         ↑                            ↑                            ↑                      │
│         │                            │                            │                      │
│  task_plan.md 不存在      task_plan.md 已创建            task_plan.md 中                  │
│         │                      无 in_progress              有 in_progress                 │
│         │                            │                            │                      │
└─────────┴────────────────────────────┴────────────────────────────┴──────────────────────┘
```

---

## 会话上下文恢复（每次会话开始）

```
新会话开始
    │
    ▼
┌──────────────────────┐
│ 检查 task_plan.md    │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
   存在        不存在
     │           │
     ▼           ▼
┌────────────┐ ┌──────────────────────┐
│ 读取       │ │ Phase 1              │
│ task_plan  │ │ BRAINSTORMING        │
│ + findings │ │ (正常规划流程)         │
│ + progress │ └──────────────────────┘
│            │
│ ↓ 检查 in_progress 状态
│   ├─ 无 → Phase 2 WRITING PLANS
│   └─ 有 → Phase 3 EXECUTE
└────────────┘
```

---

## Phase 1: BRAINSTORMING 需求探索

```
用户触发: "设计一个 X"、"规划一个项目"、"帮我梳理需求"
    │
    ▼
┌──────────────────────────┐
│ Step 1: 检查项目上下文     │
│ - 读取 task_plan.md       │
│ - 读取 findings.md        │
│ - 读取 progress.md        │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Step 2: 逐个提问收敛需求   │
│ (一次一问，多选优先)        │
│                          │
│ 维度:                     │
│ 1. 产品定位 (C端/B端)      │
│ 2. 核心功能               │
│ 3. 用户交互               │
│ 4. 数据需求               │
│ 5. 技术偏好               │
│ 6. 设计风格               │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Step 3: 提出方案 (2-3个)  │
│ - 每个方案说明适用场景     │
│ - 推荐最优方案            │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Step 4: 分 Section 批准   │
│ - 架构 → 核心组件 → 数据流  │
│ - 技术选型 → 设计风格      │
│ (每个 section 获批后继续)  │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Step 5: 写入设计文档       │
│                          │
│ docs/plan-for-all/specs/ │
│ YYYY-MM-DD-<feature>-   │
│ design.md                │
└──────────┬───────────────┘
           │
           ▼
    过渡到 Phase 2
    WRITING PLANS
```

**产出：**
- `docs/plan-for-all/specs/YYYY-MM-DD-<feature>-design.md`

---

## Phase 2: WRITING PLANS 计划生成

```
读取设计文档
docs/plan-for-all/specs/YYYY-MM-DD-<feature>-design.md
    │
    ▼
┌──────────────────────────┐
│ Step 1: 创建 Detail Plan │
│                          │
│ docs/plan-for-all/plans/ │
│ YYYY-MM-DD-<feature>-    │
│ detail.md                │
│                          │
│ 结构:                    │
│ ## Chunk N: [Phase名]    │
│ ### 组件/模块 N.X        │
│ **文件:** Create/Modify   │
│ **Step:** [2-5分钟操作]   │
└──────────┬───────────────┘
           │
           ▼ 【Hook: PostToolUse 检测到 detail plan 写入】
    ┌─────────────────────────────────────┐
    │ 调用 step-decomposition skill        │
    │ 对每个 Chunk 生成 step_subplan       │
    └───────────────┬─────────────────────┘
                    │
    ┌───────────────┴───────────────┐
    ▼                               ▼
┌──────────────────┐   ┌──────────────────┐
│ step_subplan_    │   │ step_subplan_    │
│ phase1.md        │   │ phase2.md        │
└──────────┬───────┘   └──────────┬───────┘
           │                      │
           └──────────┬───────────┘
                      ▼
┌──────────────────────────────────────────┐
│ Step 2: 生成 task_plan.md (统筹视图)       │
│                                          │
│ - Phase 列表 + 对应 step_subplan 引用      │
│ - 每个 Phase 的 Step 清单                 │
│ - 状态追踪: [ ] pending / [→] in_progress │
│ - 错误记录表                              │
│ - 关键问题 / 已做决策                      │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Step 3: 生成 findings.md (研究发现)        │
│ - 设计决策表                              │
│ - 技术参考                               │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Step 4: 生成 progress.md (进度日志)       │
│ - 会话记录                               │
│ - 规划阶段完成标记                        │
└──────────┬───────────────────────────────┘
           │
           ▼
    告知用户计划已就绪
    等待"开始执行"
```

**产出：**
- `docs/plan-for-all/plans/YYYY-MM-DD-<feature>-detail.md`
- `docs/plan-for-all/plans/step_subplans/step_subplan_phase*.md`
- `task_plan.md`
- `findings.md`
- `progress.md`

---

## Phase 3: EXECUTE 执行阶段

```
用户说"开始执行"或"继续"
    │
    ▼
┌──────────────────────────────────────────┐
│ Hook: PreToolUse (Bash|Edit|Write)       │
│ 读取当前 task_plan.md                    │
│ 找到 in_progress 的 Phase                │
│ 显示当前 Step 概要                        │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ 自动读取当前 step_subplan_*.md            │
│ (Hook: 每次执行前读取当前 step 详情)        │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ 按 step_subplan 执行 TDD 循环            │
│                                          │
│ Step A: [ ] RED - 写失败的测试            │
│     │                                    │
│     ▼                                    │
│ Step B: [ ] GREEN - 运行验证测试失败      │
│     │                                    │
│     ▼                                    │
│ Step C: [ ] GREEN - 写最小实现代码        │
│     │                                    │
│     ▼                                    │
│ Step D: [ ] GREEN - 运行验证测试通过      │
│     │                                    │
│     ▼                                    │
│ Step E: [ ] REFACTOR - 清理代码          │
│     │                                    │
│     ▼                                    │
│ Step F: [ ] COMMIT - 提交                │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Hook: PostToolUse (Write/Edit)           │
│ 更新 progress.md 记录本次操作             │
│ 检查当前 step 是否完成                     │
└──────────┬───────────────────────────────┘
           │
      ┌────┴────┐
      ▼         ▼
   完成      未完成
      │         │
      ▼         ▼
 更新      当前 step
 task_plan  继续执行
 .md 状态
      │
      ▼
┌──────────────────┐
│ 所有 Phase 完成？ │
└────────┬─────────┘
    YES  │ NO
   ┌─────┴──────┐
   ▼           ▼
 任务完成   读取下一个
          step_subplan
```

---

## Hook 触发矩阵

| 阶段 | Hook 类型 | 触发条件 | 动作 |
|------|----------|---------|------|
| 通用 | `UserPromptSubmit` | 会话开始 | 检测 task_plan.md 存在则提示恢复上下文 |
| 通用 | `PreToolUse` (Read\|Glob\|Grep) | task_plan.md 存在 | 显示当前 task_plan.md 内容 (前60行) |
| 执行 | `PreToolUse` (Bash\|Edit\|Write) | task_plan 有 in_progress | 读取并显示当前 step_subplan 内容 |
| 规划 | `PostToolUse` (Write\|Edit) | 检测到 detail plan | 提示调用 step-decomposition skill |
| 规划 | `PostToolUse` (Write\|Edit) | task_plan 更新 | 提示更新 progress.md |
| 执行 | `PostToolUse` (Bash) | git commit | 记录提交到 progress.md |
| 停止 | `Stop` | 会话结束 | 显示完成进度: $COMPLETE / $TOTAL |

---

## 三级规划对应关系

| 层级 | 文件 | 粒度 | 产出阶段 |
|------|------|------|---------|
| L1 统筹 | `task_plan.md` | Phase/Step 级 | Writing Plans |
| L2 执行 | `step_subplan_phase*.md` | 2-5分钟 TDD 步 | Writing Plans (step-decomposition) |
| L3 细节 | `detail_plan.md` | 完整代码/命令 | Writing Plans |

---

## 文件结构

```
project/
├── task_plan.md                      ← 统筹视图（Hook 自动读取）
├── findings.md                       ← 研究发现
├── progress.md                       ← 会话日志
│
└── docs/plan-for-all/
    ├── specs/                        ← 设计文档 (Phase 1)
    │   └── YYYY-MM-DD-<feature>-design.md
    │
    └── plans/                        ← 实现计划 (Phase 2)
        ├── YYYY-MM-DD-<feature>-detail.md
        │
        └── step_subplans/            ← 自动拆分的执行文件
            ├── step_subplan_phase1.md
            ├── step_subplan_phase2.md
            └── ...
```

---

## 关键 Hook 伪代码

### 1. 会话开始：检测上下文

```yaml
UserPromptSubmit:
  hooks:
    - type: command
      command: |
        if [ -f task_plan.md ]; then
          echo '[plan-for-all] 检测到活跃计划。请读取 task_plan.md、progress.md 和 findings.md 恢复上下文。';
        fi
```

### 2. 执行前：读取当前 step

```yaml
PreToolUse:
  matcher: "Bash|Edit|Write"
  condition: "task_plan.md 存在且有 in_progress 状态"
  hooks:
    - type: command
      command: |
        if grep -q 'in_progress' task_plan.md; then
          CURRENT_SUBPLAN=$(grep -A2 'in_progress' task_plan.md | grep 'step_subplan' | ...);
          if [ -n "$CURRENT_SUBPLAN" ] && [ -f "$CURRENT_SUBPLAN" ]; then
            echo '[plan-for-all] === 当前执行 Step ===';
            cat "$CURRENT_SUBPLAN";
          fi
        fi
```

### 3. 规划后：触发 step-decomposition

```yaml
PostToolUse:
  matcher: "Write|Edit"
  condition: "文件名匹配 docs/plan-for-all/plans/.*detail.md$"
  hooks:
    - type: command
      command: |
        echo '[plan-for-all] 检测到 detail plan 已更新';
        echo '[plan-for-all] 请对每个 Phase 调用 step-decomposition skill 提取 step_subplan';
        echo '[plan-for-all] 然后汇总生成 task_plan.md';
```

### 4. 会话停止：显示完成进度

```yaml
Stop:
  hooks:
    - type: command
      command: |
        if [ -f task_plan.md ]; then
          COMPLETE=$(grep -c '\[x\]' task_plan.md);
          TOTAL=$(grep -c '\- \[' task_plan.md);
          echo "进度: $COMPLETE / $TOTAL 个 Step 完成";
        fi
```

---

## 五问恢复测试

| 问题 | 答案来源 |
|------|---------|
| 我在哪里？ | `task_plan.md` 中的当前 Phase + 对应 `step_subplan_*.md` |
| 我要去哪里？ | `task_plan.md` 剩余 Phase 列表 |
| 目标是什么？ | `task_plan.md` 的 Goal 声明 |
| 我学到了什么？ | `findings.md` |
| 我要做什么？ | 当前 `step_subplan_*.md` 的当前 Step 的 TDD 步骤 |

---

## 核心规则

| 规则 | 说明 |
|------|------|
| 先创建计划 | 永远不要在没有 `task_plan.md` 的情况下执行复杂任务 |
| 两步操作规则 | 每 2 次查看/搜索操作后，保存关键发现到文件 |
| 决策前先读 | 做重大决策前，读取计划文件 |
| 行动后更新 | 完成阶段后标记状态，记录错误 |
| 记录所有错误 | 在 `progress.md` 中记录错误和解决方案 |
| 三次失败协议 | 第1次: 诊断修复 / 第2次: 替代方案 / 第3次: 重新思考 / 3次后: 向用户求助 |

---

## Skill 结构

```
plan-for-all/
├── SKILL.md                      ← 主技能入口 (plan-for-all)
├── skills/
│   ├── brainstorming/            ← Phase 1: 需求探索
│   │   └── SKILL.md
│   ├── writing-plans/            ← Phase 2: 计划生成
│   │   └── SKILL.md
│   └── step-decomposition/       ← Phase 2: 子任务分解
│       └── SKILL.md
├── templates/
│   ├── task_plan.md
│   ├── step_subplan.md
│   ├── findings.md
│   └── progress.md
└── scripts/
    └── session-catchup.py       ← 会话恢复脚本
```
