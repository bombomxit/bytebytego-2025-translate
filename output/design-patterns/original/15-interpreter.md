# 15. Interpreter

[Contents](../README.md) · [Tiếng Việt](../vi/15-interpreter.md)

## Problem

An administrator configures how the portal selects documents for review. One team requires an external label together with a minimum page count. Another team wants a different combination of those same conditions. The portal needs one vocabulary it can compose into rules and reuse against successive documents.

## Pattern and boundary

Define a small grammar and give its expression nodes evaluation behavior. Here, predicates on labels and page counts are terminal expressions. `And` is a nonterminal expression that delegates to its child expressions, with ordinary short-circuit behavior. The document facts are the context supplied to the whole expression tree. A leaf reads those facts and an operator combines results.

This example builds the expression tree directly. A textual format would introduce a parser to turn text into that tree and reject invalid syntax. Evaluation begins after a valid tree exists. Keeping these steps explicit lets the same evaluator serve a form-based rule editor or a textual format.

## TypeScript example

```typescript
type DocumentFacts = Readonly<{ labels: readonly string[]; pages: number }>;

interface Expression {
  evaluate(facts: DocumentFacts): boolean;
}

class HasLabel implements Expression {
  constructor(private readonly label: string) {}

  evaluate(facts: DocumentFacts): boolean {
    return facts.labels.includes(this.label);
  }
}

class AtLeastPages implements Expression {
  constructor(private readonly threshold: number) {}

  evaluate(facts: DocumentFacts): boolean {
    return facts.pages >= this.threshold;
  }
}

class And implements Expression {
  constructor(
    private readonly left: Expression,
    private readonly right: Expression,
  ) {}

  evaluate(facts: DocumentFacts): boolean {
    return this.left.evaluate(facts) && this.right.evaluate(facts);
  }
}

const needsReview = new And(new HasLabel("external"), new AtLeastPages(10));
if (!needsReview.evaluate({ labels: ["external"], pages: 10 })) {
  throw new Error("A matching label and the inclusive threshold must pass");
}
if (needsReview.evaluate({ labels: ["external"], pages: 9 })) {
  throw new Error("The label alone is insufficient");
}
if (needsReview.evaluate({ labels: ["internal"], pages: 18 })) {
  throw new Error("The page count alone is insufficient");
}
```

## When to use

Use Interpreter when the permitted operations form a small, stable vocabulary, rules can be composed, and the application benefits from evaluating many expressions with the same semantics.

### Common use cases

- **Composing document filters.** Offer predefined operations such as testing labels, comparing page counts, and combining conditions with AND or OR. Each node in the tree evaluates against the document facts. If users can enter text, parse it into the tree before evaluation.
- **Configuring routing conditions.** An administrator combines conditions over submission categories and supported attributes. Bound the operator set, argument types, and expression depth so users can predict the result. Use ordinary expressions in code when the business has only a few fixed rules.

## When a simpler approach is enough

A single hard-coded rule is easiest to read as a Boolean expression. If an application already uses a mature query language for the same purpose, rely on its supported predicates and validation.

## Trade-offs

Every new construct adds semantics to document and test, including its interaction with existing operators. For user-authored rules, validate accepted operators and arguments and set practical limits on rule size and depth. Large grammars or high-volume workloads can justify a dedicated parser, compiler, or rules engine.

## Practice

Add an `Or` expression that accepts the same two children. Check that an external document with nine pages now qualifies, an internal document with ten pages qualifies, and an internal document with nine pages does not.

## References

- [Interpreter · Design Patterns, Gang of Four](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780201633610)

[← Previous · 14. Command](14-command.md) · [Next → · 16. Iterator](16-iterator.md)
