import string

import pythoncom
import win32com.client

from exceptions import OPCError


class OpcCom:
    def __init__(self, opc_class: str):
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

    def create_browser(self):
        return self.opc_client.CreateBrowser()

    def disconnect(self):
        self.opc_client.Disconnect()

    def server_name(self):
        return self.opc_client.ServerName

    def get_opc_servers(self, opc_host):
        return self.opc_client.GetOPCServers(opc_host)

    def get_properties(self, tag):
        (count, property_id, descriptions, datatypes) = list(self.opc_client.QueryAvailableProperties(tag))
        return count, property_id, descriptions, datatypes

    def __str__(self):
        return f"OPCCom Object: {self.host} {self.server} {self.minor_version}.{self.major_version}"
