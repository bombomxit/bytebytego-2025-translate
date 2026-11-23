# 18. Memento

[Contents](../README.md) · [Tiếng Việt](../vi/18-memento.md)

## Problem

A drafting tool offers checkpoints while a user revises a document. Today the document has a title and tags. Later it may gain private fields such as a review note or an editing mode. The component that holds checkpoints needs to restore the whole draft without learning how each new field is stored.

## Pattern and boundary

The originator captures its own state and creates a memento. A caretaker keeps the memento and asks the originator to restore it later. The caretaker needs to know which checkpoint to use. The originator retains responsibility for the snapshot format and for applying it.

In the example, `Draft` is the originator. The variable holding `checkpoint` stands in for a history or checkpoint manager. The memento is an opaque token, with the corresponding data stored in a private per-draft `WeakMap`. Another draft cannot use that token. The tag array is copied so changes to values passed by the caller do not silently alter a checkpoint. The values inside that array are immutable strings.

## TypeScript example

```typescript
type DraftMemento = object;

class Draft {
  private title: string;
  private tags: string[];
  private readonly snapshots = new WeakMap<
    DraftMemento,
    Readonly<{ title: string; tags: readonly string[] }>
  >();

  constructor(title: string, tags: readonly string[]) {
    this.title = title;
    this.tags = [...tags];
  }

  revise(title: string, tags: readonly string[]): void {
    this.title = title;
    this.tags = [...tags];
  }

  view(): Readonly<{ title: string; tags: readonly string[] }> {
    return { title: this.title, tags: [...this.tags] };
  }

  save(): DraftMemento {
    const memento = Object.freeze({});
    this.snapshots.set(memento, this.view());
    return memento;
  }

  restore(memento: DraftMemento): boolean {
    const snapshot = this.snapshots.get(memento);
    if (!snapshot) return false;
    this.revise(snapshot.title, snapshot.tags);
    return true;
  }
}

const draft = new Draft("Agenda", ["planning"]);
const checkpoint = draft.save();
draft.revise("Published agenda", ["public"]);

if (!draft.restore(checkpoint)) {
  throw new Error("The draft must accept its own checkpoint");
}
const restored = draft.view();
if (restored.title !== "Agenda" || restored.tags.join() !== "planning") {
  throw new Error("Restore must recover both the title and the tag collection");
}

const otherDraft = new Draft("Notes", []);
if (otherDraft.restore(checkpoint) || otherDraft.view().title !== "Notes") {
  throw new Error("A checkpoint must only restore its owner");
}
```

## When to use

Use Memento when restore should recover a coherent private state and several fields may change together. A checkpoint fits cases where edits support rollback at snapshots, including edits that lack an operation-specific inverse.

## When a simpler approach is enough

If only one scalar value must be restored, keep the previous value in the code that owns it. A normal immutable value can already serve as a snapshot when its complete shape is an appropriate public contract.

## Trade-offs

A full snapshot consumes memory in proportion to the data retained. Cap a growing history or use a representation that shares immutable data if checkpoint size becomes significant. This example stores volatile checkpoints bound to one draft instance. Persistent checkpoints need a stable representation, migration rules, and storage whose access policy matches the data.

## Practice

Add a locale field to the draft, then save a checkpoint before changing both the locale and title. Confirm that restore recovers both while the code that holds the checkpoint stays the same.

## References

- [Memento · Refactoring.Guru](https://refactoring.guru/design-patterns/memento)

[← Previous · 17. Mediator](17-mediator.md) · [Next → · 19. Observer](19-observer.md)
