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
        self.server: str | None = None
        self.host: str = 'localhost'
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
            raise OPCError(f'Dispatch: {err} opc_class:"{opc_class}"')

    def connect(self, server: str | None, host: str):
        self.server = server
        self.host = host
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
        """
        Return the available properites of that specific server. Be aware that the properties names are different between
        different servers, there is no consistency here . It seems that at least the property ids are consistent.
        """

        try:
            (count, property_id, descriptions, datatypes) = list(self.opc_client.QueryAvailableProperties(tag))
            self.available_properties_cache = (count, property_id, descriptions, datatypes)
            return count, property_id, descriptions, datatypes
        except pythoncom.com_error as err:
            error_msg = err#'properties: %s' % self._get_error_str(err)
            raise OPCError(error_msg)


    def _property_value_conversion(self, description, input_value):
        value = input_value
        # Different servers have different writings
        if description in {'Item Canonical DataType', 'Item Canonical Data Type'}:
            value = VtType(value).name
        elif description in {'Item Timestamp', 'Item TimeStamp'}:
            value = str(value)
        elif description == 'Item Access Rights':
            value = ACCESS_RIGHTS[value]
        elif description == 'Item Quality':
            if value > 3:
                value = 3
            value = OPC_QUALITY[value]
        else:
            pass
            #print(f'Error: Could not find description "{description}"  and value {input_value}')

        return value

    def get_tag_properties(self, tag, property_ids=[]) -> TagProperties:
        """
        This method returns the Properties of a tag. If you want to read many tags from a server it is
        recommended to only read the property ids that are required. Testing has shown, that this method is
        quite slow and leads to crashes on some servers.

        """
        property_ids_filter = property_ids
        properties_by_id = TagProperties().get_default_tag_properies_by_id()

        if not property_ids:
            count, property_ids, descriptions, datatypes = self.get_available_properties(tag)

            for result in zip(property_ids, descriptions, datatypes):
                property_item = properties_by_id.get(result[0], TagPropertyItem())
                property_item.property_id = result[0]
                property_item.description = result[1]
                property_item.available = True
                property_item.data_type = VtType(result[2]).name
                properties_by_id[result[0]] = property_item

            property_ids_cleaned = [p for p in property_ids if p > 0]

        if property_ids_filter:
            property_ids_cleaned = [p for p in property_ids if p in property_ids_filter]
        try:
            # print(f"self.opc_client.GetItemProperties('{item_id}', {len(property_ids_cleaned)},{property_ids_cleaned})")
            # GetItemProperties needs property id "0" to work properly.
            item_properties_values, errors = self.opc_client.GetItemProperties(tag, len(property_ids_cleaned), [0] + property_ids_cleaned)
        except pythoncom.com_error as err:
            error_msg = f"Error reading properties of '{tag}' {self._get_error_str(err)}"
            raise OPCError(error_msg)

        for (property_id, property_value) in zip(property_ids_cleaned, item_properties_values):
            property_item = properties_by_id[property_id]
            property_item.value = self._property_value_conversion(property_item.description, property_value)

        tag_properties = TagProperties().from_tag_property_items_by_id(tag, properties_by_id)
        return tag_properties, errors

    def get_error_string(self, error_id: int):
        return self.opc_client.GetErrorString(error_id)

    def _get_error_str(self, err):
        """Return the error string for a OPC or COM error code"""

        hr, msg, exc, arg = err.args

        if exc == None:
            error_str = str(msg)
        else:
            scode = exc[5]

            try:
                opc_err_str = self._opc.GetErrorString(scode).strip('\r\n')
            except:
                opc_err_str = None

            try:
                com_err_str = pythoncom.GetScodeString(scode).strip('\r\n')
            except:
                com_err_str = None

            # OPC error codes and COM error codes are overlapping concepts,
            # so we combine them together into a single error message.

            if opc_err_str is None and com_err_str is None:
                error_str = str(scode)
            elif opc_err_str is com_err_str:
                error_str = opc_err_str
            elif opc_err_str is None:
                error_str = com_err_str
            elif com_err_str is None:
                error_str = opc_err_str
            else:
                error_str = '%s (%s)' % (opc_err_str, com_err_str)

        return error_str

    def __str__(self):
        return f"OPCCom Object: {self.host} {self.server} {self.major_version}.{self.minor_version}"

    @staticmethod
    def get_quality_string(quality_bits):
        """Convert OPC quality bits to a descriptive string"""

        quality = (quality_bits >> 6) & 3
        return OPC_QUALITY[quality]

    @staticmethod
    def get_vt_type(datatype_number: int):
        return VtType(datatype_number).name
