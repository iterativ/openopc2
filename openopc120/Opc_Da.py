import string

import pythoncom
import win32com.client
import logging
import os
from exceptions import OPCError
from pythoncom_datatypes import VtType
from dataclasses import dataclass
from enum import Enum
from collections import namedtuple

logger = logging.getLogger(__name__)

# Win32 only modules not needed for 'open' protocol mode
if os.name == 'nt':
    try:
        import win32com.client
        import win32com.server.util
        import win32event
        import pythoncom
        import pywintypes
        import SystemHealth as SystemHealth

        # Win32 variant types
        pywintypes.datetime = pywintypes.TimeType

        # Allow gencache to create the cached wrapper objects
        win32com.client.gencache.is_readonly = False

        # Under p2exe the call in gencache to __init__() does not happen
        # so we use Rebuild() to force the creation of the gen_py folder
        win32com.client.gencache.Rebuild(verbose=0)

    # So we can work on Windows in "open" protocol mode without the need for the win32com modules
    except ImportError as e:
        print(e)
        win32com_found = False
    else:
        win32com_found = True
else:
    win32com_found = False


ACCESS_RIGHTS = (0, 'Read', 'Write', 'Read/Write')
OPC_QUALITY = ('Bad', 'Uncertain', 'Unknown', 'Good')


@dataclass
class TagProperty:
    data_type = None
    value = None
    quality = None
    timestamp = None
    access_rights = None
    server_scan_rate = None
    eu_type = None
    eu_info = None
    description = None

tag_property_fields = [
     'DataType', 'Value', 'Quality', 'Timestamp', 'AccessRights', 'ServerScanRate', 'ItemEUType', 'ItemEUInfo',
     'Description']
TagPropertyNames = namedtuple('TagProperty',tag_property_fields, defaults=[None]*len(tag_property_fields))

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
        return [e.value for e in cls]

    @classmethod
    def all_names(cls):
        return [e.name for e in cls]



class OpcCom:
    def __init__(self, opc_class: str):
        # TODO: Get browser type (hierarchical etc)
        self.server: string = None
        self.host: string = 'localhost'
        self.groups = None
        self.opc_class = opc_class
        self.client_name = None
        self.server_name = None
        self.server_state = None
        self.major_version = None
        self.minor_version = None
        self.build_number = None
        self.start_time = None
        self.current_time = None
        self.vendor_info = None
        self.opc_client = None
        self.initialize_client(opc_class)

    def initialize_client(self, opc_class):
        try:
            pythoncom.CoInitialize()
            self.opc_client = win32com.client.gencache.EnsureDispatch(opc_class, 0)
        except pythoncom.com_error as err:
            # TODO: potential memory leak, destroy pythoncom
            print(opc_class)
            pythoncom.CoUninitialize()
            raise OPCError(f'Dispatch: {err}')

    def connect(self, host: str, server: str):
        self.server = server
        self.host = host

        self.opc_client.Connect(self.server, self.host)
        self.groups = self.opc_client.OPCGroups
        self.client_name = self.opc_client.ClientName
        self.server_name = self.opc_client.ServerName
        self.server_state = self.opc_client.ServerState
        self.major_version = self.opc_client.MajorVersion
        self.minor_version = self.opc_client.MinorVersion
        self.build_number = self.opc_client.BuildNumber
        self.start_time = self.opc_client.StartTime
        self.current_time = self.opc_client.CurrentTime
        self.vendor_info = self.opc_client.VendorInfo

        # for key in dir(self.opc_client):
        #     method = getattr(self.opc_client, key)
        #     print(key)
        #     if str(type(method)) == "<type 'instance'>":
        #         print(key)
        #         for sub_method in dir(method):
        #             if not sub_method.startswith("_") and not "clsid" in sub_method.lower():
        #                 print("\t" + sub_method)
        #     else:
        #         print("\t", method)

    def create_browser(self):
        return self.opc_client.CreateBrowser()

    def disconnect(self):
        self.opc_client.Disconnect()

    def server_name(self):
        return self.opc_client.ServerName

    def get_opc_servers(self, opc_host):
        return self.opc_client.GetOPCServers(opc_host)

    def get_available_properties(self, tag):
        (count, property_id, descriptions, datatypes) = list(self.opc_client.QueryAvailableProperties(tag))
        return count, property_id, descriptions, datatypes

    def get_tag_properties(self, tag, property_ids=TagPropertyId.all_ids()):
        # TODO: Find out if it makes any difference to request selected properties (so far there is no benefit)


        property_ids_checked = [e.value for e in property_ids] if type(property_ids[0]) == TagPropertyId else property_ids

        if any(p not in TagPropertyId.all_ids() for p in property_ids_checked):
            logger.error(f"Invalid property id found. requested ids 0 {property_ids_checked} on tag: {tag}")
            property_ids_checked = [i for i in property_ids_checked if i in TagPropertyId.all_ids()]

        properties_raw, errors = self.opc_client.GetItemProperties(tag, len(property_ids_checked) - 1, property_ids_checked)

        # try:
        #     properties = TagPropertyNames(*properties_raw)
        # except:
        #     pass
        #
        #
        # values = []
        #
        # # Replace variant id with type strings
        # # Replace quality bits with quality string§s
        # # Replace access rights bits with strings
        # if properties.AccessRights:
        #     properties = properties._replace(AccessRights=ACCESS_RIGHTS[properties.AccessRights])
        #
        # if properties.DataType:
        #     properties = properties._replace(DataType=self.get_vt_type(property_ids.index(1)))
        #
        # if properties.Quality:
        #     properties = properties._replace( Quality=self.get_quality_string(property_ids.index(3)))
        #
        # return properties, errors

    def get_error_string(self, error_id:int):
        return self.opc_client.GetErrorString(error_id)


    def __str__(self):
        return f"OPCCom Object: {self.host} {self.server} {self.minor_version}.{self.major_version}"

    @staticmethod
    def get_quality_string(quality_bits):
        """Convert OPC quality bits to a descriptive string"""

        quality = (quality_bits >> 6) & 3
        return OPC_QUALITY[quality]

    @staticmethod
    def get_vt_type(datatype_number: int):
        return VtType(datatype_number).name




