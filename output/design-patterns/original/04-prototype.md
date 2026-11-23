# 04. Prototype

[Contents](../README.md) · [Tiếng Việt](../vi/04-prototype.md)

## Problem

An office portal creates review workflows from existing departmental templates. Each preset already has named stages and default reviewers. A new draft should start with that configuration and remain editable. If the draft shares a mutable reviewer list with its template, adding a reviewer silently changes what the next document receives.

## Pattern and boundary

Prototype puts copying behavior behind a `clone()` operation. `startReview()` asks a selected `ReviewPrototype` to create a new draft. The concrete template knows which fields need a fresh copy and assigns the new draft name while retaining stage configuration. As independent template types appear, they can preserve their own rules without adding conditional reconstruction to the caller.

## TypeScript example

The constructor takes ownership of mutable state by copying the stages and each nested reviewer list. `clone()` invokes that constructor, so two drafts each start with the same values and can diverge. The example checks both the inherited values and the isolation of the two drafts.

```typescript
type ReviewStage = Readonly<{ name: string; reviewers: readonly string[] }>

interface ReviewDraft {
  readonly name: string
  addReviewer(stageName: string, reviewer: string): void
  reviewersFor(stageName: string): readonly string[]
}

interface ReviewPrototype {
  clone(draftName: string): ReviewDraft
}

class ReviewWorkflow implements ReviewPrototype, ReviewDraft {
  private readonly stages: { name: string; reviewers: string[] }[]

  constructor(readonly name: string, stages: readonly ReviewStage[]) {
    this.stages = stages.map(stage => ({
      name: stage.name,
      reviewers: [...stage.reviewers],
    }))
  }

  clone(draftName: string): ReviewWorkflow {
    return new ReviewWorkflow(draftName, this.stages)
  }

  addReviewer(stageName: string, reviewer: string): void {
    const stage = this.stages.find(candidate => candidate.name === stageName)
    if (!stage) throw new Error("Unknown review stage")
    stage.reviewers.push(reviewer)
  }

  reviewersFor(stageName: string): readonly string[] {
    const stage = this.stages.find(candidate => candidate.name === stageName)
    if (!stage) throw new Error("Unknown review stage")
    return [...stage.reviewers]
  }
}

function startReview(prototype: ReviewPrototype, draftName: string): ReviewDraft {
  return prototype.clone(draftName)
}

const finance = new ReviewWorkflow("Finance default", [
  { name: "approval", reviewers: ["Hanh"] },
])
const first = startReview(finance, "Q1 draft")
if (first.name !== "Q1 draft" || first.reviewersFor("approval").join(",") !== "Hanh") {
  throw new Error("The draft must inherit configuration and receive its own name")
}

first.addReviewer("approval", "Linh")
const second = startReview(finance, "Q2 draft")
if (first.reviewersFor("approval").join(",") !== "Hanh,Linh" ||
    second.reviewersFor("approval").join(",") !== "Hanh" ||
    finance.reviewersFor("approval").join(",") !== "Hanh") {
  throw new Error("A draft edit must stay in that draft")
}
```

## When to use

Use Prototype when a configured example is the most useful starting point for new objects and copying rules vary by concrete type. Identify which fields are owned by the clone, which immutable values can be shared, and which identity or lifecycle fields must be regenerated. The appropriate copy boundary comes from the domain. A draft workflow can inherit default reviewers while receiving a new name or ID.

## When a simpler approach is enough

An ordinary factory with a parameter object is simpler when all creation inputs are explicit and there is one concrete type. For plain, immutable configuration, sharing a preset and replacing only the values that differ can also be sufficient. Reach for a polymorphic copy method when callers otherwise need to reproduce private construction or copying rules.

## Trade-offs

- A shallow copy shares nested state, which can make later mutations leak between drafts. Copying a large owned object graph increases CPU and memory use.
- Resources such as sockets or open transactions have lifecycles of their own. Decide whether to reconnect or pass a reference through a separate boundary.
- Generic copying utilities support specific types. A domain clone can preserve class behavior and deliberately exclude runtime identity.

## Practice

Add a second stage and create two drafts from the same prototype. Append a reviewer to the second stage of the first draft. Verify that the first stage and both original reviewer lists in the second draft retain their original values.

## References

- [Refactoring.Guru · Prototype](https://refactoring.guru/design-patterns/prototype)

[← Previous · 03. Builder](03-builder.md) · [Next → · 05. Singleton](05-singleton.md)
