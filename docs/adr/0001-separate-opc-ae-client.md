# Separate OPC AE Client

OpenOPC2 will expose OPC Alarms and Events through a separate `OpcAeClient` rather than expanding `OpcDaClient` into a combined OPC Classic client. OPC Data Access and OPC Alarms and Events have different domain models, lifecycles, and server interfaces: DA centers on groups, items, reads, and writes, while AE centers on event subscriptions, filters, callbacks, condition state, and acknowledgements.

**Considered Options**

- Expand `OpcDaClient` into a combined DA/AE client.
- Add a dedicated `OpcAeClient`.

**Consequences**

`OpcAeClient` can share gateway and configuration infrastructure with the existing DA client, but AE concepts should not be represented as DA tags or DA groups.
