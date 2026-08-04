# Include OPC AE Gateway Support

The first `OpcAeClient` implementation will support both local Windows COM usage and remote access through the OpenOPC2 gateway. OpenOPC2's primary value is making OPC Classic usable from non-Windows clients, and the queue-first event batch API is compatible with gateway polling.

**Considered Options**

- Ship OPC AE as local Windows COM only first.
- Include Pyro gateway support in the first OPC AE implementation.

**Consequences**

AE event, event batch, filter, category, condition state, and acknowledgement types must be serializable through Pyro from the start. The gateway should expose an AE client proxy separately from the existing DA client proxy.
