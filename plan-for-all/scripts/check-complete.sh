#!/usr/bin/env bash
# Check Complete Script for step-planning
# 验证所有 Phase 和 Step 是否完成

if [ ! -f task_plan.md ]; then
    echo "[step-planning] task_plan.md 不存在"
    exit 1
fi

echo "[step-planning] 检查任务完成状态..."
echo ""

# 统计
TOTAL=$(grep -c '\- \[' task_plan.md 2>/dev/null || echo 0)
COMPLETE=$(grep -c '\- \[x\]' task_plan.md 2>/dev/null || echo 0)
IN_PROGRESS=$(grep -c '\- \[ \]' task_plan.md 2>/dev/null || echo 0)
PHASES=$(grep -c '^## Phase' task_plan.md 2>/dev/null || echo 0)

echo "Phase 总数: $PHASES"
echo "Step 总数: $TOTAL"
echo "已完成: $COMPLETE"
echo "进行中: $IN_PROGRESS"
echo ""

# 检查是否有 in_progress
if grep -q 'in_progress' task_plan.md 2>/dev/null; then
    CURRENT=$(grep -B1 'in_progress' task_plan.md | head -2)
    echo "当前进行中:"
    echo "$CURRENT"
    echo ""
fi

# 计算百分比
if [ "$TOTAL" -gt 0 ]; then
    PERCENT=$((COMPLETE * 100 / TOTAL))
    echo "完成进度: ${PERCENT}%"
fi

echo ""

if [ "$COMPLETE" = "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "[step-planning] 所有任务已完成！"
    exit 0
else
    echo "[step-planning] 任务尚未完成，请继续执行"
    exit 1
fi
