from collections import namedtuple
from dataclasses import dataclass, asdict
from enum import Enum


class ProtocolMode(str, Enum):
    """
    Protocol mode
    """
    COM = "com"
    GATEWAY = "gateway"


class DataSource(str, Enum):
    """
    Data source for read
    """
    CACHE = "cache"
    DEVICE = "device"
    HYBRID = "hybrid"


class LogLevel(str, Enum):
    """
    Log level
    """
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


ACCESS_RIGHTS = (0, 'Read', 'Write', 'Read/Write')
OPC_QUALITY = ('Bad', 'Uncertain', 'Unknown', 'Good')


@dataclass
class TagPropertyItem:
    data_type = None
    value = None
    description = None
    property_id = None

    def get_default_tuple(self):
        return self.property_id, self.description, self.value


@dataclass()
class TagProperties:
    """
    This is a container for all Properties one Tag can have.
    """
    tag_name: str = None
    data_type: str = None
    value: float = None
    quality: str = None
    timestamp: str = None
    access_rights: str = None
    server_scan_rate: float = None
    eu_type: str = None
    eu_info: str = None
    description: str = None

    def from_tag_property_items_by_name(self, tag, tag_property_items_by_name: dict[TagPropertyItem]):
        default_property_item = TagPropertyItem()
        self.tag_name = tag
        self.data_type = tag_property_items_by_name.get('Item Canonical DataType', default_property_item).value
        self.value = tag_property_items_by_name.get('Item Value', default_property_item).value
        self.quality = tag_property_items_by_name.get('Item Quality', default_property_item).value
        self.timestamp = tag_property_items_by_name.get('Item Timestamp', default_property_item).value
        self.access_rights = tag_property_items_by_name.get('Item Access Rights', default_property_item).value
        self.server_scan_rate = tag_property_items_by_name.get('Server Scan Rate', default_property_item).value
        self.eu_type = tag_property_items_by_name.get('Item EU Type', default_property_item).value
        self.eu_info = tag_property_items_by_name.get('Item EUINfo', default_property_item).value
        self.description = tag_property_items_by_name.get('Item Description', default_property_item).value
        return self

    def class_to_dict(self):
        default = asdict(self)
        default["__class__"] = "opc_types.TagProperties"
        return default

    @classmethod
    def dict_to_class(cls, class_name, tag_properties_dictionary):
        tag_properties_dictionary.pop("__class__")
        p = TagProperties(**tag_properties_dictionary)
        return p


tag_property_fields = [
    'DataType', 'Value', 'Quality', 'Timestamp', 'AccessRights', 'ServerScanRate', 'ItemEUType', 'ItemEUInfo',
    'Description']
TagPropertyNames = namedtuple('TagProperty', tag_property_fields, defaults=[None] * len(tag_property_fields))


class TagPropertyId(Enum):
    ItemCanonicalDatatype = 1
    ItemValue = 2
    ItemQuality = 3
    ItemTimeStamp = 4
    ItemAccessRights = 5
    ServerScanRate = 6
    ItemEUType = 7
    ItemEUInfo = 8
    ItemDescription = 101

    @classmethod
    def all_ids(cls):
        return [property_id.value for property_id in cls]

    @classmethod
    def all_names(cls):
        return [property_id.name for property_id in cls]
