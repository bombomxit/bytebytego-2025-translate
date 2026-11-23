# 07. Bridge

[Contents](../README.md) · [Tiếng Việt](../vi/07-bridge.md)

## Problem

An operations portal exports a storage report and a review-queue report. Both need Markdown for people and JSON for scheduled collection. One subclass per combination would tie the contents to the file format. Adding a third report would require one subclass for each supported format, and adding a renderer would repeat work across all existing reports. The two kinds of changes have different owners and release schedules.

## Pattern and boundary

Bridge joins two independently changing families through composition. The `Report` abstraction controls the public export operation and report variants provide the title and rows. `ReportRenderer` is the implementation interface that describes the lower-level rendering capability. The concrete renderers encode the same report structure in different formats. The caller chooses one report type and one renderer, and the report delegates formatting through that interface. In this example the contract between the two sides is a title plus a sequence of labeled numeric rows.

## TypeScript example

Two reports and two renderers are exercised in all four pairings. Each report supplies its content once. A formatting change belongs to the corresponding renderer, and a calculation change belongs to the corresponding report.

```typescript
type ReportRow = readonly [label: string, value: number];

interface ReportRenderer {
  render(title: string, rows: readonly ReportRow[]): string;
}

abstract class Report {
  constructor(private readonly renderer: ReportRenderer) {}
  protected abstract title(): string;
  protected abstract rows(): readonly ReportRow[];

  export(): string {
    return this.renderer.render(this.title(), this.rows());
  }
}

class StorageReport extends Report {
  protected title(): string {
    return "Storage";
  }

  protected rows(): readonly ReportRow[] {
    return [["Used bytes", 1200]];
  }
}

class ReviewReport extends Report {
  protected title(): string {
    return "Review queue";
  }

  protected rows(): readonly ReportRow[] {
    return [["Pending", 3]];
  }
}

class MarkdownRenderer implements ReportRenderer {
  render(title: string, rows: readonly ReportRow[]): string {
    return ["# " + title, ...rows.map(([label, value]) => "- " + label + ": " + value)]
      .join("\n");
  }
}

class JsonRenderer implements ReportRenderer {
  render(title: string, rows: readonly ReportRow[]): string {
    return JSON.stringify({ title, rows });
  }
}

const markdown = new MarkdownRenderer();
const json = new JsonRenderer();

if (new StorageReport(markdown).export() !== "# Storage\n- Used bytes: 1200" ||
    new ReviewReport(markdown).export() !== "# Review queue\n- Pending: 3") {
  throw new Error("Both report types should work with Markdown");
}
if (new StorageReport(json).export() !== '{"title":"Storage","rows":[["Used bytes",1200]]}' ||
    new ReviewReport(json).export() !== '{"title":"Review queue","rows":[["Pending",3]]}') {
  throw new Error("Both report types should work with JSON");
}
```

## When to use

Use Bridge when both dimensions already vary or when a second dimension has a concrete roadmap. Look for combinations that share a real contract. For example, a new plain-text renderer should be able to represent every existing report using the same title and rows.

### Common use cases

- **Report types and export formats.** Inventory and revenue reports prepare their own domain data while a renderer produces PDF or CSV. A new renderer can serve several reports when they already provide data through a common contract.
- **Tools that work with multiple storage backends.** Synchronization and archival can both work with local disk or object storage. Separate the workflows from the storage implementation when both sides gain variants and the resulting combinations are meaningful.

## When a simpler approach is enough

One exported report with one stable format can use a function. A formatter function passed as a parameter may also suffice if only formatting varies and reports have no common operations. Extract a named implementation interface when the two dimensions need stable contracts and independent implementations.

## Trade-offs

The shared contract adds a design obligation. A graph-only report or an export format with different fidelity requirements can force changes to both sides. Verify real combinations and model required capabilities explicitly. When evolving the interface, assess the cost for each existing report and renderer.

## Practice

Add a `PlainTextRenderer` that puts the title on the first line and emits `label=value` for each row. Verify both existing reports with it, without editing either report class.

## References

- [Bridge — Refactoring.Guru](https://refactoring.guru/design-patterns/bridge)

[← Previous · 06. Adapter](06-adapter.md) · [Next → · 08. Composite](08-composite.md)
