# 09. Decorator

[Contents](../README.md) · [Tiếng Việt](../vi/09-decorator.md)

## Problem

A document service reads from an existing storage component. Some entry points need an event for every successful read, while operators need a count of all attempts, including failures. The application can enable either behavior independently. If the reader grows a flag for each concern, every combination must be understood inside the code responsible for reading content. A second storage backend would also risk duplicating that code.

## Pattern and boundary

Decorator wraps a component, implements the same client-facing interface, and adds a behavior around delegation. `MemoryReader` is the concrete component. `ReadAudit` and `ReadMetrics` are decorators that each accept another `DocumentReader`, including another decorator. The caller receives the interface it already uses. The wrappers can change independently of the reader and can be composed where the application assembles its dependencies.

## TypeScript example

The example records successful reads in an in-memory event list and counts total attempts. The checks cover the original return value, delegation of the original error, and the different meanings of the two measurements.

```typescript
interface DocumentReader {
  read(id: string): string;
}

class MemoryReader implements DocumentReader {
  constructor(private readonly docs: ReadonlyMap<string, string>) {}

  read(id: string): string {
    const body = this.docs.get(id);
    if (body === undefined) throw new Error("Unknown document");
    return body;
  }
}

class ReadAudit implements DocumentReader {
  constructor(
    private readonly inner: DocumentReader,
    private readonly events: string[],
  ) {}

  read(id: string): string {
    const body = this.inner.read(id);
    this.events.push("read:" + id);
    return body;
  }
}

class ReadMetrics implements DocumentReader {
  attempts = 0;

  constructor(private readonly inner: DocumentReader) {}

  read(id: string): string {
    this.attempts += 1;
    return this.inner.read(id);
  }
}

const events: string[] = [];
const base = new MemoryReader(new Map([["a", "meeting notes"]]));
const metrics = new ReadMetrics(new ReadAudit(base, events));
const reader: DocumentReader = metrics;
if (reader.read("a") !== "meeting notes" || events.join(",") !== "read:a") {
  throw new Error("The decorated reader should retain the base result");
}

let missing = false;
try {
  reader.read("missing");
} catch (error) {
  if (!(error instanceof Error) || error.message !== "Unknown document") throw error;
  missing = true;
}
if (!missing || metrics.attempts !== 2 || events.length !== 1) {
  throw new Error("Count both attempts and record only successful reads");
}
```

## When to use

Use it when clients share a stable interface and need independent, optional responsibilities in different combinations. With the same reader contract, the audit wrapper can also wrap a filesystem reader or a storage gateway. If the framework already provides middleware or interceptors at the right boundary, those may supply the same composition without another layer.

### Common use cases

- **Measuring file-read latency.** A timing decorator wraps the existing reader, calls it, and records duration even when it fails. A logging decorator can be added for some requests. With a cache, the wrapping order determines whether measurements include cache hits or only underlying reads.
- **Adding optional export behavior.** One wrapper compresses the result and records the encoding in its metadata, while another sets a download filename. Both implement the same export contract, so callers can select a combination. A framework's layering mechanism can serve the same purpose when it preserves that contract.

## When a simpler approach is enough

One invariant rule may belong inside the component or in its single caller. A higher-order function may serve the same purpose when the interface is just one function and has no per-instance configuration or state.

## Trade-offs

Wrapper ordering changes which actions are visible and when side effects run. For example, placing metrics outside a cache counts all reads, while placing it inside counts only requests that reach the store. Decide how a real logging or metrics sink may fail, especially when success is contingent on an audit record. Test compositions that depend on those semantics.

## Practice

Add a wrapper that records the length of successful results. Compose it with both existing decorators. Check that a miss preserves the original error and contributes neither a result length nor a success event.

## References

- [Decorator — Refactoring.Guru](https://refactoring.guru/design-patterns/decorator)

[← Previous · 08. Composite](08-composite.md) · [Next → · 10. Facade](10-facade.md)
