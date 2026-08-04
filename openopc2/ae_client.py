import time
import uuid
from typing import Dict, Iterable, Optional, cast

try:
    import Pyro5.api
except ImportError:
    class _PyroApi:
        @staticmethod
        def expose(cls):
            return cls

    class _Pyro5:
        api = _PyroApi()

    Pyro5 = _Pyro5()

from openopc2.ae_com import OpcAeCom
from openopc2.ae_subscription import OpcAeSubscription
from openopc2.ae_types import (
    AeAcknowledgementReference,
    AeEvent,
    AeEventBatch,
    AeEventType,
    AeFilter,
)
from openopc2.config import OpenOpcConfig


@Pyro5.api.expose
class OpcAeClient:
    def __init__(self, open_opc_config: OpenOpcConfig = OpenOpcConfig(), ae_com: OpcAeCom | None = None):
        self.config = open_opc_config
        self.opc_server = open_opc_config.OPC_AE_SERVER
        self.opc_host = open_opc_config.OPC_HOST
        self.client_name = open_opc_config.OPC_AE_CLIENT
        self.client_id = uuid.uuid4()
        self.connected = False
        self._ae = ae_com or OpcAeCom(open_opc_config)
        self._subscriptions: Dict[int, OpcAeSubscription] = {}
        self._next_subscription_handle = 1

    def connect(self, opc_server: str | None = None, opc_host: str = "localhost"):
        self.opc_server = opc_server or self.config.OPC_AE_SERVER
        self.opc_host = opc_host
        self._ae.connect(self.opc_server, self.opc_host)
        self.connected = True

    def close(self):
        for subscription in list(self._subscriptions.values()):
            subscription.close()
        self._subscriptions = {}
        self._ae.disconnect()
        self.connected = False

    def info(self):
        return self._ae.get_status()

    def available_filters(self):
        """Return filters supported by the AE server. Wraps IOPCEventServer::QueryAvailableFilters."""
        return self._ae.query_available_filters()

    def categories(self, event_types: AeEventType = AeEventType.ALL):
        """Return event categories. Wraps IOPCEventServer::QueryEventCategories."""
        return self._ae.query_event_categories(event_types)

    def attributes(self, category_id: int):
        """Return vendor-specific event attributes. Wraps IOPCEventServer::QueryEventAttributes."""
        return self._ae.query_event_attributes(category_id)

    def condition_names(self, category_id: int):
        """Return condition names for a category. Wraps IOPCEventServer::QueryConditionNames."""
        return self._ae.query_condition_names(category_id)

    def subcondition_names(self, condition_name: str):
        """Return subcondition names. Wraps IOPCEventServer::QuerySubConditionNames."""
        return self._ae.query_subcondition_names(condition_name)

    def source_conditions(self, source: str):
        """Return conditions associated with a source. Wraps IOPCEventServer::QuerySourceConditions."""
        return self._ae.query_source_conditions(source)

    def subscribe(
        self,
        filter: AeFilter | None = None,
        returned_attributes: dict[int, list[int]] | None = None,
        buffer_time: int = 0,
        max_size: int = 0,
        active: bool = True,
        refresh: bool = False,
    ) -> OpcAeSubscription:
        subscription_filter = filter or AeFilter()
        client_handle = self._next_subscription_handle
        self._next_subscription_handle += 1
        backend = self._ae.create_subscription(False, buffer_time, max_size, client_handle)
        subscription = OpcAeSubscription(
            subscription_backend=backend,
            filter=subscription_filter,
            returned_attributes=returned_attributes,
        )
        if hasattr(backend, "set_filter"):
            backend.set_filter(subscription_filter)
        if returned_attributes and hasattr(backend, "select_returned_attributes"):
            for category_id, attribute_ids in returned_attributes.items():
                backend.select_returned_attributes(category_id, attribute_ids)
        if hasattr(backend, "attach_queue"):
            backend.attach_queue(subscription.enqueue_batch)
        self._subscriptions[client_handle] = subscription
        if active and hasattr(backend, "set_active"):
            backend.set_active(True)
        if refresh:
            subscription.refresh()
        return subscription

    def refresh(
        self,
        filter: AeFilter | None = None,
        returned_attributes: dict[int, list[int]] | None = None,
        timeout: Optional[float] = None,
    ) -> tuple[AeEvent, ...]:
        deadline = None if timeout is None else time.monotonic() + timeout
        with self.subscribe(filter=filter, returned_attributes=returned_attributes, active=False) as subscription:
            subscription.refresh()
            events = []
            while True:
                remaining = None if deadline is None else max(0, deadline - time.monotonic())
                batch = subscription.next_batch(timeout=remaining)
                if batch is None:
                    break
                batch = cast(AeEventBatch, batch)
                events.extend(batch.events)
                if batch.last_refresh:
                    break
            return tuple(events)

    def get_condition_state(self, source: str, condition_name: str, attribute_ids: Iterable[int] | None = None):
        """Return current condition state. Wraps IOPCEventServer::GetConditionState."""
        return self._ae.get_condition_state(source, condition_name, list(attribute_ids or []))

    def ack(self, event: AeEvent, acknowledger_id: str, comment: str = ""):
        return self.ack_reference(event.acknowledgement_reference(), acknowledger_id, comment)

    def ack_reference(self, reference: AeAcknowledgementReference, acknowledger_id: str, comment: str = ""):
        return self._ae.ack_condition([reference], acknowledger_id, comment)

    def ack_condition(
        self,
        source: str,
        condition_name: str,
        active_time,
        cookie: int,
        acknowledger_id: str,
        comment: str = "",
    ):
        reference = AeAcknowledgementReference(source, condition_name, active_time, cookie)
        return self.ack_reference(reference, acknowledger_id, comment)
