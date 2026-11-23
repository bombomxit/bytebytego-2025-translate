# 01. Factory Method

[Contents](../README.md) · [Tiếng Việt](../vi/01-factory-method.md)

## Problem

An office portal exports records from an approval workflow. Every export loads rows, normalizes display names, and returns a body along with its media type. The portal starts with plain text and later adds JSON for an integration. The rules used to prepare the source data should stay in one place as new output formats arrive.

## Pattern and boundary

The base creator, `ExportJob`, owns the shared operation `run()`. It calls an overridable `createWriter()` method and then uses the returned product through the `ReportWriter` interface. Each concrete job decides which writer to construct. A route or the application setup chooses the job. The writer works with prepared data independently from the rest of the workflow.

## TypeScript example

Both jobs consume the same unnormalized rows. The checks cover the two output bodies and their media types. The text writer produces a simple display format with one label per line. Use a structured format such as JSON if labels can contain newlines and need to round-trip.

```typescript
type ReportRow = Readonly<{ label: string }>
type ReportFile = Readonly<{ mediaType: string; body: string }>

interface ReportWriter {
  write(rows: readonly ReportRow[]): ReportFile
}

class TextReportWriter implements ReportWriter {
  write(rows: readonly ReportRow[]): ReportFile {
    return {
      mediaType: "text/plain",
      body: rows.map(row => row.label).join("\n"),
    }
  }
}

class JsonReportWriter implements ReportWriter {
  write(rows: readonly ReportRow[]): ReportFile {
    return { mediaType: "application/json", body: JSON.stringify(rows) }
  }
}

abstract class ExportJob {
  protected abstract createWriter(): ReportWriter

  run(rows: readonly ReportRow[]): ReportFile {
    const normalized = rows.map(row => ({ label: row.label.trim() }))
    return this.createWriter().write(normalized)
  }
}

class TextExportJob extends ExportJob {
  protected createWriter(): ReportWriter {
    return new TextReportWriter()
  }
}

class JsonExportJob extends ExportJob {
  protected createWriter(): ReportWriter {
    return new JsonReportWriter()
  }
}

const rows = [{ label: " Purchase " }, { label: "Travel " }]
const textFile = new TextExportJob().run(rows)
if (textFile.mediaType !== "text/plain" || textFile.body !== "Purchase\nTravel") {
  throw new Error("Text export must contain both normalized labels")
}

const jsonFile = new JsonExportJob().run(rows)
if (jsonFile.mediaType !== "application/json" ||
    jsonFile.body !== '[{"label":"Purchase"},{"label":"Travel"}]') {
  throw new Error("JSON export must encode the same normalized rows")
}
```

## When to use

Use Factory Method when a base class already owns a recurring workflow and subclasses need to decide which collaborator it creates. A useful signal is that every new product forces edits to a stable workflow. Keep the factory hook narrow so the base operation can enforce a common product contract.

## When a simpler approach is enough

A small function with a format switch is enough for a fixed list of writers. If the caller can supply a writer or a function that creates one, constructor injection can reuse the same workflow with fewer classes. A static `fromFormat(format)` method is a named factory whose selection logic stays inside that method.

## Trade-offs

- Each new writer requires a concrete creator here. A deep creator hierarchy makes it harder to trace which object runs in production.
- Each export variant can be tested through the public workflow. Normalization still needs a shared test because it affects all writers.
- Decide who owns the lifetime of expensive products. The example creates a stateless writer on every run, so ownership is local to that run.

## Practice

Add a newline-delimited JSON writer and an export job. Verify the media type and check that two input rows produce two independently parseable JSON lines with trimmed labels. Keep `ExportJob.run()` intact.

## References

- [Refactoring.Guru · Factory Method](https://refactoring.guru/design-patterns/factory-method)

[Next → · 02. Abstract Factory](02-abstract-factory.md)
