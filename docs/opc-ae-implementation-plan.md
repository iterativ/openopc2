# OPC AE Implementation Plan

This plan adds OPC Alarms and Events support to OpenOPC2 through a dedicated `OpcAeClient`, raw Windows COM bindings, queue-first event delivery, and Pyro gateway support.

## Decisions Already Made

- Use a separate `OpcAeClient`; do not merge AE into `OpcDaClient`.
- Use a raw COM binding dependency for AE, likely `comtypes`.
- Make subscriptions queue-first and iterator-friendly.
- Yield `AeEventBatch` as the primary delivery unit.
- Support acknowledgement through both `AeEvent` and explicit acknowledgement references.
- Include `get_condition_state()` and acknowledgement in the first interface.
- Defer enable and disable condition controls.
- Include gateway support in the first implementation.
- Keep subscription refresh explicit by default, with `refresh=True` as an opt-in convenience.
- Use Pythonic typed public discovery methods while referencing OPC AE spec method names in docstrings and internals.
- Make event attributes ID-keyed, with optional metadata when known.
- Require explicit returned-attribute selection per category, with a helper for selecting all.
- Add AE-specific configuration fields.
- Target both 32-bit and 64-bit Python where the AE COM server registration supports the process bitness.
- Include a minimal CLI for AE discovery, subscription, and refresh; defer CLI acknowledgement.

## Public API Shape

```python
from openopc2.ae_client import OpcAeClient
from openopc2.ae_types import AeEventType, AeFilter

client = OpcAeClient()
client.connect("Matrikon.OPC.AlarmEvent", "localhost")

subscription = client.subscribe(
    filter=AeFilter(
        event_types={AeEventType.CONDITION},
        low_severity=600,
        high_severity=1000,
        areas=["Plant1"],
    ),
    returned_attributes={10: [1001, 1002]},
    buffer_time=1000,
    max_size=100,
    refresh=False,
)

subscription.refresh()

for batch in subscription.batches(timeout=5):
    for event in batch.events:
        if event.ack_required:
            client.ack(event, acknowledger_id="operator-1", comment="checked")
```

Convenience refresh:

```python
events = client.refresh(
    filter=AeFilter(event_types={AeEventType.CONDITION}),
    timeout=10,
)
```

This convenience must be implemented using an AE subscription refresh. It is not event history replay.

## Phase 1: Domain Types

Add `openopc2/ae_types.py`.

Core types:

- `AeEventType`
- `AeChangeMask`
- `AeConditionState`
- `AeFilterMask`
- `AeFilter`
- `AeCategory`
- `AeAttribute`
- `AeEvent`
- `AeEventBatch`
- `AeAcknowledgementReference`
- `AeConditionStateSnapshot`
- `AeSubscriptionState`

Design notes:

- `AeEvent.attributes` should be `Mapping[int, Any]`.
- Attribute IDs are authoritative.
- Optional attribute metadata can be carried as `Mapping[int, str]` or a richer metadata map.
- `AeAcknowledgementReference` must contain `source`, `condition_name`, `active_time`, and `cookie`.
- Pyro serializers must be registered for all custom AE types that cross the gateway.

## Phase 2: Configuration

Extend `OpenOpcConfig` with AE-specific settings.

Suggested fields:

- `OPC_AE_SERVER`
- `OPC_AE_CLIENT`
- `OPC_AE_TIMEOUT`

Reuse existing host and gateway settings where they already mean the same thing:

- `OPC_HOST`
- `OPC_GATE_HOST`
- `OPC_GATE_PORT`

Do not reuse `OPC_SERVER` as the default AE server ProgID.

## Phase 3: COM Binding Layer

Add `openopc2/ae_com.py`.

Responsibilities:

- Initialize COM on Windows.
- Connect to the AE server ProgID.
- Expose low-level wrappers around OPC AE custom interfaces.
- Translate COM structs and HRESULT arrays into Python domain types.
- Hide raw COM details from `OpcAeClient`.

Initial methods:

- `connect(server, host)`
- `disconnect()`
- `get_status()`
- `query_available_filters()`
- `query_event_categories(event_types)`
- `query_event_attributes(category_id)`
- `query_condition_names(category_id)`
- `query_subcondition_names(condition_name)`
- `query_source_conditions(source)`
- `create_subscription(active, buffer_time, max_size, client_handle)`
- `get_condition_state(source, condition_name, attribute_ids)`
- `ack_condition(references, acknowledger_id, comment)`

Deferred methods:

- `enable_condition_by_source`
- `disable_condition_by_source`
- `enable_condition_by_area`
- `disable_condition_by_area`
- OPC AE 1.10 optional `IOPCEventServer2` enable-state methods

## Phase 4: Subscription Runtime

