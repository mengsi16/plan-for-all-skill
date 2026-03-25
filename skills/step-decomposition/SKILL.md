---
name: step-decomposition
description: "将 detail_plan.md 中的 Phase 提取为 step_subplan"
---

# Step Decomposition

将 `detail_plan.md` 中的指定 Phase（Chunk）提取整理为 `step_subplan_phase{N}.md`。

---

## 输入

- `detail_plan.md` 文件路径
- 要提取的 Phase 编号

---

## 输出

`docs/plan-for-all/plans/step_subplans/step_subplan_phase{N}.md`

格式：
```markdown
# Phase [N]: [标题] — Step Subplan

> **来源：** detail_plan.md

## Step [编号]: [标题]

### 详细内容
[从 detail_plan 提取的完整实现内容]

### TDD 循环
- [ ] **RED:** 写失败的测试
- [ ] **GREEN:** 运行测试验证失败
- [ ] **GREEN:** 写最小实现代码
- [ ] **GREEN:** 运行测试验证通过
- [ ] **COMMIT:** 提交

---

## Step [编号]: [标题]
...

## Chunk 元信息
```yaml
phase: [编号]
source: detail_plan.md
tdd_granularity: step
```
```

---

## 示例

**输入：** detail_plan.md 中 Phase 1 的内容：
```markdown
## Chunk 1: 用户认证

### 组件 1.1: NextAuth 配置

**文件：**
- Create: `auth.ts`

**Step 1:** 安装 NextAuth 并配置 Google Provider
```bash
npm install next-auth@beta
```

**Step 2:** 创建 auth.ts 配置文件
```typescript
import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
}

const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }
```
```

**输出：** step_subplan_phase1.md：
```markdown
# Phase 1: 用户认证 — Step Subplan

> **来源：** detail_plan.md

## Step 1.1: 安装 NextAuth 并配置 Google Provider

**命令：**
```bash
npm install next-auth@beta
```

### TDD 循环
- [ ] **RED:** 写失败的测试
  ```typescript
  // 测试 NextAuth 安装
  ```
- [ ] **GREEN:** 运行测试验证失败
  ```bash
  npm test -- --grep "NextAuth"
  ```
- [ ] **GREEN:** 写最小实现代码
  ```bash
  npm install next-auth@beta
  ```
- [ ] **GREEN:** 运行测试验证通过
  ```bash
  npm test -- --grep "NextAuth"
  ```
- [ ] **COMMIT:** 提交
  ```bash
  git add . && git commit -m "feat: install next-auth"
  ```

## Step 1.2: 创建 auth.ts 配置文件
**文件：**
- Create: `auth.ts`

### TDD 循环
- [ ] **RED:** 写失败的测试
- [ ] **GREEN:** 运行测试验证失败
- [ ] **GREEN:** 写最小实现代码
  ```typescript
  import NextAuth from "next-auth"
  import GoogleProvider from "next-auth/providers/google"

  export const authOptions = {
    providers: [
      GoogleProvider({
        clientId: process.env.GOOGLE_CLIENT_ID!,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      }),
    ],
  }

  const handler = NextAuth(authOptions)
  export { handler as GET, handler as POST }
  ```
- [ ] **GREEN:** 运行测试验证通过
- [ ] **COMMIT:** 提交
  ```bash
  git add . && git commit -m "feat: add auth config with Google provider"
  ```

## Chunk 元信息
```yaml
phase: 1
source: detail_plan.md
tdd_granularity: step
```
```

---

## 执行步骤

1. 读取 `docs/plan-for-all/plans/` 下的 detail_plan.md
2. 找到 `## Chunk N:` 或 `## Phase N:` 开头的章节
3. 提取该 Phase 下的所有组件和 Step
4. 按上述格式生成 step_subplan_phase{N}.md
5. 保存到 `docs/plan-for-all/plans/step_subplans/`
