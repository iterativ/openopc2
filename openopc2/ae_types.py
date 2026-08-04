from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime
from enum import IntEnum, IntFlag
from typing import Any, Dict, Mapping, Optional, Tuple, Type


class AeEventType(IntFlag):
    SIMPLE = 1
    TRACKING = 2
    CONDITION = 4
    ALL = SIMPLE | TRACKING | CONDITION


class AeChangeMask(IntFlag):
    ACTIVE_STATE = 1
    ACK_STATE = 2
    ENABLE_STATE = 4
    QUALITY = 8
    SEVERITY = 16
    SUBCONDITION = 32
    MESSAGE = 64
    ATTRIBUTE = 128


class AeConditionState(IntFlag):
    ENABLED = 1
    ACTIVE = 2
    ACKED = 4


class AeFilterMask(IntFlag):
    BY_EVENT = 1
    BY_CATEGORY = 2
    BY_SEVERITY = 4
    BY_AREA = 8
    BY_SOURCE = 16


class AeServerState(IntEnum):
    RUNNING = 1
    FAILED = 2
    NOCONFIG = 3
    SUSPENDED = 4
    TEST = 5


@dataclass(frozen=True)
class AeFilter:
    event_types: AeEventType = AeEventType.ALL
    categories: Tuple[int, ...] = ()
    low_severity: int = 1
    high_severity: int = 1000
    areas: Tuple[str, ...] = ()
    sources: Tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.event_types, AeEventType):
            event_types = AeEventType(0)
            for event_type in self.event_types:
                event_types |= event_type
            object.__setattr__(self, "event_types", event_types)
        object.__setattr__(self, "categories", tuple(self.categories))
        object.__setattr__(self, "areas", tuple(self.areas))
        object.__setattr__(self, "sources", tuple(self.sources))
        if int(self.event_types) == 0:
            raise ValueError("event_types must not be empty")
        if not 1 <= self.low_severity <= 1000:
            raise ValueError("low_severity must be between 1 and 1000")
        if not 1 <= self.high_severity <= 1000:
            raise ValueError("high_severity must be between 1 and 1000")
        if self.low_severity > self.high_severity:
            raise ValueError("low_severity must be less than or equal to high_severity")


@dataclass(frozen=True)
class AeCategory:
    category_id: int
    description: str
    event_type: Optional[AeEventType] = None


@dataclass(frozen=True)
class AeAttribute:
    attribute_id: int
    description: str
    data_type: str


@dataclass(frozen=True)
class AeAcknowledgementReference:
    source: str
    condition_name: str
    active_time: datetime
    cookie: int


@dataclass(frozen=True)
class AeEvent:
    source: str
    time: datetime
    message: str
    event_type: AeEventType
    category_id: int
    severity: int
    attributes: Mapping[int, Any] = field(default_factory=dict)
    attribute_names: Mapping[int, str] = field(default_factory=dict)
    condition_name: Optional[str] = None
    subcondition_name: Optional[str] = None
    change_mask: Optional[AeChangeMask] = None
    new_state: Optional[AeConditionState] = None
    quality: Optional[int] = None
    ack_required: bool = False
    active_time: Optional[datetime] = None
    cookie: Optional[int] = None
    actor_id: Optional[str] = None

    def acknowledgement_reference(self) -> AeAcknowledgementReference:
        if self.event_type != AeEventType.CONDITION:
            raise ValueError("Only condition events can be acknowledged")
        if not self.condition_name or self.active_time is None or self.cookie is None:
            raise ValueError("Condition event is missing acknowledgement fields")
        return AeAcknowledgementReference(
            source=self.source,
            condition_name=self.condition_name,
            active_time=self.active_time,
            cookie=self.cookie,
        )


@dataclass(frozen=True)
class AeEventBatch:
    subscription_id: int
    refresh: bool
    last_refresh: bool
    events: Tuple[AeEvent, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "events", tuple(self.events))

    @property
    def keep_alive(self) -> bool:
        return len(self.events) == 0


