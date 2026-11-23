# 21. Strategy

[Contents](../README.md) · [Tiếng Việt](../vi/21-strategy.md)

## Problem

An archive team estimates how long document imports will take. Interactive imports use the recorded file count and average processing time. Scheduled imports also account for a fixed delay before the batch window. Both estimates feed the same status screen. A third estimate for historical replays would otherwise add another branch to the status code.

Name the contract before extracting it. In this case, the rule receives the same facts and always returns an estimate in seconds. The caller can handle the result consistently across rules.

## Pattern and boundary

Strategy gives the context, here the status formatter, an interchangeable algorithm behind a shared contract. The caller picks the rule at the point where it knows the import mode and passes it in. A function type supplies the contract in TypeScript. Each rule can be tested independently, and a new rule can be attached without revising the formatter.

Both rules should agree on the meaning of their inputs and the units of their results. An algorithm that also schedules the import would introduce a side effect outside this contract.

## TypeScript example

```typescript
type ImportBatch = Readonly<{ fileCount: number; secondsPerFile: number }>;
type EstimateSeconds = (batch: ImportBatch) => number;

const interactiveEstimate: EstimateSeconds = ({ fileCount, secondsPerFile }) =>
  fileCount * secondsPerFile;

const scheduledEstimate: EstimateSeconds = (batch) =>
  60 + interactiveEstimate(batch);

function statusLine(batch: ImportBatch, estimate: EstimateSeconds): string {
  return `Estimated time: ${estimate(batch)} seconds`;
}

const batch = { fileCount: 3, secondsPerFile: 5 };

if (statusLine(batch, interactiveEstimate) !== "Estimated time: 15 seconds") {
  throw new Error("Interactive estimate should use the processing time");
}
if (statusLine(batch, scheduledEstimate) !== "Estimated time: 75 seconds") {
  throw new Error("Scheduled estimate should include the batch delay");
}
```

## When to use

Use Strategy when alternatives evolve independently and need one stable set of inputs and outputs. It also fits when two callers need the same surrounding workflow with different rules.

## When a simpler approach is enough

Keep a conditional when the rules are short, stable, and used once. If only the delay value varies, accept the value as a parameter or use a lookup table.

## Trade-offs

Selection and behavior now live in separate places. Pick one place to select the rule, and give concrete strategies names that identify their policy. A type signature checks the shape of the result, while tests still need to establish units, normal cases, and boundary values.

## Practice

Add a replay rule that estimates with half the recorded processing time per file and rounds the total up. An import with three files at five seconds per file should report eight seconds, and the other modes should keep their existing results.

## References

- [Strategy · Refactoring.Guru](https://refactoring.guru/design-patterns/strategy)

[← Previous · 20. State](20-state.md) · [Next → · 22. Template Method](22-template-method.md)
