# 19. Observer

[Contents](../README.md) · [Tiếng Việt](../vi/19-observer.md)

## Problem

When a document is published, one component updates a local index and another records the revision in a local journal. A future UI may subscribe to refresh its list. Requiring the publisher to know each consumer makes every new reaction a change to the publish path.

## Pattern and boundary

Expose a subscription contract for a typed event. A subject tracks subscriptions and notifies active observers when that event occurs. Each observer owns its reaction. The publisher knows the event shape and the subscription contract.

`DocumentPublisher` is the subject. The index and journal callbacks are observers. Each call to `subscribe` returns a function that releases that subscription. This implementation takes a snapshot of the subscription list when dispatch starts. Subscription changes affect later events, including an event published by a reentrant callback. Delivery is synchronous and in registration order. A throwing callback would interrupt delivery to later observers.

## TypeScript example

```typescript
type DocumentPublished = Readonly<{ documentId: string; revision: number }>;
type PublishedObserver = (event: DocumentPublished) => void;

class DocumentPublisher {
  private readonly observers = new Set<PublishedObserver>();

  subscribe(observer: PublishedObserver): () => void {
    // A wrapper gives each subscription its own identity.
    const subscription = (event: DocumentPublished) => observer(event);
    this.observers.add(subscription);
    return () => { this.observers.delete(subscription); };
  }

  publish(documentId: string, revision: number): void {
    const event = Object.freeze({ documentId, revision });
    for (const observer of [...this.observers]) {
      observer(event);
    }
  }
}

const publisher = new DocumentPublisher();
const indexed: string[] = [];
const journal: number[] = [];

const stopIndexing = publisher.subscribe(event => indexed.push(event.documentId));
publisher.subscribe(event => journal.push(event.revision));

publisher.publish("proposal", 1);
if (indexed.join() !== "proposal" || journal.join() !== "1") {
  throw new Error("Each active observer must receive the first event");
}

stopIndexing();
publisher.publish("minutes", 2);
if (indexed.join() !== "proposal" || journal.join() !== "1,2") {
  throw new Error("Unsubscribing one observer must leave the others active");
}
```

## When to use

Use Observer when independent in-process consumers need the same event and their participants or lifetimes can change. Tie unsubscription to the lifetime of objects such as views.

### Common use cases

- **Reacting to document publication.** The publisher emits an event with the document ID and version. An open list can reload while a counter updates. Independent reactions can subscribe separately. Keep any update required for successful publication in the main workflow.
- **Keeping editor views in sync.** A status bar observes word-count changes while the outline observes heading changes. Release subscriptions when the window closes. Define error handling when other observers must still be notified after one throws.

## When a simpler approach is enough

A single stable reaction is easy to follow as a direct call. Use explicit orchestration when several steps must all finish in a particular order before a use case can succeed.

## Trade-offs

Side effects are less visible at the publication site. Define listener order, reentrancy, and how listener exceptions affect the publisher and other listeners. This example provides neither durable delivery nor automatic retry. Cross-process messaging requires its own delivery contract, including duplicate handling and ordering where those matter.

## Practice

Subscribe the same callback twice and unsubscribe only the first subscription. Publish a new event and check that the callback runs once. Then release both subscriptions and verify that another publication leaves its observed count unchanged.

## References

- [Observer · Refactoring.Guru](https://refactoring.guru/design-patterns/observer)

[← Previous · 18. Memento](18-memento.md) · [Next → · 20. State](20-state.md)
