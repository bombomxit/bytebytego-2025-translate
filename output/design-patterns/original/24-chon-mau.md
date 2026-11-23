# How to choose a design pattern

[Contents](../README.md) · [Tiếng Việt](../vi/24-chon-mau.md)

## Start with the change

1. Name a change the code has already faced or will face soon. “A second preview provider returns a different result shape” is specific enough to discuss.
2. Locate the responsibility that should absorb it. For the preview provider, put conversion at the integration boundary and define the result the rest of the app expects.
3. Try the smallest useful design. For a single provider, a mapping function can do the job. Move to a reusable adapter when the application actually needs a contract that multiple implementations can satisfy.
4. Verify the next change. Introduce one new variant and check which files change, which contract tests still pass, and what new failure modes need tests.

## Find a pattern by situation

Match the situation first, then check the chapter's simpler approach and trade-offs.

| Situation | Pattern |
| --- | --- |
| An existing workflow must let subclasses choose the component it creates. | [Factory Method](01-factory-method.md) |
| Products provided by one vendor must work together. | [Abstract Factory](02-abstract-factory.md) |
| Construction has several steps and only some combinations are valid. | [Builder](03-builder.md) |
| A configured instance is the starting point for independent copies. | [Prototype](04-prototype.md) |
| Exactly one owner is required in a well-defined runtime scope. | [Singleton](05-singleton.md) |
| An API you cannot change needs to satisfy your application's interface. | [Adapter](06-adapter.md) |
| Two dimensions of a component vary independently. | [Bridge](07-bridge.md) |
| A leaf and a subtree should support the same operation. | [Composite](08-composite.md) |
| Multiple optional duties wrap the same core operation. | [Decorator](09-decorator.md) |
| Callers need a stable entry point into a multi-step subsystem. | [Facade](10-facade.md) |
| Many objects repeat the same intrinsic, shareable data. | [Flyweight](11-flyweight.md) |
| A stand-in must control when the real object is accessed. | [Proxy](12-proxy.md) |
| An ordered set of handlers can handle, pass on, or stop a request. | [Chain of Responsibility](13-chain-of-responsibility.md) |
| An operation must be represented as a value for later execution. | [Command](14-command.md) |
| A small grammar describes combinations of business rules. | [Interpreter](15-interpreter.md) |
| Clients need to traverse a collection without knowing its storage layout. | [Iterator](16-iterator.md) |
| A group of components needs one owner for its coordination rules. | [Mediator](17-mediator.md) |
| An object's previous state must be restored while preserving encapsulation. | [Memento](18-memento.md) |
| A local change has multiple independent listeners. | [Observer](19-observer.md) |
| An object's lifecycle phase controls accepted actions and transitions. | [State](20-state.md) |
| The caller chooses one of several algorithms with the same contract. | [Strategy](21-strategy.md) |
| Related subclasses vary individual steps in an inherited workflow. | [Template Method](22-template-method.md) |
| A stable element model gains new operations frequently. | [Visitor](23-visitor.md) |

## Compare nearby patterns

- **Strategy and State.** The caller supplies a Strategy for a particular calculation or policy. State represents a phase in the object's lifecycle and governs what can happen and which phase follows.
- **Adapter, Facade, and Bridge.** Adapter makes a foreign interface fit an interface the client expects. Facade gives callers a higher-level entry point to a subsystem. Bridge separates two dimensions expected to vary independently.
- **Decorator and Proxy.** Decorator adds duties that can be composed while maintaining the interface. Proxy stands in for the same subject and can decide how or when to hand off to it.
- **Factory Method, Abstract Factory, and Builder.** Factory Method gives each creator subclass a creation point to override. Abstract Factory supplies a consistent family of products. Builder assembles one product through steps.
- **Observer and publish–subscribe.** The Observer example calls listeners in the same process. Across services, a broker, delivery guarantees, idempotency, and failure handling belong in the design.
- **Strategy and Template Method.** Strategy delegates a policy to a component that the caller can supply. Template Method uses inheritance to let subclasses implement defined steps in a base workflow.
- **Command and Memento.** A Command captures what to execute. A Memento captures an object's state at a time. An undo feature can use a reversible command, a memento, or both.

## Glossary

| Term | Tiếng Việt | Meaning in this book |
| --- | --- | --- |
| Composition | Kết hợp đối tượng | An object delegates work to collaborators it holds or receives. |
| Inheritance | Kế thừa | A subclass specializes a base type and may inherit implementations. |
| Contract | Hợp đồng | The behavior callers can rely on, including inputs, outputs, errors and side effects. |
| Boundary | Ranh giới | The point where responsibility or a dependency changes hands. |
| Lifecycle | Vòng đời | Which phases an object can enter and when its resources are created or released. |
| Invariant | Bất biến | A rule that must hold for every valid state. |

[← Previous · 23. Visitor](23-visitor.md)
