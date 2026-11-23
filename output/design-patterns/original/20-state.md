# 20. State

[Contents](../README.md) · [Tiếng Việt](../vi/20-state.md)

## Problem

A document follows a review lifecycle. A draft can be submitted. A document in review can be approved or sent back for changes. An approved document is terminal in this workflow. There may soon be a withdrawn state with different allowed actions. If eligibility checks spread across the submit and approval actions, adding that state can require changes in every existing handler.

## Pattern and boundary

Make the context delegate state-dependent decisions to its current state. Each concrete state defines its available behavior and can name a successor. The context owns the current state and applies a permitted transition. Invalid actions leave the context unchanged and return a rejection result.

In this example, the state objects define transition rules and `DocumentReview` alone updates its private state. Returning the same state instance signals rejection in this example. If an action may succeed without changing state, use an explicit result that distinguishes acceptance from transition. The public actions represent meaningful requests such as `submit`. Callers never set a status directly. With Strategy, a caller or configuration can select among algorithms for a job. In State, the object's lifecycle determines which behavior and transitions are available when the request arrives.

## TypeScript example

```typescript
type ReviewAction = "submit" | "approve" | "request-changes";
type Status = "draft" | "in-review" | "approved";

interface ReviewState {
  readonly status: Status;
  next(action: ReviewAction): ReviewState;
}

class DraftState implements ReviewState {
  readonly status = "draft";

  next(action: ReviewAction): ReviewState {
    return action === "submit" ? new InReviewState() : this;
  }
}

class InReviewState implements ReviewState {
  readonly status = "in-review";

  next(action: ReviewAction): ReviewState {
    if (action === "approve") return new ApprovedState();
    if (action === "request-changes") return new DraftState();
    return this;
  }
}

class ApprovedState implements ReviewState {
  readonly status = "approved";

  next(_action: ReviewAction): ReviewState {
    return this;
  }
}

class DocumentReview {
  private state: ReviewState = new DraftState();

  status(): Status {
    return this.state.status;
  }

  dispatch(action: ReviewAction): boolean {
    const next = this.state.next(action);
    if (next === this.state) return false;
    this.state = next;
    return true;
  }
}

const review = new DocumentReview();
if (review.dispatch("approve") || review.status() !== "draft") {
  throw new Error("A draft cannot be approved directly");
}
if (!review.dispatch("submit") || review.status() !== "in-review") {
  throw new Error("Submitting a draft should move it into review");
}
if (!review.dispatch("request-changes") || review.status() !== "draft") {
  throw new Error("A request for changes should return the document to draft");
}
if (!review.dispatch("submit") || !review.dispatch("approve")) {
  throw new Error("A revised draft should be eligible for approval");
}
if (review.dispatch("request-changes") || review.status() !== "approved") {
  throw new Error("An approved review is terminal in this workflow");
}
```

## When to use

Use State when the same operations behave differently across lifecycle stages and those stages are acquiring distinct rules. Validate permissions before applying any authorized transition where the workflow has actors with different rights.

### Common use cases

- **Approving a submission.** A draft can be submitted, an item under review can be approved or returned, and an approved item has its own rules. Group action handling by state. For persisted data, check its version when writing so concurrent actions cannot both proceed from the same old state.
- **Handling an import lifecycle.** Cancel can discard a queued import immediately and request termination for a running one. A completed import can reject cancellation. A transition table is often sufficient when each action only determines a next state and behavior has yet to diverge.

## When a simpler approach is enough

For a small transition graph with no state-specific behavior, an explicit table of allowed actions and outcomes keeps the whole graph visible. A short switch can serve a stable two-state workflow.

## Trade-offs

Behavior is grouped by state, while a reader may need to inspect several classes to see the full graph. Test every allowed transition, the rejected actions, and any terminal states. A persisted workflow also needs atomic updates or version checks to stop concurrent actions from both being accepted against the same old state.

## Practice

Add a withdrawn state reached by dispatching `withdraw` from an in-review document. Verify that withdrawal is rejected from draft, succeeds during review, and prevents further approval in the withdrawn state.

## References

- [State · Refactoring.Guru](https://refactoring.guru/design-patterns/state)

[← Previous · 19. Observer](19-observer.md) · [Next → · 21. Strategy](21-strategy.md)
