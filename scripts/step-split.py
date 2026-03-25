#!/usr/bin/env python3
"""
Step-Split Script for step-planning skill

将 detail_plan.md 按 ## Chunk N 标题拆分为 step_subplan_*.md，
并生成 task_plan.md 统筹计划文件。

Usage: python3 step-split.py [plans-directory]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def find_detail_plan(plans_dir: Path) -> Optional[Path]:
    """找到最新的 detail plan 文件。"""
    if not plans_dir.exists():
        return None

    detail_plans = sorted(
        plans_dir.glob("*detail*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    # 也尝试查找没有 "-detail" 后缀但有 YYYY-MM-DD 的 plan 文件
    if not detail_plans:
        all_plans = sorted(
            plans_dir.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        for p in all_plans:
            if re.match(r'\d{4}-\d{2}-\d{2}-.*\.md', p.name):
                return p

    return detail_plans[0] if detail_plans else None


def parse_chunks(content: str) -> List[Dict[str, str]]:
    """解析 detail plan 内容，按 ## Chunk N 标题拆分。"""
    chunks = []

    # 匹配 ## Chunk N: 或 ## Phase N: 格式的标题
    chunk_pattern = re.compile(r'^##\s+(?:Chunk|Phase)\s+(\d+):\s*(.+)$', re.MULTILINE)

    positions = []
    for match in chunk_pattern.finditer(content):
        positions.append((match.start(), match.group(1), match.group(2).strip()))

    # 提取每个 Chunk 的内容
    for i, (start, num, title) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(content)
        chunk_content = content[start:end].strip()

        chunks.append({
            'number': num,
            'title': title,
            'content': chunk_content
        })

    return chunks


def extract_steps_from_chunk(chunk_content: str) -> List[Dict[str, str]]:
    """从 Chunk 内容中提取所有 Step（### Task N: 格式）。"""
    steps = []

    # 匹配 ### 1.1 title 或 ### Step N: title 或 **Step N:** 格式
    # 格式1: ### 1.1 title (无冒号)
    # 格式2: ### Step 1.1: title 或 ### Task 1.1: title
    # 格式3: **Step 1.1:** title (粗体)
    step_pattern = re.compile(
        r'^###\s+(\d+\.\d+)\s+(.+)$|^###\s+(?:Step|Task)\s+(\d+\.\d+):\s*(.+)$|^\*\*Step\s+(\d+\.\d+):\*\*\s*(.+)$',
        re.MULTILINE
    )

    positions = []
    for match in step_pattern.finditer(chunk_content):
        if match.group(1):  # Format: ### 1.1 title
            positions.append((match.start(), match.group(1), match.group(2).strip()))
        elif match.group(3):  # Format: ### Step N: title
            positions.append((match.start(), match.group(3), match.group(4).strip()))
        elif match.group(5):  # Format: **Step N:** title
            positions.append((match.start(), match.group(5), match.group(6).strip()))

    for i, (start, num, title) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(chunk_content)
        step_content = chunk_content[start:end].strip()

        steps.append({
            'number': num,
            'title': title,
            'content': step_content
        })

    return steps


def extract_tdd_steps(step_content: str) -> Dict[str, str]:
    """从 Step 内容中提取 TDD 循环的各个步骤。"""
    tdd = {
        'red': '',
        'green_run_fail': '',
        'green_code': '',
        'green_run_pass': '',
        'commit': ''
    }

    # 匹配各个 TDD 阶段
    patterns = {
        'red': re.compile(r'- \[ \]\s+\*\*.*RED.*:\s*\n+(.+?)(?=\n- \[ \]|\n---)', re.DOTALL | re.IGNORECASE),
        'green_run_fail': re.compile(r'- \[ \]\s+\*\*.*运行.*验证.*失败.*:\s*\n+(.+?)(?=\n- \[ \]|\n```\`\`|---)', re.DOTALL | re.IGNORECASE),
        'green_code': re.compile(r'(?:```\w*\n.+?\n```)', re.DOTALL),
        'green_run_pass': re.compile(r'- \[ \]\s+\*\*.*验证.*通过.*:\s*\n+(.+?)(?=\n- \[ \]|\n---)', re.DOTALL | re.IGNORECASE),
        'commit': re.compile(r'- \[ \]\s+\*\*.*COMMIT.*:\s*\n+(.+?)(?=\n- \[ \]|\n---)', re.DOTALL | re.IGNORECASE),
    }

    # 简化提取：如果没有精确匹配，提取所有代码块
    code_blocks = re.findall(r'```\w*\n.+?\n```', step_content, re.DOTALL)

    # 提取 bash 命令
    bash_commands = re.findall(r'运行：`(.+?)`', step_content)
    if bash_commands:
        tdd['green_run_fail'] = '\n'.join(bash_commands[:1])
        tdd['green_run_pass'] = '\n'.join(bash_commands[1:2])

    return tdd


