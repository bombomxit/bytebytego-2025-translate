# 06. Adapter

[Contents](../README.md) · [Tiếng Việt](../vi/06-adapter.md)

## Problem

A document portal needs to read metadata from a legacy index. Its screens and background jobs expect a document ID, a byte count, and a clear distinction between a missing document and an index outage. The legacy index uses its own field names and status codes. If every caller interprets them, migrating the index means finding every copy of that translation. An outage handled as a miss could also trigger an incorrect “document deleted” notification.

## Pattern and boundary

Adapter implements the interface the client already expects and delegates work to the incompatible service. Here `DocumentDirectory` is the target interface, `LegacyIndex` is the adaptee, and `LegacyDirectoryAdapter` owns the translation. The caller depends on the directory contract and can receive either the legacy adapter or a replacement. Keep the boundary narrow so that vendor-specific decisions stay in the adapter and policies such as retrying a lookup stay in the appropriate caller or resilience layer.

## TypeScript example

The legacy reply type describes an already decoded response. The adapter maps fields and status codes. The checks confirm that metadata is translated and that an outage remains distinguishable from a miss.

```typescript
type DocumentInfo = { id: string; bytes: number };
type DocumentLookup =
  | { kind: "found"; document: DocumentInfo }
  | { kind: "missing" }
  | { kind: "unavailable" };

interface DocumentDirectory {
  find(id: string): DocumentLookup;
}

type LegacyReply =
  | { status: "OK"; record: { document_no: string; size_b: number } }
  | { status: "NOT_FOUND" }
  | { status: "INDEX_OFFLINE" };

interface LegacyIndex {
  lookup(documentNumber: string): LegacyReply;
}

class LegacyDirectoryAdapter implements DocumentDirectory {
  constructor(private readonly legacy: LegacyIndex) {}

  find(id: string): DocumentLookup {
    const reply = this.legacy.lookup(id);
    switch (reply.status) {
      case "OK":
        return {
          kind: "found",
          document: { id: reply.record.document_no, bytes: reply.record.size_b },
        };
      case "NOT_FOUND":
        return { kind: "missing" };
      case "INDEX_OFFLINE":
        return { kind: "unavailable" };
    }
  }
}

const directory: DocumentDirectory = new LegacyDirectoryAdapter({
  lookup: (id) => {
    if (id === "d1") {
      return { status: "OK", record: { document_no: id, size_b: 240 } };
    }
    if (id === "d2") return { status: "NOT_FOUND" };
    return { status: "INDEX_OFFLINE" };
  },
});
const found = directory.find("d1");
if (found.kind !== "found" || found.document.id !== "d1" ||
    found.document.bytes !== 240) {
  throw new Error("Expected normalized document metadata");
}
if (directory.find("d2").kind !== "missing" ||
    directory.find("d3").kind !== "unavailable") {
  throw new Error("Missing documents and outages must stay distinct");
}
```

## When to use

Use it when the same provider-specific concepts recur across callers, or when you must run old and new integrations under one application contract. In this example a second provider can return the same union from a different response without changing the portal or its jobs.

## When a simpler approach is enough

For a single field rename after one request, a local mapping function can be sufficient. An object adapter earns its place when the application needs a stable dependency with several implementations, a lifetime to manage, or multiple operations backed by the same provider.

## Trade-offs

A translator must be maintained as upstream semantics change. The contract should document units, nullability, and failure meanings because matching types alone leaves room for mismatches. At a real network boundary, validate the decoded payload and decide explicitly how to surface malformed responses and transport failures.

## Practice

Add an adapter for a replacement index that reports file sizes in KiB. Reuse the checks through `DocumentDirectory` and add a case proving that 2 KiB becomes 2048 bytes. The caller should remain unchanged.

## References

- [Adapter — Refactoring.Guru](https://refactoring.guru/design-patterns/adapter)

[← Previous · 05. Singleton](05-singleton.md) · [Next → · 07. Bridge](07-bridge.md)
