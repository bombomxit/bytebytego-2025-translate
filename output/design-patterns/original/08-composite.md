# 08. Composite

[Contents](../README.md) · [Tiếng Việt](../vi/08-composite.md)

## Problem

An export screen accepts one document or an entire folder. The request must fit a limit on the total input bytes before packaging begins. Folders can contain documents and other folders. The screen, batch worker, and command-line tool all need the same estimate. If each caller navigates the tree itself, support for another kind of export entry can require changes in several places.

## Pattern and boundary

Composite gives leaves and containers a small common interface. In this example `ArchivePart` is the component. The document leaf contributes its own byte count. The folder implements the same operation by asking each child for its count and combining their answers. The client `fitsLimit` works with an `ArchivePart` regardless of depth. Expose operations shared by all parts on this interface. Child management, when needed, belongs on the folder interface.

## TypeScript example

The check on a single document exercises the same size-limit operation as the check on a nested package. The example assumes a nonnegative byte count from trusted metadata for each document and a validated nonnegative limit. Counts, the total, and the limit fit within JavaScript's safe integer range. An empty folder counts as zero. Archive headers, compression, and other output overhead belong in a separate estimate.

```typescript
interface ArchivePart {
  contentBytes(): number;
}

class ArchiveDocument implements ArchivePart {
  constructor(private readonly bytes: number) {}

  contentBytes(): number {
    return this.bytes;
  }
}

class ArchiveFolder implements ArchivePart {
  private readonly children: readonly ArchivePart[];

  constructor(...children: ArchivePart[]) {
    this.children = children;
  }

  contentBytes(): number {
    return this.children.reduce((total, child) => total + child.contentBytes(), 0);
  }
}

function fitsLimit(part: ArchivePart, limitBytes: number): boolean {
  return part.contentBytes() <= limitBytes;
}

const contract = new ArchiveDocument(140);
const empty = new ArchiveFolder();
const bundle = new ArchiveFolder(
  contract,
  new ArchiveFolder(new ArchiveDocument(60), empty),
);

if (!fitsLimit(contract, 140) || empty.contentBytes() !== 0) {
  throw new Error("A document and an empty folder should each be measurable");
}
if (bundle.contentBytes() !== 200 || fitsLimit(bundle, 199)) {
  throw new Error("A nested bundle should include every document");
}
```

## When to use

Use it when your data really forms a hierarchy and an operation on a group has a consistent interpretation derived from its children. Totals, rendering ordered sections, and applying a rule across a subtree are common cases. Adding a new kind of leaf can then stay local as long as it fulfills the existing component contract.

## When a simpler approach is enough

A discriminated union with one recursive function may be clearer when the tree shape is closed and only one operation walks it. A flat list and a sum suffice when grouping has no effect on the domain.

## Trade-offs

A shared interface should avoid promising capabilities that some nodes cannot honor. Traversal visits every entry and can exhaust the call stack on extremely deep trees. This example models a tree of package entries and counts a document each time it is included. If the production model supports shortcuts or links, define how to handle cycles and repeated references before traversing it.

## Practice

Add a leaf for a generated manifest with a known byte count. Nest it inside a folder and prove that the overall limit calculation changes without modifying `ArchiveFolder` or `fitsLimit`.

## References

- [Composite — Refactoring.Guru](https://refactoring.guru/design-patterns/composite)

[← Previous · 07. Bridge](07-bridge.md) · [Next → · 09. Decorator](09-decorator.md)