Add `openopc2/ae_subscription.py`.

Responsibilities:

- Own the COM subscription object.
- Own the COM connection point sink.
- Convert `OnEvent` callbacks into `AeEventBatch`.
- Enqueue batches quickly inside the COM callback.
- Expose `batches(timeout=None)`, `next_batch(timeout=None)`, and `refresh()`.
- Expose `close()` and context-manager behavior.

Callback rules:

- The COM sink must return quickly.
- The sink should not call user code directly.
- Callback payloads with `dwCount == 0` must still become an `AeEventBatch` so keep-alives are visible.
- `refresh` and `last_refresh` must be preserved.

## Phase 5: High-Level Client

Add `openopc2/ae_client.py`.

Public methods:

- `connect(opc_server=None, opc_host="localhost")`
- `close()`
- `info()`
- `available_filters()`
- `categories(event_types)`
- `attributes(category_id)`
- `condition_names(category_id)`
- `subcondition_names(condition_name)`
- `source_conditions(source)`
- `subscribe(filter=None, returned_attributes=None, buffer_time=0, max_size=0, active=True, refresh=False)`
- `refresh(filter=None, returned_attributes=None, timeout=None)`
- `get_condition_state(source, condition_name, attribute_ids=None)`
- `ack(event, acknowledger_id, comment="")`
- `ack_condition(source, condition_name, active_time, cookie, acknowledger_id, comment="")`

Design notes:

- `ack(event, ...)` should reject non-condition events and condition events without a complete acknowledgement reference.
- `refresh()` should create a temporary subscription, request refresh, collect until `last_refresh`, close the subscription, and return condition events or batches depending on final API choice.
- Public method docstrings should reference the corresponding OPC AE method names.

## Phase 6: Gateway Support

Update gateway modules:

- `openopc2/gateway_server.py`
- `openopc2/gateway_proxy.py`

Add:

- `OpenOpcGatewayServer.create_ae_client(...)`
- `OpenOpcGatewayProxy.get_opc_ae_client_proxy()`
- serializer registration for AE dataclasses and exceptions

Gateway delivery model:

- Remote clients should poll `next_batch(timeout)` or iterate batches.
- Do not marshal arbitrary user callbacks over Pyro.
- Keep AE proxy separate from the DA proxy.

## Phase 7: CLI

Add minimal AE commands to `openopc2/cli.py`.

Suggested commands:

```shell
python -m openopc2 ae-categories
python -m openopc2 ae-subscribe --event-type condition --severity-min 600
python -m openopc2 ae-refresh --event-type condition --severity-min 600
```

Include options:

- `--protocol-mode`
- `--opc-ae-server`
- `--opc-host`
- `--gateway-host`
- `--gateway-port`
- `--event-type`
- `--category`
- `--severity-min`
- `--severity-max`
- `--area`
- `--source`
- `--timeout`
- `--output-csv`

Defer CLI acknowledgement until there is a careful design for passing an acknowledgement reference exactly.

## Phase 8: Tests

Unit tests:

- AE dataclass serialization and deserialization.
- Filter bitmask conversion.
- Event type and condition state bitmask conversion.
- `AeEvent` to `AeAcknowledgementReference`.
- `ack()` validation for invalid event types and missing ack fields.
- Subscription queue behavior for normal batches, refresh batches, last-refresh batches, and keep-alives.
- Client-level `refresh()` closes temporary subscriptions.

Integration-style tests with fakes:

- Fake `ae_com` object that simulates discovery methods.
- Fake subscription callback sink that enqueues `AeEventBatch`.
- Gateway serializer round trips for AE objects.

Real-server tests:

- Keep these opt-in behind environment variables.
- Require Windows and a configured AE server.
- Validate categories, subscription callback delivery, refresh, and acknowledgement only when the server supports condition events.

## Phase 9: Documentation

Update:

- `README.md`
- `CLI.md`
- installation notes
- gateway documentation

Document clearly:

- OPC AE local COM requires Windows.
- Python bitness must match the registered AE COM server.
- Gateway is the preferred cross-platform path.
- Refresh is not event history replay.
- Event attributes are vendor-specific and selected explicitly.
- AE server ProgID is configured separately from DA server ProgID.

## Open Implementation Risks

- `comtypes` custom COM interface definitions may require hand-written IDL mappings for OPC AE structs and interfaces.
- Some AE servers implement only simple events and may return `E_NOTIMPL` for condition methods.
- Some filter criteria may be ignored by servers; `available_filters()` and `subscription.get_filter()` should make this visible.
- Condition timestamps and COM `FILETIME` conversion must be exact because acknowledgement depends on them.
- Queue overflow policy is not yet decided. Start with an unbounded queue or configurable max size, then make overflow behavior explicit before production use.
