# Separate OPC AE Configuration

OpenOPC2 will add separate configuration fields for OPC Alarms and Events instead of reusing the existing Data Access server defaults. DA and AE servers often have different ProgIDs, so `OpcAeClient.connect()` should default from AE-specific configuration such as `OPC_AE_SERVER`.

**Considered Options**

- Reuse `OPC_SERVER` and existing DA defaults for AE.
- Add AE-specific configuration fields.

**Consequences**

The AE client and gateway can share host and gateway settings with DA where appropriate, but AE server identity should be configured independently to avoid accidental DA/AE cross-wiring.
