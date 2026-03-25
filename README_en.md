<div align="center">

# Plan-For-All

*Persist memory to disk like Manus, execute in small steps like TDD.*

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.com/claude-code)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Claude-Code-Skill** | **Manus-Style** | **MIT License** | **TDD-Driven** | **Hook-Powered** | **Disk-Persistent**

</div>

---

<div align="center">

**🌐 Language / 语言**

[English](README_en.md) | [简体中文](README.md)

</div>

---

## Pain Points

Have you experienced these frustrating moments?

| Scenario | Result |
|----------|--------|
| Claude Code Plan Mode context gets compressed | All your carefully gathered requirements are lost, ToDos never get completed |
| brainstorming + writing-plans output massive plans | Overwhelming context causes Claude Code to fall back to default tool calls, forgetting your specified skills |
| Long task interrupted mid-session | When you return, you have no idea where you left off — everything from scratch |

**Plan-For-All** draws from the planning-with-files (Manus philosophy) — writing plans to disk to prevent plan loss from context compression. It also draws from superpowers' requirements design and step-decomposition concepts, actually implementing them as small files (step_subplan) to prevent massive content from flooding the context.

---

## Core Philosophy

Plan-For-All breaks large plans into small chunks, uses `task_plan.md` as the master view, and automatically loads small plans as each phase progresses. This keeps **the plan always up-to-date** and **context always clean**.

```
┌────────────────────────────────────────────────────────────┐
│  Traditional: Everything in context → Compressed/Lost      │
│  Plan-For-All: Plans to disk → Load on demand → Clean     │
└────────────────────────────────────────────────────────────┘
```

---

## Workflow

```
Phase 1: BRAINSTORMING          Phase 2: WRITING PLANS         Phase 3: EXECUTE
┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│  Explore → Approve  │ ──► │  detail_plan →      │ ──► │  TDD small steps    │
│  design.md output   │       │  step_subplan →     │       │  Hook auto-reads    │
│                      │       │  task_plan.md        │       │  auto-updates state  │
└─────────────────────┘       └─────────────────────┘       └─────────────────────┘
```

---

## Usage Examples

### Example 1: Todo-Web with Login

**Input:**

```
I want a todo website with login functionality.
```

**What happens automatically:**

```
[plan-for-all] New project detected, entering Phase 1: BRAINSTORMING
```

```
Q1: Is this todo website for yourself or for others?
  A: Personal use / B: Team collaboration / C: Public access
```

After your selection, AI continues asking questions one by one (tech stack, data storage, design style, etc.), then presents 2-3 options with a recommendation.

After design approval, AI writes the design document to:
```
docs/plan-for-all/specs/YYYY-MM-DD-todo-web-design.md
```

When you type "start planning", Phase 2 begins:

```
AI creates detail_plan.md with all Chunks (auth, database, frontend components, etc.)
AI calls step-decomposition skill for each Chunk
AI generates task_plan.md
```

After completion you see:

```
✅ Plan ready!

- docs/plan-for-all/specs/YYYY-MM-DD-todo-web-design.md
- docs/plan-for-all/plans/YYYY-MM-DD-todo-web-detail.md
- docs/plan-for-all/plans/step_subplans/step_subplan_phase1.md  (Auth)
- docs/plan-for-all/plans/step_subplans/step_subplan_phase2.md  (Todo CRUD)
- task_plan.md  ← Master view
- findings.md   ← Research findings
- progress.md    ← Progress log

Type "start executing" and I'll implement step by step via TDD.
```

When you type "start executing", Phase 3 begins:

```
[plan-for-all] === Current Step ===
## Step 1.1: Configure NextAuth + Google Provider

### TDD Loop
- [ ] RED: Write a failing test
- [ ] GREEN: Run test to verify failure
- [ ] GREEN: Write minimal implementation
- [ ] GREEN: Run test to verify pass
- [ ] COMMIT: Commit
```

