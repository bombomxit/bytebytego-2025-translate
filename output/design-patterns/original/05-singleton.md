# 05. Singleton

[Contents](../README.md) · [Tiếng Việt](../vi/05-singleton.md)

## Problem

A desktop document intake app controls one physical scanner. The import screen and a background task run in the same application instance and must coordinate access to that device. If each creates its own in-memory gate, both can see an idle scanner and start a scan. Here uniqueness comes from one resource and one agreed owner.

## Pattern and boundary

`ScannerGate` restricts ordinary construction through a private constructor and exposes one shared instance through `getInstance()`. That instance owns the occupancy flag and hands out a release function to the current holder. It governs callers of this class inside the same loaded module instance. Browser tabs, workers, separate processes, and distinct module copies can each have their own instance.

## TypeScript example

The example assumes a single JavaScript execution context. `tryAcquire()` updates the flag synchronously, so a second call in that context sees the claim immediately. Calling an old release function twice cannot unlock a later claim. Real scan callers would release the claim in a `finally` block after the operation settles.

```typescript
class ScannerGate {
  static readonly #instance = new ScannerGate()
  #occupied = false

  private constructor() {}

  static getInstance(): ScannerGate {
    return ScannerGate.#instance
  }

  tryAcquire(): (() => void) | undefined {
    if (this.#occupied) return undefined
    this.#occupied = true

    let released = false
    return () => {
      if (released) return
      released = true
      this.#occupied = false
    }
  }
}

const importScreen = ScannerGate.getInstance()
const backgroundJob = ScannerGate.getInstance()
const releaseImport = importScreen.tryAcquire()
if (!releaseImport || importScreen !== backgroundJob ||
    backgroundJob.tryAcquire() !== undefined) {
  throw new Error("Both entry points must coordinate through the same gate")
}

releaseImport()
const releaseBackground = backgroundJob.tryAcquire()
if (!releaseBackground) throw new Error("Releasing must let the next caller acquire")

releaseImport()
if (importScreen.tryAcquire() !== undefined) {
  throw new Error("An old release function must not unlock a later claim")
}
releaseBackground()
```

## When to use

Consider Singleton when uniqueness is an intentional invariant inside a documented ownership scope and multiple entry points must find the same owner. State what process or container creates it, when it is initialized, and who handles shutdown if it owns a resource.

### Common use cases

- **Coordinating work inside one process.** Several entry points submit work to one coordinator so they share a concurrency limit. The uniqueness scope is that process. Enforcing a common limit across processes requires a shared coordination mechanism.
- **Managing an exclusive resource.** If a process may open only one session with a device, a manager can own opening it, granting access to it, and closing it at shutdown. When the application has a clear startup entry point, creating the manager there and injecting it where needed is often sufficient.

## When a simpler approach is enough

When you control application startup, construct one object there and inject the same instance into the import screen and background task. This keeps dependency and lifetime visible. A stateless utility can be a module function. If independent processes have to share a scanner, use coordination with the actual device driver or another owner visible to all contenders.

## Trade-offs

- A static accessor hides dependencies at call sites and shared state may carry across tests in the same runtime.
- Requiring one owner can simplify coordination. Treating a general mutable object as a global service can create accidental coupling between features.
- A single in-memory gate only models the stated runtime scope. It cannot enforce device-level exclusivity when code elsewhere bypasses that owner.

## Practice

Write a `scan()` wrapper that acquires the gate and releases it with `finally`. Make the first scan throw and verify that a later scan can still acquire the gate.

## References

- [Refactoring.Guru · Singleton](https://refactoring.guru/design-patterns/singleton)

[← Previous · 04. Prototype](04-prototype.md) · [Next → · 06. Adapter](06-adapter.md)
