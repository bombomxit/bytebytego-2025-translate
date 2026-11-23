# 11. Flyweight

[Contents](../README.md) · [Tiếng Việt](../vi/11-flyweight.md)

## Problem

A workflow canvas renders thousands of nodes. Many nodes have the same shape and border color because those properties depend on the node kind and the theme. Each node still has its own ID and coordinates. If profiling shows duplicate style objects contributing to heap growth, one canonical style object per kind and theme can reduce allocations. A richer style descriptor can make the difference visible even when the canvas contains only a few node kinds.

## Pattern and boundary

Flyweight shares repeated intrinsic state and leaves extrinsic state with each occurrence or its caller. In the example, the frozen `NodeStyle` is intrinsic. The ID and coordinates are extrinsic and remain on `DiagramNode`. `StylePool` is a factory and cache that returns the canonical object for a given key. Include every input that can change those shared fields in the key. Exclude per-node inputs such as the currently selected node, which can change independently.

## TypeScript example

Two nodes of the same kind and theme share object identity and keep separate positions. The checks also show that a different theme yields a different style, and a different kind can change the shape.

```typescript
type NodeKind = "task" | "approval";
type Theme = "light" | "dark";
type NodeStyle = Readonly<{ shape: "box" | "diamond"; border: string }>;

class StylePool {
  private readonly styles = new Map<string, NodeStyle>();

  get(kind: NodeKind, theme: Theme): NodeStyle {
    const key = kind + "/" + theme;
    const existing = this.styles.get(key);
    if (existing !== undefined) return existing;

    const style: NodeStyle = Object.freeze({
      shape: kind === "task" ? "box" : "diamond",
      border: theme === "light" ? "#202020" : "#e0e0e0",
    });
    this.styles.set(key, style);
    return style;
  }
}

type DiagramNode = { id: string; x: number; y: number; style: NodeStyle };
const styles = new StylePool();

function approvalNode(id: string, x: number, theme: Theme): DiagramNode {
  return { id, x, y: 12, style: styles.get("approval", theme) };
}

const first = approvalNode("n1", 10, "light");
const second = approvalNode("n2", 40, "light");
const dark = approvalNode("n3", 75, "dark");

if (first.x === second.x || first.style !== second.style ||
    !Object.isFrozen(first.style)) {
  throw new Error("Each node should keep its position and share an immutable style");
}
const taskStyle = styles.get("task", "light");
if (dark.style === first.style || dark.style.border === first.style.border ||
    taskStyle === first.style || first.style.shape !== "diamond" || taskStyle.shape !== "box") {
  throw new Error("The style key should preserve theme and node kind");
}
```

## When to use

Use the pattern when many live objects repeat stable state and measurements show that sharing it reduces memory or construction cost. This example has only four possible keys. With configuration-driven styles, choose a pool scope that matches the lifetime of the data you intend to share.

### Common use cases

- **Storing styles for a large diagram.** Nodes of the same kind and theme share shape, border color, and font data. Coordinates and selection state remain per node. Shared data should be immutable, and its lookup key must include everything that changes the style.
- **Sharing fonts and icons in a renderer.** Many elements can reference the same icon description while retaining their positions. Measure memory before introducing a shared pool. If the number of variants grows with input data, scope the pool to a document or bound the retained descriptions.

## When a simpler approach is enough

A constant or small static map is sufficient for a few known combinations. Store a scalar or style ID when consumers already resolve it efficiently. Keep the straightforward per-node representation until allocation pressure justifies a pool.

## Trade-offs

Pool lookups add a small amount of work. A pool that retains unique keys indefinitely can consume more memory than it saves. Scope it to the canvas or set a retention policy when keys are dynamic. Shared state needs effective immutability. `Object.freeze` is shallow, so the example only stores primitives in the frozen object.

## Practice

Add a selection outline that follows one node. Draw it from that node's state and verify that toggling selection leaves the shared style and its other users unchanged.

## References

- [Flyweight — Refactoring.Guru](https://refactoring.guru/design-patterns/flyweight)

[← Previous · 10. Facade](10-facade.md) · [Next → · 12. Proxy](12-proxy.md)
