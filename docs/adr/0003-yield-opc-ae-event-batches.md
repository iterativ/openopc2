# Yield OPC AE Event Batches

`OpcAeSubscription` will yield `AeEventBatch` objects as its primary delivery unit rather than yielding only individual `AeEvent` objects. OPC AE `OnEvent` callbacks include subscription-level metadata such as refresh markers, last-refresh markers, and keep-alive calls with zero events; preserving that callback boundary keeps the public API faithful to the protocol.

**Considered Options**

- Flatten callback payloads into individual events.
- Preserve callback payloads as event batches.

**Consequences**

Convenience methods may flatten batches into individual events, but the primary API must expose batch metadata so clients can synchronize condition state correctly.
