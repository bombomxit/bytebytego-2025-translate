# 23. Visitor

[Contents](../README.md) · [Tiếng Việt](../vi/23-visitor.md)

## Problem

A document editor stores a tree of section, paragraph, and attachment nodes. It needs an attachment-size report now and a broken-link report next. With a stable node model and several new reports, putting every report method on each node would spread report changes across the editor's model.

## Pattern and boundary

Each element exposes `accept(visitor)` and calls the visitor method for its concrete type. The element's implementation selects the typed method. The visitor supplied by the caller determines which implementation runs. Together those two dispatches select an operation for a particular element kind.

Here the section accepts the visitor and forwards traversal to its children. The size operation lives in one visitor implementation. Decide who walks the tree early. If later operations need to prune subtrees or control ordering, give them a traversal API with that control.

## TypeScript example

```typescript
interface DocumentElement {
  accept(visitor: DocumentVisitor): void;
}

interface DocumentVisitor {
  visitSection(section: Section): void;
  visitParagraph(paragraph: Paragraph): void;
  visitAttachment(attachment: Attachment): void;
}

class Section implements DocumentElement {
  constructor(readonly children: readonly DocumentElement[]) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitSection(this);
    for (const child of this.children) child.accept(visitor);
  }
}

class Paragraph implements DocumentElement {
  constructor(readonly text: string) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitParagraph(this);
  }
}

class Attachment implements DocumentElement {
  constructor(readonly bytes: number) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitAttachment(this);
  }
}

class AttachmentSize implements DocumentVisitor {
  totalBytes = 0;

  visitSection(_section: Section): void {}

  visitParagraph(_paragraph: Paragraph): void {}

  visitAttachment(attachment: Attachment): void {
    this.totalBytes += attachment.bytes;
  }
}

const tree = new Section([
  new Paragraph("Release notes"),
  new Attachment(200),
  new Section([new Attachment(550)]),
]);

const report = new AttachmentSize();
tree.accept(report);
if (report.totalBytes !== 750) throw new Error("Expected 750 attachment bytes");

const paragraph = new Paragraph("No attachments");
const emptyReport = new AttachmentSize();
paragraph.accept(emptyReport);
if (emptyReport.totalBytes !== 0) throw new Error("Expected zero attachment bytes");
```

## When to use

Use Visitor when the set of element types is stable and operations that handle those types in different ways are added frequently. A visitor interface makes each operation account explicitly for supported elements.

## When a simpler approach is enough

A discriminated union and an exhaustive switch may be clearer when there are few operations and the element model consists of plain data. A loop with a callback often suffices when it applies the same work to every element.

## Trade-offs

Adding an operation costs one new visitor. Adding an element kind changes the visitor interface and can require an update to every visitor. Stateful visitors also need a clear lifetime, so this example creates one instance per report.

## Practice

Implement a second visitor that counts paragraphs. The example tree should produce one paragraph and still report 750 attachment bytes. The node classes should support both visitors as written.

## References

- [Visitor · Refactoring.Guru](https://refactoring.guru/design-patterns/visitor)

[← Previous · 22. Template Method](22-template-method.md) · [Next → · How to choose a design pattern](24-chon-mau.md)
