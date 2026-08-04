# Queue-First OPC AE Subscriptions

`OpcAeClient` subscriptions will expose event notifications through an iterator or queue-first API, with direct callbacks only as an optional convenience. OPC AE delivers notifications through COM callbacks, and those callbacks should do minimal work; enqueueing event batches keeps user processing outside the COM callback path and makes the same interface usable through the Pyro gateway.

**Considered Options**

- Make user callbacks the primary API.
- Make subscription queues and iterators the primary API.

**Consequences**

The COM event sink should translate incoming `OnEvent` payloads into Python event objects and enqueue them quickly. Gateway clients should consume queued events by polling or streaming-style iterator calls rather than registering arbitrary remote callbacks.
