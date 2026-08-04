# OPC AE Developer Notes

These notes describe the implementation shape behind the OPC Alarms and Events API. For user-facing behavior, see [opc-ae.md](./opc-ae.md).

## Current Implementation State

Implemented:

- AE domain types in `openopc2/ae_types.py`
- Queue-first subscription wrapper in `openopc2/ae_subscription.py`
- Public `OpcAeClient` scaffold in `openopc2/ae_client.py`
- AE-specific configuration fields in `OpenOpcConfig`
- AE serializer registration for gateway use
- Minimal AE CLI commands
- Unit tests with fake AE backends

Not implemented yet:

- Raw Windows OPC AE custom COM binding in `openopc2/ae_com.py`
- COM connection point sink for `IOPCEventSink::OnEvent`
- Real AE gateway integration tests against a running gateway
- Opt-in real-server tests against a vendor AE server

## Module Boundaries

`OpcAeClient` is the public API. It should stay Pythonic and should not expose raw COM structs or HRESULT arrays.

`OpcAeCom` is the low-level COM boundary. It should wrap OPC AE custom interfaces and return domain objects from `ae_types.py`.

`OpcAeSubscription` owns event delivery state. It should expose queued batches and should not execute user callbacks from the COM callback path.

`ae_types.py` owns serializable domain objects. Any AE object crossing Pyro must be registered through `register_ae_serializers()`.

## COM Backend Requirements

The COM backend must support these first-pass methods:

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

The backend should create subscriptions inactive, apply filters and returned attributes, attach the event queue sink, and then activate the subscription. This avoids a short window where an active subscription could deliver unfiltered events.

## Callback Rules

The `IOPCEventSink::OnEvent` implementation must do minimal work:

- Convert `ONEVENTSTRUCT` payloads into `AeEvent` objects.
- Wrap the callback payload in `AeEventBatch`.
- Enqueue the batch.
- Return `S_OK`.

Do not call user code directly from `OnEvent`. Do not perform blocking work in the COM callback.

Zero-event callbacks are meaningful keep-alive notifications and should still enqueue an `AeEventBatch` with `events=()`.

## Event Conversion

Map OPC AE event fields into `AeEvent`:

- `szSource` -> `source`
- `ftTime` -> `time`
- `szMessage` -> `message`
- `dwEventType` -> `event_type`
- `dwEventCategory` -> `category_id`
- `dwSeverity` -> `severity`
- selected vendor attributes -> `attributes`
- condition fields -> `condition_name`, `subcondition_name`, `change_mask`, `new_state`, `quality`, `ack_required`, `active_time`, `cookie`
- `szActorID` -> `actor_id`

Use exact `FILETIME` conversion for `active_time`. Acknowledgement depends on passing that value back unchanged.

## Acknowledgement Rules

`OpcAeClient.ack(event, ...)` should use `event.acknowledgement_reference()`.

`ack_condition(...)` should construct `AeAcknowledgementReference` explicitly.

The COM backend must call `IOPCEventServer::AckCondition` with the original source, condition name, active time, and cookie. Do not synthesize or normalize these values beyond required COM type conversion.

## Gateway Rules

Gateway support should preserve the queue-first model:

- expose `OpcAeClient` separately from `OpcDaClient`
- register all AE serializers on both proxy and server
- use `next_batch(timeout)` or batch iteration
- do not marshal arbitrary user callbacks over Pyro

`AeEventBatch` is the gateway delivery unit because it preserves refresh, last-refresh, and keep-alive metadata.

## Testing Strategy

Keep most tests fake-backed and platform-independent:

- domain type serialization round trips
- bitmask conversion
- ack reference extraction
- queue behavior
- refresh collection until `last_refresh`
- subscription activation order
- gateway serializer registration

Real-server tests should be opt-in and guarded by environment variables because they require Windows and a configured AE server.

Suggested environment variables:

```shell
OPENOPC2_AE_INTEGRATION=1
OPC_AE_SERVER=Matrikon.OPC.AlarmEvent
OPC_HOST=localhost
```

## Known Risks

- OPC AE uses custom COM interfaces; `comtypes` may need hand-written interface definitions.
- Some AE servers support only simple events and may return `E_NOTIMPL` for condition methods.
- Servers may ignore unsupported filters; expose `available_filters()` and eventually returned filter state to make that visible.
- Queue overflow policy is not decided yet.
- `Refresh()` is not event history replay; tests and docs should keep that distinction explicit.
