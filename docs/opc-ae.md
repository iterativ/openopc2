# OPC Alarms and Events

OpenOPC2 is adding support for OPC Alarms and Events through a dedicated `OpcAeClient`. OPC AE is separate from OPC Data Access: DA reads and writes live item values, while AE receives event notifications from an OPC event server.

## Status

The Python API, domain types, gateway serialization hooks, configuration fields, and minimal CLI commands are present. The raw Windows OPC AE custom COM backend in `openopc2/ae_com.py` is still in progress, so local COM usage will raise `NotImplementedError` until that backend is completed.

Use this document as the intended public API contract for the AE feature.

## Configuration

OPC AE uses its own server configuration so it is not accidentally pointed at a DA server.

```shell
OPC_AE_SERVER=Matrikon.OPC.AlarmEvent
OPC_AE_CLIENT=OpenOPC-AE
OPC_AE_TIMEOUT=1000
```

These settings are separate from `OPC_SERVER`, which remains the Data Access server ProgID. AE reuses the existing host and gateway settings where they mean the same thing:

```shell
OPC_HOST=localhost
OPC_GATE_HOST=192.168.1.96
OPC_GATE_PORT=7766
```

Local AE COM access requires Windows and a Python process bitness that matches the registered AE COM server. The gateway remains the intended cross-platform path.

## Basic Usage

```python
from openopc2.ae_client import OpcAeClient
from openopc2.ae_types import AeEventType, AeFilter

client = OpcAeClient()
client.connect("Matrikon.OPC.AlarmEvent", "localhost")

subscription = client.subscribe(
    filter=AeFilter(
        event_types=AeEventType.CONDITION,
        low_severity=600,
        high_severity=1000,
        areas=("Plant1",),
    ),
    buffer_time=1000,
    max_size=100,
    refresh=False,
)

subscription.refresh()

for batch in subscription.batches(timeout=5):
    for event in batch.events:
        print(event.source, event.severity, event.message)
```

`subscribe(..., refresh=False)` is the default. Creating or activating an AE subscription does not imply a refresh.

## Event Batches

Subscriptions yield `AeEventBatch` objects rather than only individual events.

```python
for batch in subscription.batches(timeout=5):
    print(batch.subscription_id, batch.refresh, batch.last_refresh, batch.keep_alive)
```

This preserves OPC AE callback metadata:

- `refresh`: the batch was sent in response to a condition refresh.
- `last_refresh`: the batch completes a refresh response.
- `keep_alive`: the server sent a zero-event keep-alive notification.
- `events`: the event notifications delivered in this callback.

Use `subscription.events()` when you intentionally want to flatten batches.

## Discovery

The public API uses Pythonic names while docstrings and internals keep the corresponding OPC AE method names visible.

```python
filters = client.available_filters()
categories = client.categories(AeEventType.CONDITION)
attributes = client.attributes(category_id=10)
condition_names = client.condition_names(category_id=10)
subconditions = client.subcondition_names("LevelAlarm")
source_conditions = client.source_conditions("FIC101")
```

Event attributes are server-specific and selected by attribute ID. Attribute names or descriptions are useful metadata, but IDs are the stable protocol identity.

## Returned Attributes

Returned attributes are selected explicitly per event category.

```python
subscription = client.subscribe(
    filter=AeFilter(categories=(10,)),
    returned_attributes={10: [1001, 1002]},
)
```

To intentionally select all known attributes for a category:

```python
from openopc2.ae_types import AeReturnedAttributes

attrs = client.attributes(category_id=10)
subscription = client.subscribe(
    filter=AeFilter(categories=(10,)),
    returned_attributes={10: AeReturnedAttributes.all_for(attrs)},
)
```

Avoid selecting all attributes by default on production systems. Some servers expose large or unstable vendor-specific attribute sets.

## Condition Refresh

`client.refresh()` is a convenience for building a current alarm summary.

```python
events = client.refresh(
    filter=AeFilter(event_types=AeEventType.CONDITION),
    timeout=10,
)
```

This creates a temporary subscription, requests a condition refresh, collects batches until the last refresh marker or timeout, then closes the subscription.

Condition refresh is not event history replay. It is only for current active conditions and inactive but unacknowledged conditions matching the subscription filter.

## Acknowledgement

The normal acknowledgement path is event-first:

```python
for event in subscription.events(timeout=5):
    if event.ack_required:
        client.ack(event, acknowledger_id="operator-1", comment="checked")
```

For persistence and retry workflows, acknowledge with an explicit reference:

```python
client.ack_condition(
    source="FIC101",
    condition_name="LevelAlarm",
    active_time=active_time,
    cookie=42,
    acknowledger_id="operator-1",
    comment="checked",
)
```

The acknowledgement reference must use the original `source`, `condition_name`, `active_time`, and `cookie` received from the condition event notification.

## Gateway Usage

AE is intended to work through the same OpenOPC2 gateway model as DA, with a separate AE proxy.

```python
from openopc2.gateway_proxy import OpenOpcGatewayProxy

client = OpenOpcGatewayProxy("192.168.1.96", 7766).get_opc_ae_client_proxy()
client.connect("Matrikon.OPC.AlarmEvent", "localhost")

subscription = client.subscribe(filter=AeFilter(event_types=AeEventType.CONDITION))
batch = subscription.next_batch(timeout=5)
```

Gateway clients should poll batches or iterate over queued batches. User callbacks are not marshalled across Pyro.

## CLI

Minimal AE CLI commands are available for discovery and smoke testing:

```shell
python -m openopc2 ae-categories --event-type condition
python -m openopc2 ae-refresh --event-type condition --severity-min 600
python -m openopc2 ae-subscribe --event-type condition --severity-min 600
```

CLI acknowledgement is intentionally deferred because it requires passing the acknowledgement reference exactly.

## Deferred Scope

The first AE interface intentionally does not expose condition enable or disable controls:

- `enable_condition_by_source`
- `disable_condition_by_source`
- `enable_condition_by_area`
- `disable_condition_by_area`

Those methods change server behavior and should be added after subscribe, refresh, condition state, gateway delivery, and acknowledgement are proven against real AE servers.