@dataclass(frozen=True)
class AeConditionStateSnapshot:
    source: str
    condition_name: str
    state: AeConditionState
    active_subcondition: Optional[str] = None
    quality: Optional[int] = None
    last_ack_time: Optional[datetime] = None
    subcondition_last_active: Optional[datetime] = None
    condition_last_active: Optional[datetime] = None
    condition_last_inactive: Optional[datetime] = None
    acknowledger_id: Optional[str] = None
    comment: Optional[str] = None
    attributes: Mapping[int, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AeSubscriptionState:
    active: bool
    buffer_time: int
    max_size: int
    client_handle: int


@dataclass(frozen=True)
class AeServerStatus:
    start_time: datetime
    current_time: datetime
    last_update_time: Optional[datetime]
    state: AeServerState
    major_version: int
    minor_version: int
    build_number: int
    vendor_info: str


SERIALIZABLE_AE_TYPES: Tuple[Type[Any], ...] = (
    AeFilter,
    AeCategory,
    AeAttribute,
    AeAcknowledgementReference,
    AeEvent,
    AeEventBatch,
    AeConditionStateSnapshot,
    AeSubscriptionState,
    AeServerStatus,
)


def _encode(value):
    if isinstance(value, (IntFlag, IntEnum)):
        return int(value)
    if isinstance(value, datetime):
        return {"__datetime__": value.isoformat()}
    if is_dataclass(value):
        return value.class_to_dict()
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, Mapping):
        return {_encode(key): _encode(item) for key, item in value.items()}
    return value


def _decode(value):
    if isinstance(value, dict):
        if "__datetime__" in value:
            return datetime.fromisoformat(value["__datetime__"])
        if "__class__" in value:
            return dict_to_ae_class(value["__class__"], value)
        return {_decode(key): _decode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_decode(item) for item in value]
    return value


def _class_name(cls: Type[Any]) -> str:
    return f"ae_types.{cls.__name__}"


def ae_class_to_dict(obj) -> Dict[str, Any]:
    data = {field.name: _encode(getattr(obj, field.name)) for field in fields(obj)}
    data["__class__"] = _class_name(type(obj))
    return data


def dict_to_ae_class(class_name: str, data: Dict[str, Any]):
    clean = dict(data)
    clean.pop("__class__", None)
    cls_name = class_name.split(".")[-1]
    cls = {cls.__name__: cls for cls in SERIALIZABLE_AE_TYPES}[cls_name]
    values = {key: _decode(value) for key, value in clean.items()}
    enum_fields = {
        "event_types": AeEventType,
        "event_type": AeEventType,
        "change_mask": AeChangeMask,
        "new_state": AeConditionState,
        "state": AeConditionState,
    }
    for field in fields(cls):
        if field.name in enum_fields and values.get(field.name) is not None:
            values[field.name] = enum_fields[field.name](values[field.name])
        if field.name in {"categories", "areas", "sources", "events"} and field.name in values:
            values[field.name] = tuple(values[field.name])
    if cls is AeServerStatus and values.get("state") is not None:
        values["state"] = AeServerState(values["state"])
    return cls(**values)


def _install_serializers():
    for cls in SERIALIZABLE_AE_TYPES:
        cls.class_to_dict = ae_class_to_dict
        cls.dict_to_class = classmethod(lambda ae_cls, class_name, data: dict_to_ae_class(class_name, data))


_install_serializers()


def register_ae_serializers(register_class_to_dict, register_dict_to_class):
    for cls in SERIALIZABLE_AE_TYPES:
        register_class_to_dict(cls, cls.class_to_dict)
        register_dict_to_class(cls, cls.dict_to_class)
        register_dict_to_class(_class_name(cls), cls.dict_to_class)


class AeReturnedAttributes:
    @staticmethod
    def all_for(attributes):
        return [attribute.attribute_id for attribute in attributes]
