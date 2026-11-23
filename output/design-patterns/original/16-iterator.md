# 16. Iterator

[Contents](../README.md) · [Tiếng Việt](../vi/16-iterator.md)

## Problem

A portal lists the files inside nested folders for exports and reports. Today both callers can walk the tree directly. When folders later require a different internal representation, every caller that follows `entries` would need to change. Some callers also need only the first matching file and should be able to stop the traversal early.

## Pattern and boundary

Let the collection decide which traversal it exposes and give each iterator its own position. A caller reads values through a common traversal interface. It can advance, stop or start another traversal without knowing how the collection stores its entries.

The example uses the JavaScript iteration protocol. `DocumentTree` is iterable and the generator it returns is an iterator. This collection promises to yield file names in depth-first order, preserving the sibling order. Each iterator maintains an independent pending stack. Pushing siblings in reverse preserves their visible order when popping them. The example assumes a finite tree that stays stable during traversal.

## TypeScript example

```typescript
type DocumentEntry =
  | Readonly<{ kind: "file"; name: string }>
  | Readonly<{ kind: "folder"; entries: readonly DocumentEntry[] }>;

class DocumentTree implements Iterable<string> {
  constructor(private readonly root: DocumentEntry) {}

  *[Symbol.iterator](): IterableIterator<string> {
    // Each traversal owns its own stack.
    const pending: DocumentEntry[] = [this.root];
    while (true) {
      const entry = pending.pop();
      if (!entry) return;
      if (entry.kind === "file") {
        yield entry.name;
      } else {
        for (let index = entry.entries.length - 1; index >= 0; index--) {
          pending.push(entry.entries[index]);
        }
      }
    }
  }
}

const tree = new DocumentTree({
  kind: "folder",
  entries: [
    { kind: "file", name: "agenda.md" },
    { kind: "folder", entries: [{ kind: "file", name: "notes.md" }] },
  ],
});
const first = tree[Symbol.iterator]();
const second = tree[Symbol.iterator]();

if (first.next().value !== "agenda.md" || first.next().value !== "notes.md") {
  throw new Error("Traversal must yield files in depth-first order");
}
if (second.next().value !== "agenda.md" || !first.next().done) {
  throw new Error("Iterators must have independent positions and signal exhaustion");
}
if ([...new DocumentTree({ kind: "folder", entries: [] })].length !== 0) {
  throw new Error("An empty folder tree must yield no files");
}
```

## When to use

Use an iterator when callers benefit from a shared traversal contract, early termination, or multiple independent traversals. For remote pages, consider an async iterator and choose how callers cancel in-flight requests and observe errors.

### Common use cases

- **Walking a directory tree on demand.** One traversal can stop as soon as it finds a file, while another can walk the whole tree for a report. Document the order of files and folders and what happens if the tree changes mid-traversal.
- **Reading paginated API data.** An async iterator loads the next page when the caller needs more records. Keep a separate cursor per traversal and propagate API errors to the caller. On early exit, release resources or cancel in-flight requests where needed.

## When a simpler approach is enough

If the data is already an array and the default traversal meets the need, use its built-in iterator with `for...of`. An eager array result is practical when callers need random access to a small result.

## Trade-offs

Consumers may come to depend on iteration order and the behavior of concurrent mutations. Document the rules, such as enumerating an immutable snapshot or rejecting modification while traversal is active. Lazy traversal avoids materializing all yielded values, while this implementation can still hold many pending siblings in memory.

## Practice

Create a folder containing an empty subfolder between two files. Confirm that only the two files are yielded, in their original order, and that breaking after the first file leaves a fresh iterator able to read from the beginning.

## References

- [Iterator · Refactoring.Guru](https://refactoring.guru/design-patterns/iterator)

[← Previous · 15. Interpreter](15-interpreter.md) · [Next → · 17. Mediator](17-mediator.md)
