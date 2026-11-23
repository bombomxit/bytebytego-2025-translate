# 03. Builder

[Contents](../README.md) · [Tiếng Việt](../vi/03-builder.md)

## Problem

A document team prepares a release package with a heading, an optional summary, and an ordered checklist. The same package is used as a structured result for automation and as plain text for reviewers. The order and completeness checks follow the same rules in both outputs. As the package gains optional sections, wiring each output separately makes it easy to omit a step in one of them.

## Pattern and boundary

The `PackageBuilder` interface names the assembly steps. `assemblePackage()` acts as the director by applying the same sequence to either builder. `StructuredPackageBuilder` and `TextPackageBuilder` decide how to represent the steps and expose their own result accessors. The director owns the recipe and the builders own representation. The caller supplies a fresh builder for each result.

## TypeScript example

The example checks that the two builders preserve item order and that the shared recipe rejects an empty checklist. The structured builder returns a copy of the checklist so the returned result has its own array.

```typescript
type PackageDraft = Readonly<{
  title: string
  summary?: string
  checks: readonly string[]
}>

interface PackageBuilder {
  setTitle(title: string): void
  setSummary(summary: string): void
  addCheck(check: string): void
}

function assemblePackage(draft: PackageDraft, builder: PackageBuilder): void {
  if (!draft.title.trim() || draft.checks.length === 0) {
    throw new Error("A title and at least one check are required")
  }

  builder.setTitle(draft.title)
  if (draft.summary) builder.setSummary(draft.summary)
  for (const check of draft.checks) builder.addCheck(check)
}

class StructuredPackageBuilder implements PackageBuilder {
  private title = ""
  private summary: string | undefined
  private readonly checks: string[] = []

  setTitle(title: string): void {
    this.title = title
  }

  setSummary(summary: string): void {
    this.summary = summary
  }

  addCheck(check: string): void {
    this.checks.push(check)
  }

  build(): PackageDraft {
    return {
      title: this.title,
      ...(this.summary === undefined ? {} : { summary: this.summary }),
      checks: [...this.checks],
    }
  }
}

class TextPackageBuilder implements PackageBuilder {
  private readonly lines: string[] = []

  setTitle(title: string): void {
    this.lines.push(title)
  }

  setSummary(summary: string): void {
    this.lines.push(summary)
  }

  addCheck(check: string): void {
    this.lines.push("- " + check)
  }

  build(): string {
    return this.lines.join("\n")
  }
}

const draft = {
  title: "Policy update",
  summary: "Review before Friday",
  checks: ["Confirm dates", "Notify staff"],
}
const structured = new StructuredPackageBuilder()
const textBuilder = new TextPackageBuilder()
assemblePackage(draft, structured)
assemblePackage(draft, textBuilder)
const result = structured.build()
if (result.title !== draft.title || result.summary !== draft.summary ||
    result.checks.join(",") !== "Confirm dates,Notify staff") {
  throw new Error("The structured package must preserve the draft")
}
if (textBuilder.build() !== "Policy update\nReview before Friday\n- Confirm dates\n- Notify staff") {
  throw new Error("The text package must preserve the recipe order")
}

let rejected = false
try {
  assemblePackage({ title: draft.title, checks: [] }, new TextPackageBuilder())
} catch (error) {
  rejected = error instanceof Error && error.message === "A title and at least one check are required"
}
if (!rejected) throw new Error("The recipe must reject an empty checklist")
```

## When to use

Use Builder when assembling an object takes several steps, or when the same assembly sequence produces different representations. Identify which combinations are valid and make the result available only after the requirements for its particular construction path are satisfied. A director is useful when several clients need the same recipe.

### Common use cases

- **Configuring a recurring report.** The user selects a data source, filters, a format, and a schedule over several steps. A builder accumulates these choices and produces the final configuration once required fields are present, such as a time zone for the delivery schedule.
- **Assembling an export package.** The workflow may include multiple documents, a table of contents, and optional encryption. A builder checks combinations at completion, such as requiring a valid recipient for an encrypted package. A function that takes a configuration object may suffice when all inputs are available at once and checked together.

## When a simpler approach is enough

Start with a typed options object and a validation function if every field is available at once and there is one representation. If the two outputs are simply serializations of a complete, stable domain object, construct that object once and write two serializers. Builders are useful when each representation gains work that is incremental or sensitive to the sequence.

## Trade-offs

- A mutable builder has a lifecycle. This example expects one fresh builder per package. Reusing one without a reset could mix checklist items from different packages.
- A common builder interface makes the recipe reusable. Changing that recipe to require a new operation can affect every concrete builder.
- The shared recipe covers its normal entry point. Check or restrict direct calls too if the product must enforce the same invariants for every caller.

## Practice

Add an optional reviewer note after the summary. Verify that the text builder puts the note before the first checklist item and that the structured builder includes the note only when provided.

## References

- [Refactoring.Guru · Builder](https://refactoring.guru/design-patterns/builder)

[← Previous · 02. Abstract Factory](02-abstract-factory.md) · [Next → · 04. Prototype](04-prototype.md)
