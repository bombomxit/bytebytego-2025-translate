# 10. Facade

[Contents](../README.md) · [Tiếng Việt](../vi/10-facade.md)

## Problem

The export endpoint and a background worker need to prepare the latest document version for delivery once that version is approved. Each request reads the version, checks its approval status, renders the exact version it read, and archives the result under that revision. Repeating this sequence invites drift. A worker that renders a draft or stores the output under a later revision can produce an export the system cannot trace back to its inputs.

## Pattern and boundary

Facade offers one entry point over several subsystem operations. The clients call `DocumentExport.prepare` with a document ID. The facade coordinates `VersionStore`, `ExportRenderer`, and `ExportArchive` and returns an application result. The subsystem interfaces still serve legitimate use cases on their own. A preview service, for example, might use the renderer without the archive. Keep the facade focused on the export operation and leave general storage and rendering logic with their owners.

## TypeScript example

The checks show an approved version flowing through the three dependencies in order and a draft stopping before rendering or archiving. In-memory dependencies record what happened so the example runs independently of any infrastructure.

```typescript
type Version = { revision: number; approved: boolean; text: string };

interface VersionStore {
  latest(documentId: string): Version;
}

interface ExportRenderer {
  render(text: string): string;
}

interface ExportArchive {
  store(documentId: string, revision: number, output: string): string;
}

type ExportResult =
  | { kind: "ready"; archiveId: string }
  | { kind: "approval-required" };

class DocumentExport {
  constructor(
    private readonly versions: VersionStore,
    private readonly renderer: ExportRenderer,
    private readonly archive: ExportArchive,
  ) {}

  prepare(documentId: string): ExportResult {
    const version = this.versions.latest(documentId);
    if (!version.approved) return { kind: "approval-required" };

    const output = this.renderer.render(version.text);
    const archiveId = this.archive.store(documentId, version.revision, output);
    return { kind: "ready", archiveId };
  }
}

const trace: string[] = [];
const exporter = new DocumentExport(
  {
    latest: (documentId) => {
      trace.push("read:" + documentId);
      return { revision: 3, approved: documentId === "approved", text: "Summary" };
    },
  },
  {
    render: (text) => {
      trace.push("render:" + text);
      return "Exported " + text;
    },
  },
  {
    store: (documentId, revision, output) => {
      trace.push("store:" + output);
      return documentId + "/" + revision;
    },
  },
);

const ready = exporter.prepare("approved");
if (ready.kind !== "ready" || ready.archiveId !== "approved/3") {
  throw new Error("The facade should return the archived revision");
}
if (exporter.prepare("draft").kind !== "approval-required" ||
    trace.join(",") !== "read:approved,render:Summary,store:Exported Summary,read:draft") {
  throw new Error("A draft should stop before rendering and archiving");
}
```

## When to use

Use it when a client needs a stable operation built from several lower-level calls or rules. A mobile export endpoint can share the same contract with a worker, even if storage and rendering change internally. If a provider uses an incompatible interface, a facade can use an adapter as one of its components.

## When a simpler approach is enough

If a single client calls one stable operation, use that subsystem directly. A small function may be enough to coordinate two calls owned by the same module. Extract a facade when the use case benefits from a named boundary and clients can usefully share it.

## Trade-offs

Consumers see fewer implementation details, so the result must expose actionable outcomes. Define behavior for storage failures and retries before using the facade in a worker. An upload can succeed while its response is lost. Safe retry may require a durable idempotency key that identifies the chosen document, revision, and export format.

## Practice

Extend the example with a renderer that throws. Check that the failure propagates and the archive is never called. The facade signature and its callers should stay the same.

## References

- [Facade — Refactoring.Guru](https://refactoring.guru/design-patterns/facade)

[← Previous · 09. Decorator](09-decorator.md) · [Next → · 11. Flyweight](11-flyweight.md)