Every time you execute Bash/Edit/Write, the Hook automatically loads and displays the current step. After completion, it updates `task_plan.md` and moves to the next Step.

---

### Example 2: Scientific Calculator

**Input:**

```
Help me plan a scientific calculator with trigonometric functions, logarithms, and factorial.
```

**What happens automatically:**

```
Phase 1: AI asks questions (precision? history? UI style? keyboard layout?)
     → Design document output

Phase 2: AI generates detail_plan.md
     Chunk 1: Basic operations (add/subtract/multiply/divide, parentheses)
     Chunk 2: Scientific functions (sin/cos/tan/log/ln)
     Chunk 3: Factorial and special operations
     → Split into step_subplan_phase1.md, step_subplan_phase2.md, step_subplan_phase3.md
     → Aggregated into task_plan.md

Phase 3: TDD loop execution
     Step 1.1: Implement Calculator class skeleton
     Step 1.2: Implement basic arithmetic
     Step 1.3: Implement parentheses priority handling
     Step 2.1: Implement trigonometric functions
     ...
```

---

## File Overview

| File | Purpose |
|------|---------|
| `task_plan.md` | Master view — tracks all Phase and Step statuses |
| `step_subplan_phaseN.md` | Execution file — complete TDD steps for current Phase |
| `detail_plan.md` | Archive file — complete original implementation plan |
| `findings.md` | Research findings — tech decisions, references |
| `progress.md` | Progress log — session records, error records |

---

## Hook Automation

Plan-For-All uses Hooks for full-session protection:

| Timing | Hook | Automation |
|--------|------|------------|
| Session start | `UserPromptSubmit` | Detect if task_plan.md exists |
| When reading files | `PreToolUse` | Auto-display current task_plan.md |
| Before execution | `PreToolUse` | Auto-load and display current step_subplan |
| After plan write | `PostToolUse` | Prompt to call step-decomposition |
| On git commit | `PostToolUse` | Auto-record to progress.md |
| Session end | `Stop` | Show completion progress |

---

## Plans Are Not Perfect

Plan-For-All's plans are generated based on design documents and AI reasoning, but unexpected issues always arise during actual execution. These minor issues:

> Can be handled by the more powerful (and expensive) **ChatGPT 5.4x High** and **Claude Opus 4.6**.

Plan-For-All is responsible for **never losing direction, never stopping in small steps** — specific technical details and edge cases can be handed off to more powerful models.

---

## Installation & Usage

Load plan-for-all skill in Claude Code:

Download and extract the project, place it in the ~/.claude/skills directory.

Invoke with:
```
/plan-for-all prompt
```

---

## Core Rules

| Rule | Description |
|------|-------------|
| Create plan first | Never execute complex tasks without task_plan.md |
| Two-step rule | After every 2 read/search operations, save key findings to file |
| Read before decisions | Read plan files before making major decisions |
| Update after action | Mark status after completing phases, record errors |
| Record all errors | Log errors and solutions in progress.md |
| Three-failure protocol | Diagnose → Alternative approach → Rethink → Ask user |

---

## Five-Question Recovery Test

At the start of each session, quickly recover context using these five questions:

| Question | Answer Source |
|----------|---------------|
| Where am I? | Current Phase in `task_plan.md` + `step_subplan_*.md` |
| Where am I going? | Remaining Phase list in `task_plan.md` |
| What's the goal? | Goal declaration in `task_plan.md` |
| What have I learned? | `findings.md` |
| What do I do next? | Current TDD step in `step_subplan_*.md` |

---

## Acknowledgments

Plan-For-All was made possible by these open source projects:

- **[superpowers](https://github.com/Cluade-code/superpowers)** — Provided the powerful brainstorming and writing-plans skill system, making requirements exploration and plan generation systematic
- **[planning-with-files](https://github.com/ClaudiaAI/Claudia)** — The Manus philosophy — persisting plans to disk — is the source of Plan-For-All's core philosophy

Special thanks to the Manus project for its core insight: **keep context for what really matters, let disk handle the plan.**

