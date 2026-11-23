# 13. Chain of Responsibility

[Contents](../README.md) · [Tiếng Việt](../vi/13-chain-of-responsibility.md)

## Problem

A document portal routes submissions to a reviewer. Oversized documents go to a senior reviewer, and documents subject to a compliance policy go to a specialist. Both conditions can apply to one submission, with compliance taking precedence. The next customer may add a legal-review rule and place it between those two checks.

The portal already knows how to send work to a queue. What changes is the set and ordering of rules that choose the queue.

## Pattern and boundary

Give each handler the same request and a way to signal that it declines. The first handler willing to take responsibility ends the search. The caller hands its request to the chain, and the code that assembles the chain decides precedence.

Here, functions stand in for handler objects. The dispatcher advances through an ordered array, which plays the same forwarding role as a successor reference in a linked chain. The resulting queue identifier crosses the boundary back to the portal, which owns the next step. An exhausted chain returns `undefined` so the portal can apply its own policy for unmatched documents.

## TypeScript example

```typescript
type ReviewRequest = Readonly<{ pages: number; regulated: boolean }>;
type Queue = "compliance" | "senior-review";
type ReviewHandler = (request: ReviewRequest) => Queue | undefined;

const compliance: ReviewHandler = request =>
  request.regulated ? "compliance" : undefined;
const seniorReview: ReviewHandler = request =>
  request.pages > 50 ? "senior-review" : undefined;

function selectQueue(
  request: ReviewRequest,
  handlers: readonly ReviewHandler[],
): Queue | undefined {
  for (const handle of handlers) {
    const queue = handle(request);
    if (queue !== undefined) return queue;
  }
  return undefined;
}

const handlers = [compliance, seniorReview];
if (selectQueue({ regulated: false, pages: 70 }, handlers) !== "senior-review") {
  throw new Error("A declining handler must pass the request onward");
}
if (selectQueue({ regulated: true, pages: 70 }, handlers) !== "compliance") {
  throw new Error("Compliance must take precedence when both rules match");
}
if (selectQueue({ regulated: false, pages: 5 }, handlers) !== undefined) {
  throw new Error("An unmatched request must remain unassigned");
}
```

## When to use

Use a chain when eligibility rules overlap, their order matters, and deployments are likely to add or reorder independently owned rules. Keep route selection free from writes when the caller needs to retry safely.

### Common use cases

- **Routing submissions for review.** Check compliance cases first, then high-value cases. If several rules match, the first match determines the destination. Test requests that match multiple rules and the fallback to the default queue when none match.
- **Passing a request through multiple processing layers.** Format and permission checks can return errors early or forward the request to the next step. Define which steps may terminate the chain and which must always run. If every step is mandatory in a fixed order, a sequential orchestration function is easier to follow.

## When a simpler approach is enough

Two stable checks can live in a single function. An exact key such as the declared document type generally fits a lookup table.

## Trade-offs

Rule placement becomes part of behavior. A new broad rule near the front can shadow a later specialist, so test overlapping requests as well as each rule in isolation. Decide explicitly whether a thrown error aborts dispatch or is mapped to a known outcome.

## Practice

Insert a legal-review handler using a new request flag. A regulated request with that flag should still route to compliance, a non-regulated request with the flag should route to legal review, and an unmatched request should stay unassigned.

## References

- [Chain of Responsibility · Refactoring.Guru](https://refactoring.guru/design-patterns/chain-of-responsibility)

[← Previous · 12. Proxy](12-proxy.md) · [Next → · 14. Command](14-command.md)
