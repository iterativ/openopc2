# Defer OPC AE Enable and Disable Controls

The first `OpcAeClient` interface will include event subscriptions, discovery queries, `get_condition_state()`, and acknowledgement methods, but will not expose enable or disable operations for areas or sources. Enable and disable methods alter server behavior and carry operational risk, while subscription, condition state, and acknowledgement are enough to build a useful alarm client first.

**Considered Options**

- Expose all `IOPCEventServer` methods immediately.
- Ship the first AE interface without enable and disable controls.

**Consequences**

The implementation should still leave room for later `enable_condition_by_source`, `disable_condition_by_source`, `enable_condition_by_area`, and `disable_condition_by_area` methods, including the OPC AE 1.10 optional `IOPCEventServer2` variants.
