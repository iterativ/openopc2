from datetime import datetime, timezone
from unittest import TestCase

from openopc2.ae_types import (
    AeAcknowledgementReference,
    AeConditionState,
    AeEvent,
    AeEventBatch,
    AeEventType,
    AeFilter,
    dict_to_ae_class,
)


class TestAeTypes(TestCase):
    def test_filter_accepts_event_type_sets(self):
        ae_filter = AeFilter(event_types={AeEventType.SIMPLE, AeEventType.CONDITION})

        self.assertEqual(AeEventType.SIMPLE | AeEventType.CONDITION, ae_filter.event_types)

    def test_filter_validates_severity_range(self):
        with self.assertRaises(ValueError):
            AeFilter(low_severity=1000, high_severity=1)

    def test_event_acknowledgement_reference(self):
        active_time = datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc)
        event = AeEvent(
            source="FIC101",
            time=active_time,
            message="Level alarm",
            event_type=AeEventType.CONDITION,
            category_id=10,
            severity=900,
            condition_name="LevelAlarm",
            new_state=AeConditionState.ACTIVE,
            active_time=active_time,
            cookie=42,
            ack_required=True,
        )

        self.assertEqual(
            AeAcknowledgementReference("FIC101", "LevelAlarm", active_time, 42),
            event.acknowledgement_reference(),
        )

    def test_non_condition_event_cannot_be_acknowledged(self):
        event = AeEvent(
            source="System",
            time=datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
            message="Started",
            event_type=AeEventType.SIMPLE,
            category_id=1,
            severity=1,
        )

        with self.assertRaises(ValueError):
            event.acknowledgement_reference()

    def test_event_batch_serialization_round_trip(self):
        event_time = datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc)
        batch = AeEventBatch(
            subscription_id=7,
            refresh=True,
            last_refresh=True,
            events=(
                AeEvent(
                    source="FIC101",
                    time=event_time,
                    message="Level alarm",
                    event_type=AeEventType.CONDITION,
                    category_id=10,
                    severity=900,
                    attributes={1001: "Plant1"},
                    attribute_names={1001: "Area"},
                ),
            ),
        )

        restored = dict_to_ae_class("ae_types.AeEventBatch", batch.class_to_dict())

        self.assertEqual(batch, restored)
        self.assertFalse(restored.keep_alive)

    def test_empty_batch_is_keep_alive(self):
        batch = AeEventBatch(subscription_id=7, refresh=False, last_refresh=False)

        self.assertTrue(batch.keep_alive)
