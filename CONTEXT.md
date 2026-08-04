# OpenOPC2

OpenOPC2 exposes OPC Classic capabilities to Python clients, including local Windows COM access and remote gateway access from non-Windows machines.

## Language

**OPC Data Access**:
The OPC Classic capability for reading and writing live process values addressed as items.
_Avoid_: DA events, tag events

**OPC Alarms and Events**:
The OPC Classic capability for receiving alarm and event notifications from an event server.
_Avoid_: AE tags, DA alarms

**Event Notification**:
A delivered OPC Alarms and Events occurrence containing standard event fields and optional server-specific attributes.
_Avoid_: Tag value, reading, sample

**Condition Event**:
An event notification about a source condition changing state, such as becoming active, acknowledged, enabled, or moving to another subcondition.
_Avoid_: Alarm tag

**Event Subscription**:
A client-owned OPC Alarms and Events subscription with a single server-side filter that controls which event notifications are delivered.
_Avoid_: Group

**Condition Refresh**:
An OPC Alarms and Events operation that asks a subscription to resend current active or inactive-unacknowledged condition notifications matching its filter.
_Avoid_: Event history, replay

**Event Batch**:
A group of event notifications delivered together from one OPC Alarms and Events subscription callback, including refresh and keep-alive metadata.
_Avoid_: Event list, callback payload

**Acknowledgement Reference**:
The source, condition name, active time, and cookie from a condition event notification that uniquely identify the condition transition being acknowledged.
_Avoid_: Alarm ID, event ID

**Event Attribute**:
A server-specific OPC Alarms and Events value selected by attribute ID and delivered with event notifications.
_Avoid_: Event property
