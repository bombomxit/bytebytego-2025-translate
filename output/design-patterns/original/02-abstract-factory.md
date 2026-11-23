# 02. Abstract Factory

[Contents](../README.md) · [Tiếng Việt](../vi/02-abstract-factory.md)

## Problem

An office portal sends document envelopes to two archives. Each archive uses its own envelope format and receipt vocabulary. If the export path chooses a writer and a receipt reader independently, a deployment can successfully upload an envelope and fail to interpret the confirmation. A third provider should create one new integration choice for the application.

## Pattern and boundary

`ArchiveFactory` declares creation methods for two related products, `EnvelopeWriter` and `ReceiptReader`. A concrete factory provides both products for one archive. `recordDocument()` takes one factory and obtains the pair through it. Provider selection happens at the application boundary. The use case relies on the product contracts and the compatibility promised by the factory.

## TypeScript example

Strings represent provider-specific wire formats. The caller supplies the receipt that an archive would return after submission. Both pairs produce the same application result shape. The final check models the failure caused by routing a receipt to the wrong integration.

```typescript
interface EnvelopeWriter {
  encode(documentId: string): string
}

interface ReceiptReader {
  read(receipt: string): string
}

interface ArchiveFactory {
  createWriter(): EnvelopeWriter
  createReceiptReader(): ReceiptReader
}

class ArchiveAFactory implements ArchiveFactory {
  createWriter(): EnvelopeWriter {
    return { encode: id => JSON.stringify({ record: id }) }
  }

  createReceiptReader(): ReceiptReader {
    return {
      read(receipt) {
        if (!receipt.startsWith("A-")) throw new Error("Archive A receipt expected")
        return receipt.slice(2)
      },
    }
  }
}

class ArchiveBFactory implements ArchiveFactory {
  createWriter(): EnvelopeWriter {
    return { encode: id => "document=" + encodeURIComponent(id) }
  }

  createReceiptReader(): ReceiptReader {
    return {
      read(receipt) {
        if (!receipt.startsWith("B/")) throw new Error("Archive B receipt expected")
        return receipt.slice(2)
      },
    }
  }
}

function recordDocument(factory: ArchiveFactory, documentId: string, receipt: string) {
  const body = factory.createWriter().encode(documentId)
  const reference = factory.createReceiptReader().read(receipt)
  return { body, reference }
}

const archiveA = new ArchiveAFactory()
const archiveB = new ArchiveBFactory()
const recordA = recordDocument(archiveA, "D 12", "A-401")
if (recordA.body !== '{"record":"D 12"}' || recordA.reference !== "401") {
  throw new Error("Archive A must use the matching pair")
}
const recordB = recordDocument(archiveB, "D 12", "B/811")
if (recordB.body !== "document=D%2012" || recordB.reference !== "811") {
  throw new Error("Archive B must use the matching pair")
}

let rejected = false
try {
  recordDocument(archiveB, "D 12", "A-401")
} catch (error) {
  rejected = error instanceof Error && error.message === "Archive B receipt expected"
}
if (!rejected) throw new Error("A receipt from the wrong family must be rejected")
```

## When to use

Use Abstract Factory when clients need multiple products from one family and mixing families can violate a constraint such as protocol version, provider, or rendering theme. Choose the family once per use case or configuration scope. Dynamic tenant routing still needs an application-level policy to choose the family.

### Common use cases

- **Integrating digital-signature providers.** Each provider has its own components for submitting requests, checking status, and verifying results under the same protocol. Select a factory once per signing transaction so all three steps use the same provider.
- **Themed user-interface components.** Each theme supplies buttons, dialogs, and fields that follow the same visual rules. The pattern helps when components have distinct implementations per theme. Theme variables or palettes suffice when only colors and sizes differ.

## When a simpler approach is enough

If the integration exposes one small object, supply it directly. If all components are already constructed together at startup, pass a typed object containing the collaborators. It keeps the providers together with less creation code. Factory Method serves one overridable creation hook. Abstract Factory groups the creation of related products.

## Trade-offs

- A provider adds a factory implementation and its products. A new product role changes the factory interface and every family.
- The interfaces define product shape. Compatibility needs contract tests because products with the same TypeScript interface can expect different wire formats.
- Set a lifetime for production adapters. A factory can create one per operation or return collaborators that share an application-managed lifetime.

## Practice

Add a third archive whose receipts start with `C-`. Its own receipt must be accepted, an `A-` receipt must be rejected, and `recordDocument()` must work without a new provider branch.

## References

- [Refactoring.Guru · Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)

[← Previous · 01. Factory Method](01-factory-method.md) · [Next → · 03. Builder](03-builder.md)