def generate_step_subplan(chunk: Dict, steps: List[Dict], phase_num: int) -> str:
    """为一个 Phase 生成 step_subplan 文件内容。"""
    lines = []
    lines.append(f"# Phase {phase_num}: {chunk['title']} — Step Subplan\n")
    lines.append(f"> **关联 task_plan:** Phase {phase_num}\n")

    for step in steps:
        step_num = step['number']
        step_title = step['title']
        step_content = step['content']

        lines.append(f"\n## Step {step_num}: {step_title}\n")

        # 提取文件信息
        files_match = re.search(r'\*\*文件：\*\*(.+?)(?=\n###|\n##|\n---)', step_content, re.DOTALL)
        if files_match:
            lines.append(f"**文件：**\n{files_match.group(1).strip()}\n")

        lines.append("\n### TDD 循环\n")

        # 提取并简化 TDD 内容
        # RED
        red_match = re.search(r'- \[ \]\s+\*\*.*RED.*:\s*\n+(.+?)(?=\n- \[ \]|\n```\`\`|---)', step_content, re.DOTALL | re.IGNORECASE)
        if red_match:
            red_content = red_match.group(1).strip()
            # 提取代码块
            code_blocks = re.findall(r'```\w*\n.+?\n```', red_content, re.DOTALL)
            if code_blocks:
                lines.append("- [ ] **RED: 写一个失败的测试**\n")
                lines.append(code_blocks[0] + "\n")
            else:
                lines.append("- [ ] **RED: 写一个失败的测试**\n")
                lines.append("```\n" + red_content[:200] + "...\n```\n")

        # GREEN - 运行测试
        green_run_match = re.search(r'- \[ \]\s+\*\*.*GREEN.*运行.*:\s*\n+(.+?)(?=\n- \[ \]|\n```\`\`|---)', step_content, re.DOTALL | re.IGNORECASE)
        if green_run_match:
            lines.append("- [ ] **GREEN: 运行测试验证失败**\n")
            lines.append("```bash\n" + green_run_match.group(1).strip()[:200] + "\n```\n")

        # GREEN - 代码
        code_blocks = re.findall(r'```\w*\n(.+?)```', step_content, re.DOTALL)
        if len(code_blocks) >= 2:
            lines.append("- [ ] **GREEN: 写最小实现代码**\n")
            lines.append("```\n" + code_blocks[1].strip() + "\n```\n")

        # GREEN - 验证通过
        pass_match = re.search(r'- \[ \]\s+\*\*.*PASS.*:\s*\n+(.+?)(?=\n- \[ \]|\n---)', step_content, re.DOTALL | re.IGNORECASE)
        if pass_match:
            lines.append("- [ ] **GREEN: 运行测试验证通过**\n")
            lines.append("```bash\n" + pass_match.group(1).strip()[:200] + "\n```\n")

        # COMMIT
        commit_match = re.search(r'- \[ \]\s+\*\*.*COMMIT.*:\s*\n+(.+?)(?=\n- \[ \]|\n---)', step_content, re.DOTALL | re.IGNORECASE)
        if commit_match:
            lines.append("- [ ] **COMMIT: 提交**\n")
            commit_content = commit_match.group(1).strip()
            bash_blocks = re.findall(r'```bash\n(.+?)```', commit_content, re.DOTALL)
            if bash_blocks:
                lines.append("```bash\n" + bash_blocks[0].strip() + "\n```\n")
            else:
                lines.append("```bash\n" + commit_content[:200] + "\n```\n")

        lines.append("\n---\n")

    # 添加 Chunk 元信息
    lines.append("\n## Chunk 元信息\n")
    lines.append("```yaml\n")
    lines.append(f"phase: {phase_num}\n")
    lines.append(f"subplan_file: step_subplan_phase{phase_num}.md\n")
    lines.append("tdd_granularity: feature-block\n")
    lines.append("```\n")

    return ''.join(lines)


