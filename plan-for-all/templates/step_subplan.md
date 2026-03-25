# Phase N: [阶段名称] — Step Subplan

> **关联 task_plan:** Phase N

## Step N.1: [功能块名称]

**文件：**
- Create: `src/xxx.ts`
- Modify: `src/yyy.ts:1-50`
- Test: `tests/xxx.test.ts`

### TDD 循环

- [ ] **RED: 写一个失败的测试**

```typescript
test('[功能描述]', async () => {
  // 测试代码
});
```

- [ ] **GREEN: 运行测试验证失败，然后写最小代码**

```bash
npm test tests/xxx.test.ts -- --testNamePattern="功能描述"
# 预期：FAIL - function is not defined
```

```typescript
function/[class]() {
  // 最小实现
  return expected;
}
```

- [ ] **REFACTOR: 确认测试通过，清理代码**

```bash
npm test tests/xxx.test.ts
# 预期：PASS
```

- [ ] **COMMIT: 提交**

```bash
git add tests/xxx.test.ts src/xxx.ts
git commit -m "feat: [功能描述]"
```

---

## Step N.2: [下一个功能块名称]

[同上结构...]

---

## Chunk 元信息

```yaml
phase: N
subplan_file: step_subplan_phaseN.md
created_from: docs/plan-for-all/plans/YYYY-MM-DD-<feature>-detail.md
tdd_granularity: feature-block
```
