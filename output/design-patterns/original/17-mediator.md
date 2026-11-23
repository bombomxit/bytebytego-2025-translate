# 17. Mediator

[Contents](../README.md) · [Tiếng Việt](../vi/17-mediator.md)

## Problem

An upload dialog has a file picker, a consent checkbox, and a submit button. A file and consent must both be present to enable submission. If each input changes the button independently, each has to learn about the other input. Another dialog may use the same widgets and add a required classification selector.

## Pattern and boundary

Have components notify a mediator about their changes. The mediator owns the interaction rule and updates the affected components. The components are colleagues in the pattern. They can raise their own events without knowing which other components will respond.

The picker and checkbox send events through `UploadFormEvents`. `UploadFormMediator` combines the inputs and updates `SubmitButton`. This mediator is scoped to one form instance. A framework implementation might render the button from derived form state. That preserves the same direction of collaboration when the form owns the rule and its inputs report changes to it.

## TypeScript example

```typescript
interface UploadFormEvents {
  fileSelected(name: string | null): void;
  consentChanged(accepted: boolean): void;
}

class FilePicker {
  constructor(private readonly events: UploadFormEvents) {}

  select(name: string | null): void {
    this.events.fileSelected(name);
  }
}

class ConsentCheckbox {
  constructor(private readonly events: UploadFormEvents) {}

  toggle(accepted: boolean): void {
    this.events.consentChanged(accepted);
  }
}

class SubmitButton {
  enabled = false;
}

class UploadFormMediator implements UploadFormEvents {
  readonly picker = new FilePicker(this);
  readonly consent = new ConsentCheckbox(this);
  readonly submit = new SubmitButton();

  private selectedFile: string | null = null;
  private hasConsent = false;

  fileSelected(name: string | null): void {
    this.selectedFile = name;
    this.updateSubmit();
  }

  consentChanged(accepted: boolean): void {
    this.hasConsent = accepted;
    this.updateSubmit();
  }

  private updateSubmit(): void {
    this.submit.enabled = this.selectedFile !== null && this.hasConsent;
  }
}

const form = new UploadFormMediator();
form.consent.toggle(true);
if (form.submit.enabled) {
  throw new Error("Consent alone must leave the button disabled");
}
form.picker.select("proposal.pdf");
if (!form.submit.enabled) {
  throw new Error("A selected file and consent must enable the button");
}
form.picker.select(null);
if (form.submit.enabled) {
  throw new Error("Removing the file must disable the button again");
}
```

## When to use

Use a mediator when several reusable peers need coordination and changes to one peer currently spread its dependencies across the others. Scope each mediator to a coherent interaction such as one form or workflow step.

### Common use cases

- **Coordinating form fields.** The file picker, consent checkbox, and classification field report changes to a form mediator. It determines when to enable submission, so each field can remain unaware of the others. The server still validates submitted data.
- **Synchronizing editor components.** When the user selects a paragraph, both the toolbar and the properties panel need to update. A mediator receives the selection and coordinates the necessary updates. Scope it to each editor window so a selection does not affect another window.

## When a simpler approach is enough

If a form component already receives the input values and computes one disabled flag, use that component and a simple expression. The boundary matters more than adding another class.

## Trade-offs

Coordination becomes easier to find, but a mediator can accumulate unrelated rules and knowledge of every component. Keep domain rules in their owning model and keep the mediator focused on interactions. A form gate guides the user interface. The server still owns validation for submitted requests.

## Practice

Add a classification selector whose changes go to the mediator. Verify that a file and consent alone leave the button disabled and that selecting a classification enables it without changing either existing input widget.

## References

- [Mediator · Refactoring.Guru](https://refactoring.guru/design-patterns/mediator)

[← Previous · 16. Iterator](16-iterator.md) · [Next → · 18. Memento](18-memento.md)
