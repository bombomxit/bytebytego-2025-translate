# 130 - Key Terms in Domain-Driven Design

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 272-273
- Figures: 1

## Figures

![Key Terms in Domain-Driven Design - figure 1](../assets/130/figure-01.png)

## Original Extracted Text

Have you heard of Domain-Driven Design (DDD), a major software design approach?

DDD was introduced in Eric Evans' classic book "Domain-Driven Design: Tackling Complexity in the
Heart of Software". It explained a methodology to model a complex business. In this book, there is a
lot of content, so I'll summarize the basics.

The composition of domain objects:

   ● Entity: a domain object that has ID and life cycle.

   ● Value Object: a domain object without ID. It is used to describe the property of Entity.

   ● Aggregate: a collection of Entities that are bounded together by Aggregate Root (which is
      also an entity). It is the unit of storage.

The life cycle of domain objects:

   ● Repository: storing and loading the Aggregate.

   ● Factory: handling the creation of the Aggregate.

Behavior of domain objects:

   ● Domain Service: orchestrate multiple Aggregate.

   ● Domain Event: a description of what has happened to the Aggregate. The publication is
      made public so others can consume and reconstruct it.

Congratulations on getting this far. Now you know the basics of DDD. If you want to learn more, I
highly recommend the book. It might help to simplify the complexity of software modeling.

Over to you: do you know how to check the equality of two Value Objects? How about two Entities?
