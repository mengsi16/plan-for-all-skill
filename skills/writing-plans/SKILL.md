---
name: writing-plans
description: Use when an approved design contract must be converted into an executable implementation plan with smoke checks, verification steps, and persistent status files.
---

# Writing Plans

Convert an approved design contract into an executable plan.

A plan is not a code dump. Its job is to define behavior, boundaries, checkpoints, and verification so execution does not depend on hidden assumptions.

## Required Inputs

Before writing the plan, confirm you have:
- an approved design doc in `docs/plan-for-all/specs/`
- UI refinement outputs when the design includes UI work
- `docs/plan-for-all/specs/YYYY-MM-DD-<topic>-ui-spec.md` when UI work exists
- explicit goals and non-goals
- acceptance criteria
- known risks or open questions

If these are missing, return to brainstorming.

If UI work exists but refinement outputs are missing, run `skills/ui-ux-pro-max/SKILL.md` first under brainstorming supervision.

### UI Refinement Hard Gate

When the approved design includes UI work, do not start detail planning until `docs/plan-for-all/specs/YYYY-MM-DD-<topic>-ui-spec.md` exists and is reviewable.

Prefer generating this file from `templates/ui_refinement_spec.md`.

The UI spec must include at least:
- information architecture and page/screen structure
- key user flows
- component inventory and interaction-state matrix
- visual direction and design tokens
- responsive/breakpoint strategy
- accessibility and motion constraints

If this file is missing or incomplete, return to brainstorming and complete UI refinement first.

## Required Outputs

Planning must produce:
- `docs/plan-for-all/plans/YYYY-MM-DD-<topic>-detail.md`
- `docs/plan-for-all/plans/step_subplans/step_subplan_phase*.md`
- `docs/plan-for-all/task_plan.md`
- `docs/plan-for-all/findings.md`
- `docs/plan-for-all/progress.md`

When UI work exists, planning must also reference:
- `docs/plan-for-all/specs/YYYY-MM-DD-<topic>-ui-spec.md`

## Planning Principles

- **Smoke test first**: every non-trivial plan starts by proving the current baseline
- **Behavior before implementation**: define expected behavior and verification before code steps
- **Exact file paths**: file ownership must be explicit
- **Small executable steps**: each step should be concrete and bounded
- **No speculative bulk code**: include code only when a tiny snippet clarifies an interface or test shape
- **Status honesty**: initialize tracking files without fake completion claims
- **Knowledge before dependence**: if the plan depends on an external term or claim, verify it before relying on it

## Step 0: Technical Knowledge Audit Hard Gate

Use `skills/tech-knowledge-audit/SKILL.md` before planning relies on any unstable or unfamiliar knowledge.

This is not permission to defer all audit work until planning. If brainstorming, decomposition, or execution already depends on unresolved external technical meaning, audit must happen there before the workflow continues.

Planning must also inherit and re-check any `stale_recheck_required` items from earlier stages before relying on them.

Mandatory audit targets include:
- version-sensitive frameworks or libraries
- provider or protocol behavior that may have changed
- APIs with compatibility uncertainty
- unfamiliar terminology or architecture names
- high-risk terminology with likely semantic drift or recent ecosystem-specific meaning
- recent engineering patterns or agent paradigms that may not be captured by older model knowledge

### Hard Gate Rule

Do not continue to the detail plan while any mandatory audit item is unresolved.

If an item is still unresolved after checking the best available sources:
- record it in `docs/plan-for-all/findings.md`
- add it to `docs/plan-for-all/task_plan.md` blockers or open questions
- constrain the plan around that uncertainty or stop and ask the user

Planning may continue only when each mandatory item is either:
- `verified_recent`
- `verified_official`
- `project_specific_ask_user`
- explicitly recorded as unresolved with visible planning impact and blocker status

Do not use tech audit as a substitute for architecture thinking.

## Step 1: Classify The Work

Identify which planning mode applies:

### Greenfield
Use when building a new feature or project.

Plan must include:
- bootstrap or baseline smoke check
- first user-visible behavior
- vertical slices over horizontal layers when possible

### Bugfix
Use when behavior is broken or suspected broken.

Plan must include:
- minimal reproduction or smoke check
- root-cause investigation step
- failing regression test before implementation

### Refactor
Use when changing structure while preserving behavior.

Plan must include:
- behavior-preservation checks
- safety rails and rollback points
- explicit proof that external behavior stays stable

## Step 2: Build The Detail Plan

