# 12. Proxy

[Contents](../README.md) · [Tiếng Việt](../vi/12-proxy.md)

## Problem

Browsing document metadata rarely needs the preview catalog, but opening a local preview index can be expensive. The preview lookup interface already exists and clients expect it throughout the application. Eager initialization makes every process pay the cost, and caller-managed lazy loading spreads the responsibility for holding the catalog and handling load failures across features.

## Pattern and boundary

Proxy provides a stand-in for a subject and controls how or when it is reached. `PreviewCatalog` is the shared subject interface, `LoadedPreviewCatalog` is the real subject, and `LazyPreviewCatalog` is a virtual proxy that loads its subject on the first lookup. The client only sees the lookup contract. In a Decorator design, the caller typically composes optional responsibilities around an existing component. Here the proxy owns access to the real instance and determines when it starts to exist.

## TypeScript example

The checks show that constructing the proxy performs no load. The first lookup loads the catalog, and later lookups reuse the same instance and preserve the catalog's missing-entry result.

```typescript
interface PreviewCatalog {
  lookup(documentId: string): string | undefined;
}

class LoadedPreviewCatalog implements PreviewCatalog {
  constructor(private readonly files: ReadonlyMap<string, string>) {}

  lookup(documentId: string): string | undefined {
    return this.files.get(documentId);
  }
}

class LazyPreviewCatalog implements PreviewCatalog {
  private catalog?: PreviewCatalog;

  constructor(private readonly load: () => PreviewCatalog) {}

  lookup(documentId: string): string | undefined {
    if (this.catalog === undefined) {
      this.catalog = this.load();
    }
    return this.catalog.lookup(documentId);
  }
}

let loadCount = 0;
const catalog: PreviewCatalog = new LazyPreviewCatalog(() => {
  loadCount += 1;
  return new LoadedPreviewCatalog(new Map([["d1", "preview-d1.webp"]]));
});
const initialLoadCount = loadCount;
if (initialLoadCount !== 0 || catalog.lookup("d1") !== "preview-d1.webp") {
  throw new Error("The real catalog should load only at first use");
}

if (catalog.lookup("unknown") !== undefined || loadCount !== 1) {
  throw new Error("Repeated lookups should reuse the catalog and preserve misses");
}
```

## When to use

Use it when a subject has an expensive initialization, and preserving a stable interface matters to clients. Other familiar uses include a representative for a remote object or a protection proxy that checks access at a trusted boundary. In all cases, define what a successful call and failure look like to the client.

### Common use cases

- **Loading document previews on demand.** The UI shows document metadata first, and a proxy opens the preview when the user requests it. With asynchronous loading, simultaneous viewers can share the in-flight request. Define when another attempt is allowed after a failed load.
- **Representing a remote service.** Callers use a proxy through the service interface. It sends calls over the network and reports timeouts. The contract should spell out network errors and safe retry conditions because a remote operation may execute before its response is lost.

## When a simpler approach is enough

If initialization is cheap or every process uses the catalog immediately, construct the real subject directly. With a single caller, a lazy getter or one explicit load at the use site may handle the lifetime clearly enough.

## Trade-offs

Deferring load moves cost and initialization failure to the first request. In this synchronous example a thrown setup error leaves the slot empty, so a later lookup tries again. An asynchronous proxy should share an in-flight load where appropriate and define its retry and cancellation rules. If the real subject can change, the proxy needs an explicit lifetime or invalidation policy.

## Practice

Make the loader throw on its first attempt and succeed on its second. Check that the first lookup exposes the error, the second can succeed, and a third does not perform another load.

## References

- [Proxy — Refactoring.Guru](https://refactoring.guru/design-patterns/proxy)

[← Previous · 11. Flyweight](11-flyweight.md) · [Next → · 13. Chain of Responsibility](13-chain-of-responsibility.md)
