from datetime import datetime, timezone
from unittest import TestCase

from openopc2.ae_client import OpcAeClient
from openopc2.ae_types import AeEvent, AeEventBatch, AeEventType
from openopc2.config import OpenOpcConfig


class FakeSubscriptionBackend:
    def __init__(self):
        self.enqueue = None
        self.filter = None
        self.returned_attributes = {}
        self.refreshed = False
        self.closed = False
        self.active = False

    def attach_queue(self, enqueue):
        self.enqueue = enqueue

    def set_filter(self, ae_filter):
        self.filter = ae_filter

    def select_returned_attributes(self, category_id, attribute_ids):
        self.returned_attributes[category_id] = list(attribute_ids)

    def set_active(self, active):
        self.active = active

    def refresh(self):
        self.refreshed = True
        self.enqueue(
            AeEventBatch(
                subscription_id=1,
                refresh=True,
                last_refresh=True,
                events=(
                    AeEvent(
                        source="FIC101",
                        time=datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
                        message="Level alarm",
                        event_type=AeEventType.CONDITION,
                        category_id=10,
                        severity=900,
                        condition_name="LevelAlarm",
                        active_time=datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
                        cookie=42,
                        ack_required=True,
                    ),
                ),
            )
        )

    def close(self):
        self.closed = True


class FakeAeCom:
    def __init__(self):
        self.connected = None
        self.subscription = FakeSubscriptionBackend()
        self.acks = []
        self.created_subscriptions = []

    def connect(self, server, host):
        self.connected = (server, host)

    def disconnect(self):
        pass

    def create_subscription(self, active, buffer_time, max_size, client_handle):
        self.created_subscriptions.append((active, buffer_time, max_size, client_handle))
        return self.subscription

    def ack_condition(self, references, acknowledger_id, comment):
        self.acks.append((references, acknowledger_id, comment))
        return ["S_OK"]

    def get_status(self):
        return None


class TestOpcAeClient(TestCase):
    def test_connect_uses_ae_server_default(self):
        fake_ae = FakeAeCom()
        client = OpcAeClient(OpenOpcConfig(opc_ae_server="Fake.AE"), fake_ae)

        client.connect()

        self.assertEqual(("Fake.AE", "localhost"), fake_ae.connected)

    def test_refresh_collects_until_last_refresh_and_closes_subscription(self):
        fake_ae = FakeAeCom()
        client = OpcAeClient(OpenOpcConfig(), fake_ae)

        events = client.refresh(timeout=0)

        self.assertEqual(1, len(events))
        self.assertEqual("FIC101", events[0].source)
        self.assertTrue(fake_ae.subscription.refreshed)
        self.assertTrue(fake_ae.subscription.closed)

    def test_subscribe_creates_backend_inactive_before_activation(self):
        fake_ae = FakeAeCom()
        client = OpcAeClient(OpenOpcConfig(), fake_ae)

        client.subscribe()

        self.assertEqual(False, fake_ae.created_subscriptions[0][0])
        self.assertTrue(fake_ae.subscription.active)

    def test_ack_uses_event_acknowledgement_reference(self):
        fake_ae = FakeAeCom()
        client = OpcAeClient(OpenOpcConfig(), fake_ae)
        event = client.refresh(timeout=0)[0]

        result = client.ack(event, "operator-1", "checked")

        self.assertEqual(["S_OK"], result)
        references, acknowledger_id, comment = fake_ae.acks[0]
        self.assertEqual("FIC101", references[0].source)
        self.assertEqual("operator-1", acknowledger_id)
        self.assertEqual("checked", comment)
