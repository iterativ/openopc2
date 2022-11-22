from collections import namedtuple
from dataclasses import dataclass, asdict
from typing import Dict, List
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
class TagPropertyItem():
    def __init__(self, data_type=None, value=None, description=None, property_id=None):
        self.data_type: str = data_type
        self.value = value
        self.description = description
        self.property_id = property_id
        self.available = False

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

    def from_tag_property_items_by_id(self, tag, tag_property_items_by_id):
        """
        Convert by id since the description varies from server to server
        """
        default_property_item = TagPropertyItem()
        self.tag_name = tag
        self.data_type = tag_property_items_by_id.get(1, default_property_item).value
        self.value = tag_property_items_by_id.get(2, default_property_item).value
        self.quality = tag_property_items_by_id.get(3, default_property_item).value
        self.timestamp = tag_property_items_by_id.get(4, default_property_item).value
        self.access_rights = tag_property_items_by_id.get(5, default_property_item).value
        self.server_scan_rate = tag_property_items_by_id.get(6, default_property_item).value
        self.eu_type = tag_property_items_by_id.get(7, default_property_item).value
        self.eu_info = tag_property_items_by_id.get(8, default_property_item).value
        self.description = tag_property_items_by_id.get(9, default_property_item).value
        return self
    def get_default_tag_properies_by_id(self):
        result = {}
        result[1] = TagPropertyItem(property_id=1,  description='Item Canonical Data Type', data_type='VT_I2')
        result[2] = TagPropertyItem(property_id=2,  description='Item Value', data_type='VT_VARIANT')
        result[3] = TagPropertyItem(property_id=3,  description='Item Quality', data_type='VT_I2')
        result[4] = TagPropertyItem(property_id=4,  description='Item TimeStamp', data_type='VT_DATE')
        result[5] = TagPropertyItem(property_id=5,  description='Item Access Rights', data_type='VT_I4')
        result[6] = TagPropertyItem(property_id=6,  description='Server Scan Rate', data_type='VT_R4')
        return result






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