def generate_task_plan(detail_plan: Path, chunks: List[Dict]) -> str:
    """生成 task_plan.md 内容。"""
    lines = []

    # 提取头部信息
    content = detail_plan.read_text(encoding='utf-8')

    # 提取 Goal
    goal_match = re.search(r'\*\*Goal:\*\*\s*(.+)', content)
    goal = goal_match.group(1).strip() if goal_match else "[待填写目标]"

    # 提取 Architecture
    arch_match = re.search(r'\*\*Architecture:\*\*\s*(.+)', content, re.DOTALL)
    arch = arch_match.group(1).strip()[:200] if arch_match else "[待填写架构]"

    # 提取 Tech Stack
    stack_match = re.search(r'\*\*Tech Stack:\*\*\s*(.+)', content)
    stack = stack_match.group(1).strip() if stack_match else "[待填写技术栈]"

    # 文件名提取 feature name
    feature_match = re.search(r'(\d{4}-\d{2}-\d{2}-)(.+?)(?:-detail)?\.md', detail_plan.name)
    feature = feature_match.group(2).replace('-', ' ').title() if feature_match else detail_plan.stem

    lines.append(f"# {feature} Implementation Plan\n\n")
    lines.append("> **For agentic workers:** REQUIRED: 使用 superpowers:subagent-driven-development 或 superpowers:executing-plans 执行此计划。\n\n")
    lines.append(f"**Goal:** {goal}\n\n")
    lines.append(f"**Architecture:** {arch}\n\n")
    lines.append(f"**Tech Stack:** {stack}\n\n")
    lines.append("---\n\n")

    for i, chunk in enumerate(chunks):
        phase_num = i + 1
        phase_title = chunk['title']
        steps = extract_steps_from_chunk(chunk['content'])

        lines.append(f"## Phase {phase_num}: {phase_title}\n\n")
        lines.append(f"**Step Subplan:** `docs/superpowers/plans/step_subplans/step_subplan_phase{phase_num}.md`\n\n")

        for step in steps:
            lines.append(f"- [ ] Step {step['number']}: {step['title']}\n")

        lines.append("\n")

    lines.append("---\n\n")
    lines.append("## 遇到的错误\n")
    lines.append("| 错误 | 尝试次数 | 解决方案 |\n")
    lines.append("|------|---------|---------|\n")
    lines.append("|      | 1       |         |\n\n")

    return ''.join(lines)


def main():
    plans_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/superpowers/plans")

    if not plans_dir.exists():
        print(f"[step-split] 目录不存在: {plans_dir}")
        print(f"[step-split] 用法: python3 step-split.py [plans-directory]")
        sys.exit(1)

    detail_plan = find_detail_plan(plans_dir)
    if not detail_plan:
        print(f"[step-split] 未找到 detail plan 文件于 {plans_dir}")
        sys.exit(1)

    print(f"[step-split] 找到 detail plan: {detail_plan.name}")

    content = detail_plan.read_text(encoding='utf-8')
    chunks = parse_chunks(content)

    if not chunks:
        print("[step-split] 未找到任何 Chunk，无法拆分")
        sys.exit(1)

    print(f"[step-split] 找到 {len(chunks)} 个 Chunk")

    # 创建 step_subplans 目录
    subplans_dir = plans_dir / "step_subplans"
    subplans_dir.mkdir(exist_ok=True)

    # 生成每个 Phase 的 step_subplan
    for i, chunk in enumerate(chunks):
        phase_num = i + 1
        steps = extract_steps_from_chunk(chunk['content'])
        print(f"[step-split] Phase {phase_num}: {chunk['title']} - 找到 {len(steps)} 个 Step")

        step_subplan_content = generate_step_subplan(chunk, steps, phase_num)
        subplan_file = subplans_dir / f"step_subplan_phase{phase_num}.md"
        subplan_file.write_text(step_subplan_content, encoding='utf-8')
        print(f"[step-split] 写入: {subplan_file}")

    # 生成 task_plan.md
    task_plan_content = generate_task_plan(detail_plan, chunks)
    task_plan_file = Path("task_plan.md")
    task_plan_file.write_text(task_plan_content, encoding='utf-8')
    print(f"[step-split] 写入: {task_plan_file}")

    print(f"\n[step-split] 拆分完成！")
    print(f"[step-split] 请检查 task_plan.md 并根据需要调整状态")


if __name__ == '__main__':
    main()