Save to `docs/plan-for-all/plans/YYYY-MM-DD-<topic>-detail.md`.

Use this structure:

```markdown
# [Topic] Implementation Plan

> Required Skill: Invoke `plan-for-all:test-driven-development` before executing the detailed steps below.

**Goal:** [One sentence]
**Mode:** [Greenfield | Bugfix | Refactor]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]

---

## Contract Summary
- Goals:
- Non-goals:
- Acceptance criteria:
- UI refinement constraints (required when UI work exists):
- UI spec path (required when UI work exists):
- Open questions / risks:
- Verified terminology / external assumptions:

## Phase 1: [Name]

**Objective:**
**Why now:**
**Files:**
- Create:
- Modify:
- Test:

### Smoke Check
Run: `[command]`
Expected: `[baseline behavior or failure]`

### Steps
1. [Action]
2. [Action]
3. [Verification]

### Exit Criteria
- [observable condition]

## Phase 2: [Name]
...
```

## What A Good Phase Contains

Each phase should include:
- objective
- files in scope
- smoke check or baseline verification
- ordered steps
- verification command(s)
- exit criteria
- known risk if applicable

The detail plan itself must begin with the required `plan-for-all:test-driven-development` skill banner so execution starts under an explicit TDD contract instead of relying on later reminders.

Each step should be one action, for example:
- add a failing test for unauthorized access
- run the targeted test and confirm it fails for the expected reason
- implement the minimal auth branch
- rerun the targeted test
- run the phase smoke check

## What Must Not Go Into The Plan

Do not default to:
- full source files
- long speculative implementations
- fake completion statuses
- generic `implement feature` placeholders without verification
- broad research notes that belong in `findings.md`
- unverified external terminology or ecosystem claims presented as settled fact

## Step 3: Split Into Full-Copy Subplans

After the detail plan is written, use `skills/step-decomposition/SKILL.md` to split it into phase subplans that are full, verbatim copies.

The stage order is fixed: brainstorming -> (ui-ux-pro-max when needed) -> writing-plans -> step-decomposition -> execution with TDD.

Subplans must include:
- source path metadata
- required skill banner
- exact literal copy of the selected phase content from the detail plan

Subplans must start with this required skill banner before the copied phase content:
- `> Required Skill: Invoke `plan-for-all:test-driven-development` before executing the detailed steps below.`

Subplans are intentionally a phase-level copy of the detail plan for execution focus. Do not summarize, compress, or omit any part of the selected phase.

Preferred command for deterministic output:

`powershell -ExecutionPolicy Bypass -File plan-for-all/scripts/split-step-subplans-verbatim.ps1 -DetailPlanPath docs/plan-for-all/plans/YYYY-MM-DD-<topic>-detail.md`

## Step 4: Initialize Tracking Files

### `task_plan.md`
This is the single source of truth.

It must include:
- goal
- current mode
- phases with statuses (`pending`, `in_progress`, `completed`)
- active subplan path
- blockers
- knowledge blockers from audit
- open questions
- completion criteria

### `findings.md`
This file stores:
- decisions
- assumptions
- risks
- audit results
- unresolved questions
- term meaning resolution for high-risk terminology

It does not own progress state.

### `progress.md`
This file is append-only and factual.

It should record:
- timestamp
- action taken
- files touched
- verification run
- result

It must not mark global completion by itself.

## Step 5: Wait For Execution Approval

When planning is complete, tell the user:
- where the plan files were written
- what the active first phase is
- what smoke check will run first during execution
- whether any unresolved knowledge blockers remain

Execution begins only after the user asks to proceed.

## Plan Quality Checklist

Before handing off, confirm:
- goals and non-goals are visible in the detail plan
- every phase has verification, not just implementation intent
- bugfix plans include reproduction and failing regression tests
- refactor plans include behavior-preservation checks
- UI work includes a committed UI spec path and concrete UI constraints
- all mandatory audit items were verified or surfaced as blockers
- high-risk terminology has explicit current meaning in `findings.md`
- `task_plan.md` can be used alone to determine current status and blockers
- `progress.md` and `findings.md` do not claim authoritative completion

## Anti-Patterns

Do not do these:
- write the implementation inside the plan
- move TDD to a later reminder layer
- summarize, compress, or omit selected phase content when generating subplans
- initialize progress files with completed boxes that were never earned
- confuse research notes with execution state
- continue planning while mandatory terminology audit items remain hidden or unresolved
