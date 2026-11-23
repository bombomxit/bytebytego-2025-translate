# 14. Command

[Contents](../README.md) · [Tiếng Việt](../vi/14-command.md)

## Problem

An editor lets the toolbar, keyboard shortcuts, and menus change a draft. It also needs a single Undo action that reverses the most recent edit, regardless of the entry point that initiated it. The next edit may toggle a section flag or move a paragraph, so the Undo button cannot depend on a list of all edit types.

## Pattern and boundary

Represent a request as an object with an execution contract. The sender creates a command with its target and arguments. An invoker executes that command and applies a shared policy such as storing completed edits. The receiver is the draft that changes.

In the example, `RenameDraft` captures the previous title when it executes. This timing matters because the draft can change between creating a command and running it. `EditHistory` depends on `EditCommand` and undoes commands in reverse execution order. The example creates a fresh command for every edit. It assumes one editor owns the history and applies its edits sequentially.

## TypeScript example

```typescript
interface EditCommand {
  execute(): void;
  undo(): void;
}

class Draft {
  constructor(private title: string) {}

  getTitle(): string {
    return this.title;
  }

  rename(title: string): void {
    this.title = title;
  }
}

class RenameDraft implements EditCommand {
  private previousTitle: string | undefined;

  constructor(private readonly draft: Draft, private readonly title: string) {}

  execute(): void {
    this.previousTitle = this.draft.getTitle();
    this.draft.rename(this.title);
  }

  undo(): void {
    if (this.previousTitle === undefined) {
      throw new Error("Rename must run before it can be undone");
    }
    this.draft.rename(this.previousTitle);
    this.previousTitle = undefined;
  }
}

class EditHistory {
  private readonly completed: EditCommand[] = [];

  run(command: EditCommand): void {
    command.execute();
    this.completed.push(command);
  }

  undoLast(): boolean {
    const command = this.completed.at(-1);
    if (!command) return false;
    command.undo();
    this.completed.pop();
    return true;
  }
}

const draft = new Draft("Draft");
const commandHistory = new EditHistory();
commandHistory.run(new RenameDraft(draft, "Proposal"));
commandHistory.run(new RenameDraft(draft, "Signed proposal"));
if (draft.getTitle() !== "Signed proposal") {
  throw new Error("The last rename should be visible");
}
if (!commandHistory.undoLast() || draft.getTitle() !== "Proposal") {
  throw new Error("Undo should restore the title immediately before the last edit");
}
if (!commandHistory.undoLast() || draft.getTitle() !== "Draft" || commandHistory.undoLast()) {
  throw new Error("Undo must follow reverse execution order and stop on empty history");
}
```

## When to use

Use commands when operations need a shared execution policy such as undo, scheduling, or recording, and the operations evolve independently. In a durable job system, store a versioned description of the request and resolve the handler when processing it.

### Common use cases

- **Undoing edits.** Renaming, moving, and tagging a document are commands with a common execution contract. The history records commands after successful execution. Each command captures the old value when it runs so changes can be undone in the right order.
- **Queueing report exports.** Store the command type, request ID, arguments, and command schema version so a worker can find the right handler. Define what happens if it receives the same command again. For example, enforce uniqueness by request ID to prevent two workers from creating the same report.

## When a simpler approach is enough

If a button calls one operation immediately and the application has no execution policy to share, a direct function call keeps the flow easy to follow.

## Trade-offs

Each operation must define how it executes and, when relevant, how it reverses its effects. Undo only works while the captured information and receiver state support it. A delivered email, for example, may require a separate compensating action. Retrying a persisted command also requires a policy for duplicate delivery and partial failure.

## Practice

Add an edit that toggles a draft's archived flag. Run a rename and then the toggle through the same history. The first undo should restore the flag and keep the new title, and the second should restore the original title.

## References

- [Command · Refactoring.Guru](https://refactoring.guru/design-patterns/command)

[← Previous · 13. Chain of Responsibility](13-chain-of-responsibility.md) · [Next → · 15. Interpreter](15-interpreter.md)
