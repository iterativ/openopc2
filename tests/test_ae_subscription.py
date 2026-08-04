from datetime import datetime, timezone
from unittest import TestCase

from openopc2.ae_subscription import OpcAeSubscription
from openopc2.ae_types import AeEvent, AeEventBatch, AeEventType


class FakeBackend:
    def __init__(self):
        self.refreshed = False
        self.closed = False

    def refresh(self):
        self.refreshed = True

    def close(self):
        self.closed = True


class TestOpcAeSubscription(TestCase):
    def test_next_batch_returns_enqueued_batch(self):
        subscription = OpcAeSubscription()
        batch = AeEventBatch(
            subscription_id=1,
            refresh=False,
            last_refresh=False,
            events=(
                AeEvent(
                    source="System",
                    time=datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
                    message="Started",
                    event_type=AeEventType.SIMPLE,
                    category_id=1,
                    severity=1,
                ),
            ),
        )

        subscription.enqueue_batch(batch)

        self.assertEqual(batch, subscription.next_batch(timeout=0))

    def test_refresh_and_close_delegate_to_backend(self):
        backend = FakeBackend()
        subscription = OpcAeSubscription(subscription_backend=backend)

        subscription.refresh()
        subscription.close()

        self.assertTrue(backend.refreshed)
        self.assertTrue(backend.closed)
