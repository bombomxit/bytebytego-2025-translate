# 22. Template Method

[Contents](../README.md) · [Tiếng Việt](../vi/22-template-method.md)

## Problem

A document export follows a fixed sequence. The service normalizes the title, renders the export, and attaches the document identifier. The text and JSON versions share the normalization and metadata rules. Duplicating the sequence in each exporter makes it easy for a new format to omit a step or apply the steps in a different order.

## Pattern and boundary

The base class owns the sequence in its template method. It calls a protected abstract step that each subclass implements. In this design, `export()` defines the workflow and `render()` defines only the representation. The parent class calls the child-specific behavior at the point established by the workflow.

In TypeScript, a public method can be overridden even when the design treats it as fixed. If keeping the sequence inviolable is a runtime requirement, use a module-level function with injected steps and expose only that function as the entry point.

## TypeScript example

```typescript
type SourceDocument = Readonly<{ id: string; title: string }>;

abstract class DocumentExporter {
  export(document: SourceDocument): { documentId: string; body: string } {
    const title = document.title.trim().replace(/\s+/g, " ");
    const body = this.render(title);
    return { documentId: document.id, body };
  }

  protected abstract render(title: string): string;
}

class TextExporter extends DocumentExporter {
  protected render(title: string): string {
    return title;
  }
}

class JsonExporter extends DocumentExporter {
  protected render(title: string): string {
    return JSON.stringify({ title });
  }
}

const documentToExport = { id: "doc-8", title: "  Release   notes  " };
const text = new TextExporter().export(documentToExport);
const json = new JsonExporter().export(documentToExport);

if (text.documentId !== "doc-8" || text.body !== "Release notes") {
  throw new Error("Text should contain the normalized title and preserve the ID");
}
if (json.documentId !== "doc-8" || json.body !== '{"title":"Release notes"}') {
  throw new Error("JSON should receive the same normalized title");
}
```

## When to use

Use Template Method when related implementations share an order that should evolve in one place, with one or two well-defined points that vary. It fits an inheritance relationship where each subclass already represents a valid specialization of the base.

### Common use cases

- **Importing data from different formats.** The base class always reads, validates, and reports results in the same order. Each subclass converts CSV rows or JSON records into a common representation. Add a format by implementing the reading step while retaining shared validation.
- **Exporting documents through a common workflow.** Exporters normalize the title, render the content, and attach the document ID in the same order. Each subclass supplies rendering for its format. If only one transformation varies and inheritance is unnecessary, pass a rendering function to the shared workflow.

## When a simpler approach is enough

A standalone export function and a formatter callback are usually enough when formatting is the only variation. Choose a Strategy when the caller needs to pick or replace the formatting policy during execution.

## Trade-offs

The shared sequence becomes easier to change. Subclasses depend on the base class's protected API and on the conditions under which it calls each step. Keep hooks narrow and document the data they receive. Treat changing hook order as a change to that contract.

## Practice

Add a Markdown exporter that renders the normalized title as a heading. Confirm the output includes the original document ID and that the text and JSON exporters still pass their checks.

## References

- [Template Method · Refactoring.Guru](https://refactoring.guru/design-patterns/template-method)

[← Previous · 21. Strategy](21-strategy.md) · [Next → · 23. Visitor](23-visitor.md)
