import os
import string

import Pyro5.core

from openopc2.exceptions import OPCError
from openopc2.opc_types import ACCESS_RIGHTS, OPC_QUALITY, TagPropertyItem, TagProperties
from openopc2.pythoncom_datatypes import VtType
from openopc2.logger import log

# Win32 only modules not needed for 'open' protocol mode
if os.name == 'nt':
    try:
        # TODO: chose bewtween pywin pythoncom and wind32 but do not use both
        import pythoncom
        import pywintypes
        import win32com.client
        import win32com.server.util

        # Win32 variant types
        pywintypes.datetime = pywintypes.TimeType

        # Allow gencache to create the cached wrapper objects
        win32com.client.gencache.is_readonly = False
        win32com.client.gencache.Rebuild(verbose=0)

    # So we can work on Windows in "gateway" protocol mode without the need for the win32com modules
    except ImportError as e:
        log.exception(e)
        win32com_found = False
    else:
        win32com_found = True
else:
    win32com_found = False


@Pyro5.api.expose
class OpcCom:
    """
    This class handles the com interface of the OPC DA server.
    """

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
            log.info(f"Initialize OPC DA OpcDaClient: '{opc_class}'")
            pythoncom.CoInitialize()
            self.opc_client = win32com.client.gencache.EnsureDispatch(opc_class, 0)
        except pythoncom.com_error as err:
            # TODO: potential memory leak, destroy pythoncom
            log.exception('Error in initialize OpcDaClient')
            pythoncom.CoUninitialize()
            raise OPCError(f'Dispatch: {err}')

    def connect(self, host: str, server: str):
        self.server = server
        self.host = "localhost"
        try:
            log.info(f"Connecting OPC Client Com interface: '{self.server}', '{self.host}'")
            self.opc_client.Connect(self.server, self.host)
        except Exception as error:
            log.error(f"Error Connecting OPC Client Com interface: Server: '{self.server}', Host: '{self.host}', Error: '{error}'")

            log.exception('Error connecting OPC Client', exc_info=True)
            pass
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

    def _property_value_conversion(self, description, input_value):
        value = input_value

        if description == 'Item Canonical DataType':
            value = VtType(value).name
        if description == 'Item Timestamp':
            value = str(value)
        if description == 'Item Access Rights':
            value = ACCESS_RIGHTS[value]
        if description == 'Item Quality':
            if value > 3:
                value = 3
            value = OPC_QUALITY[value]

        return value

    def get_tag_properties(self, tag, property_ids=[]):
        # TODO: Find out if it makes any difference to request selected properties (so far there is no benefit)
        property_ids_filter = property_ids

        count, property_ids, descriptions, datatypes = self.get_available_properties(tag)
        available_properies_by_id = {}
        for result in zip(property_ids, descriptions, datatypes):
            available_properies_by_id[result[0]] = {
                'property_id': result[0],
                'description': result[1],
                'data_type': result[2]
            }

        property_ids_cleaned = [p for p in property_ids if p > 0]
        if property_ids_filter:
            property_ids_cleaned = [p for p in property_ids if p in property_ids_filter]
            # I assume this is nevessary due to 1 indexed arrays in windows
            property_ids_cleaned.insert(0, 0)

        item_properties_values, errors = self.opc_client.GetItemProperties(tag, len(property_ids_cleaned) - 1,
                                                                           property_ids_cleaned)

        if property_ids_filter:
            property_ids_cleaned.remove(0)

        # Create tag property item in a readable form. One item is one propeterty, there are many properties for one tag
        properties_by_description = {}

        if not property_ids_filter:
            # Add first property for compatibility
            tag_property_item = TagPropertyItem()
            tag_property_item.property_id = 0
            tag_property_item.description = 'Item ID (virtual property)'
            tag_property_item.value = tag

            properties_by_description[tag_property_item.description] = tag_property_item
            item_properties_values = list(item_properties_values)
            item_properties_values.insert(0, 0)

        for property_result in zip(property_ids_cleaned, item_properties_values):
            tag_property_item = TagPropertyItem()
            property = available_properies_by_id[property_result[0]]
            tag_property_item.data_type = VtType(property['data_type']).name
            tag_property_item.property_id = property['property_id']
            tag_property_item.description = property['description']
            tag_property_item.value = self._property_value_conversion(tag_property_item.description, property_result[1])

            properties_by_description[tag_property_item.description] = tag_property_item

        tag_properties = TagProperties().from_tag_property_items_by_name(tag, properties_by_description)
        return tag_properties, errors

    def get_error_string(self, error_id: int):
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
