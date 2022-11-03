# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:37:30) [MSC v.1927 32 bit (Intel)]
# From type library 'gbda_aut.dll'
# On Wed Oct  5 16:31:54 2022
'Graybox OPC DA Automation Wrapper 1.01'
makepy_version = '0.5.01'
python_version = 0x30806f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg = pythoncom.Empty
defaultNamedNotOptArg = pythoncom.Empty
defaultUnnamedArg = pythoncom.Empty

CLSID = IID('{341A7851-5DEA-4022-B0D6-F9954AF9273D}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0


class constants:
    OPCReadable = 1  # from enum OPCAccessRights
    OPCWritable = 2  # from enum OPCAccessRights
    OPCCache = 1  # from enum OPCDataSource
    OPCDevice = 2  # from enum OPCDataSource
    OPCBadRights = -1073479674  # from enum OPCErrors
    OPCBadType = -1073479676  # from enum OPCErrors
    OPCClamp = 262158  # from enum OPCErrors
    OPCDuplicateName = -1073479668  # from enum OPCErrors
    OPCInuse = 262159  # from enum OPCErrors
    OPCInvalidConfig = -1073479664  # from enum OPCErrors
    OPCInvalidFilter = -1073479671  # from enum OPCErrors
    OPCInvalidHandle = -1073479679  # from enum OPCErrors
    OPCInvalidItemID = -1073479672  # from enum OPCErrors
    OPCInvalidPID = -1073479165  # from enum OPCErrors
    OPCNotFound = -1073479663  # from enum OPCErrors
    OPCPublic = -1073479675  # from enum OPCErrors
    OPCRange = -1073479669  # from enum OPCErrors
    OPCUnknownItemID = -1073479673  # from enum OPCErrors
    OPCUnknownPath = -1073479670  # from enum OPCErrors
    OPCUnsupportedRate = 262157  # from enum OPCErrors
    OPCFlat = 2  # from enum OPCNamespaceTypes
    OPCHierarchical = 1  # from enum OPCNamespaceTypes
    OPCQualityBad = 0  # from enum OPCQuality
    OPCQualityGood = 192  # from enum OPCQuality
    OPCQualityMask = 192  # from enum OPCQuality
    OPCQualityUncertain = 64  # from enum OPCQuality
    OPCLimitConst = 3  # from enum OPCQualityLimits
    OPCLimitHigh = 2  # from enum OPCQualityLimits
    OPCLimitLow = 1  # from enum OPCQualityLimits
    OPCLimitMask = 3  # from enum OPCQualityLimits
    OPCLimitOk = 0  # from enum OPCQualityLimits
    OPCStatusCommFailure = 24  # from enum OPCQualityStatus
    OPCStatusConfigError = 4  # from enum OPCQualityStatus
    OPCStatusDeviceFailure = 12  # from enum OPCQualityStatus
    OPCStatusEGUExceeded = 84  # from enum OPCQualityStatus
    OPCStatusLastKnown = 20  # from enum OPCQualityStatus
    OPCStatusLastUsable = 68  # from enum OPCQualityStatus
    OPCStatusLocalOverride = 216  # from enum OPCQualityStatus
    OPCStatusMask = 252  # from enum OPCQualityStatus
    OPCStatusNotConnected = 8  # from enum OPCQualityStatus
    OPCStatusOutOfService = 28  # from enum OPCQualityStatus
    OPCStatusSensorCal = 80  # from enum OPCQualityStatus
    OPCStatusSensorFailure = 16  # from enum OPCQualityStatus
    OPCStatusSubNormal = 88  # from enum OPCQualityStatus
    OPCDisconnected = 6  # from enum OPCServerState
    OPCFailed = 2  # from enum OPCServerState
    OPCNoconfig = 3  # from enum OPCServerState
    OPCRunning = 1  # from enum OPCServerState
    OPCSuspended = 4  # from enum OPCServerState
    OPCTest = 5  # from enum OPCServerState


class DIOPCGroupEvent:
    'OPC Group Events'
    CLSID = CLSID_Sink = IID('{9F752E9F-E509-4B5F-B607-B4FE4781D99B}')
    coclass_clsid = IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {
        1: "OnDataChange",
        2: "OnAsyncReadComplete",
        3: "OnAsyncWriteComplete",
        4: "OnAsyncCancelComplete",
    }

    def __init__(self, oobj=None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy
            cpc = oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp = cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie = cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp, self._olecp_cookie = cp, cookie

    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass

    def close(self):
        if self._olecp is not None:
            cp, cookie, self._olecp, self._olecp_cookie = self._olecp, self._olecp_cookie, None, None
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util
        if iid == self.CLSID_Sink: return win32com.server.util.wrap(self)

# Event Handlers
# If you create handlers, they should have the following prototypes:


#	def OnDataChange(self, TransactionID=defaultNamedNotOptArg, NumItems=defaultNamedNotOptArg, ClientHandles=defaultNamedNotOptArg, ItemValues=defaultNamedNotOptArg
#			, Qualities=defaultNamedNotOptArg, TimeStamps=defaultNamedNotOptArg):
#	def OnAsyncReadComplete(self, TransactionID=defaultNamedNotOptArg, NumItems=defaultNamedNotOptArg, ClientHandles=defaultNamedNotOptArg, ItemValues=defaultNamedNotOptArg
#			, Qualities=defaultNamedNotOptArg, TimeStamps=defaultNamedNotOptArg, Errors=defaultNamedNotOptArg):
#	def OnAsyncWriteComplete(self, TransactionID=defaultNamedNotOptArg, NumItems=defaultNamedNotOptArg, ClientHandles=defaultNamedNotOptArg, Errors=defaultNamedNotOptArg):
#	def OnAsyncCancelComplete(self, CancelID=defaultNamedNotOptArg):


class DIOPCGroupsEvent:
    'OPC Groups Event'
    CLSID = CLSID_Sink = IID('{7801E80B-3F5B-4F65-9AC8-2C50213D6E13}')
    coclass_clsid = IID('{3088F151-40A7-4B34-9384-56F1BC1DEE9C}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {
        1: "OnGlobalDataChange",
    }

    def __init__(self, oobj=None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy
            cpc = oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp = cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie = cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp, self._olecp_cookie = cp, cookie

    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass

    def close(self):
        if self._olecp is not None:
            cp, cookie, self._olecp, self._olecp_cookie = self._olecp, self._olecp_cookie, None, None
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util
        if iid == self.CLSID_Sink: return win32com.server.util.wrap(self)

# Event Handlers
# If you create handlers, they should have the following prototypes:


#	def OnGlobalDataChange(self, TransactionID=defaultNamedNotOptArg, GroupHandle=defaultNamedNotOptArg, NumItems=defaultNamedNotOptArg, ClientHandles=defaultNamedNotOptArg
#			, ItemValues=defaultNamedNotOptArg, Qualities=defaultNamedNotOptArg, TimeStamps=defaultNamedNotOptArg):


class DIOPCServerEvent:
    'OPC Server Event'
    CLSID = CLSID_Sink = IID('{ABAC1580-2CAE-469C-B35E-E2BAB7DDD919}')
    coclass_clsid = IID('{2A1B069C-BC3D-41AD-B73C-1161A8578A8D}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {
        1: "OnServerShutDown",
    }

    def __init__(self, oobj=None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy
            cpc = oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp = cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie = cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp, self._olecp_cookie = cp, cookie

    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass

    def close(self):
        if self._olecp is not None:
            cp, cookie, self._olecp, self._olecp_cookie = self._olecp, self._olecp_cookie, None, None
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util
        if iid == self.CLSID_Sink: return win32com.server.util.wrap(self)

# Event Handlers
# If you create handlers, they should have the following prototypes:


#	def OnServerShutDown(self, Reason=defaultNamedNotOptArg):


from win32com.client import DispatchBaseClass


class IOPCActivator(DispatchBaseClass):
    'Used to associate existing COM servers with a OPCAutoServer object.'
    CLSID = IID('{48BA9C63-26ED-4210-BE97-396CFD08658A}')
    coclass_clsid = IID('{2596B3D9-E937-4BA1-A3B1-8B72124AF57D}')

    # Result is of type IOPCAutoServer
    def Attach(self, Server=defaultNamedNotOptArg, ProgID=defaultNamedNotOptArg, NodeName=defaultNamedOptArg):
        'Returns an automation wrapper instance for an server existing COM server.'
        ret = self._oleobj_.InvokeTypes(1610743808, LCID, 1, (9, 0), ((13, 1), (8, 1), (12, 17)), Server
                                        , ProgID, NodeName)
        if ret is not None:
            ret = Dispatch(ret, 'Attach', '{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}')
        return ret

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IOPCAutoServer(DispatchBaseClass):
    'OPCServer Object'
    CLSID = IID('{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}')
    coclass_clsid = IID('{2A1B069C-BC3D-41AD-B73C-1161A8578A8D}')

    def Connect(self, ProgID=defaultNamedNotOptArg, Node=defaultNamedOptArg):
        'Connects to an OPC Server with the specified name and node'
        return self._oleobj_.InvokeTypes(1610743826, LCID, 1, (24, 0), ((8, 1), (12, 17)), ProgID
                                         , Node)

    # Result is of type OPCBrowser
    def CreateBrowser(self):
        'Create a new OPCBrowser Object'
        ret = self._oleobj_.InvokeTypes(1610743828, LCID, 1, (9, 0), (), )
        if ret is not None:
            ret = Dispatch(ret, 'CreateBrowser', '{E79CC822-741F-4D1E-974E-1CE76B155FD6}')
        return ret

    def Disconnect(self):
        'Terminate the connection with the OPC Server'
        return self._oleobj_.InvokeTypes(1610743827, LCID, 1, (24, 0), (), )

    def GetErrorString(self, ErrorCode=defaultNamedNotOptArg):
        'Convert an error code to a descriptive string'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(1610743829, LCID, 1, (8, 0), ((3, 1),), ErrorCode
                                         )

    def GetItemProperties(self, ItemID=defaultNamedNotOptArg, Count=defaultNamedNotOptArg,
                          PropertyIDs=defaultNamedNotOptArg, PropertyValues=pythoncom.Missing
                          , Errors=pythoncom.Missing):
        'Returns the properties for the specified item.'
        return self._ApplyTypes_(1610743832, 1, (24, 0), ((8, 1), (3, 1), (24579, 1), (24588, 2), (24579, 2)),
                                 'GetItemProperties', None, ItemID
                                 , Count, PropertyIDs, PropertyValues, Errors)

    def GetOPCServers(self, Node=defaultNamedOptArg):
        'Returns an array of Server names on the specified node'
        return self._ApplyTypes_(1610743825, 1, (12, 0), ((12, 17),), 'GetOPCServers', None, Node
                                 )

    def LookupItemIDs(self, ItemID=defaultNamedNotOptArg, Count=defaultNamedNotOptArg,
                      PropertyIDs=defaultNamedNotOptArg, NewItemIDs=pythoncom.Missing
                      , Errors=pythoncom.Missing):
        'Returns the item ids for the specified properties.'
        return self._ApplyTypes_(1610743833, 1, (24, 0), ((8, 1), (3, 1), (24579, 1), (24584, 2), (24579, 2)),
                                 'LookupItemIDs', None, ItemID
                                 , Count, PropertyIDs, NewItemIDs, Errors)

    def QueryAvailableLocaleIDs(self):
        'Returns the LocaleIDs supported by this server'
        return self._ApplyTypes_(1610743830, 1, (12, 0), (), 'QueryAvailableLocaleIDs', None, )

    def QueryAvailableProperties(self, ItemID=defaultNamedNotOptArg, Count=pythoncom.Missing,
                                 PropertyIDs=pythoncom.Missing, Descriptions=pythoncom.Missing
                                 , DataTypes=pythoncom.Missing):
        'Returns the properties available for the specified item.'
        return self._ApplyTypes_(1610743831, 1, (24, 0), ((8, 1), (16387, 2), (24579, 2), (24584, 2), (24578, 2)),
                                 'QueryAvailableProperties', None, ItemID
                                 , Count, PropertyIDs, Descriptions, DataTypes)

    _prop_map_get_ = {
        "Bandwidth": (1610743822, 2, (3, 0), (), "Bandwidth", None),
        "BuildNumber": (1610743813, 2, (2, 0), (), "BuildNumber", None),
        "ClientName": (1610743818, 2, (8, 0), (), "ClientName", None),
        "CurrentTime": (1610743809, 2, (7, 0), (), "CurrentTime", None),
        "LastUpdateTime": (1610743810, 2, (7, 0), (), "LastUpdateTime", None),
        "LocaleID": (1610743820, 2, (3, 0), (), "LocaleID", None),
        "MajorVersion": (1610743811, 2, (2, 0), (), "MajorVersion", None),
        "MinorVersion": (1610743812, 2, (2, 0), (), "MinorVersion", None),
        # Method 'OPCGroups' returns object of type 'OPCGroups'
        "OPCGroups": (0, 2, (13, 0), (), "OPCGroups", '{3088F151-40A7-4B34-9384-56F1BC1DEE9C}'),
        "PublicGroupNames": (1610743824, 2, (12, 0), (), "PublicGroupNames", None),
        "ServerName": (1610743816, 2, (8, 0), (), "ServerName", None),
        "ServerNode": (1610743817, 2, (8, 0), (), "ServerNode", None),
        "ServerState": (1610743815, 2, (3, 0), (), "ServerState", None),
        "StartTime": (1610743808, 2, (7, 0), (), "StartTime", None),
        "VendorInfo": (1610743814, 2, (8, 0), (), "VendorInfo", None),
    }
    _prop_map_put_ = {
        "ClientName": ((1610743818, LCID, 4, 0), ()),
        "LocaleID": ((1610743820, LCID, 4, 0), ()),
    }

    # Default property for this class is 'OPCGroups'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (13, 0), (), "OPCGroups", '{3088F151-40A7-4B34-9384-56F1BC1DEE9C}'))

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IOPCGroup(DispatchBaseClass):
    'OPC Group Object'
    CLSID = IID('{DC37E960-DAEA-4F78-A551-76D115F50045}')
    coclass_clsid = IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')

    def AsyncCancel(self, CancelID=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(1610743833, LCID, 1, (24, 0), ((3, 1),), CancelID
                                         )

    def AsyncRead(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg, Errors=pythoncom.Missing,
                  TransactionID=defaultNamedNotOptArg
                  , CancelID=pythoncom.Missing):
        return self._ApplyTypes_(1610743830, 1, (24, 0), ((3, 1), (24579, 1), (24579, 2), (3, 1), (16387, 2)),
                                 'AsyncRead', None, NumItems
                                 , ServerHandles, Errors, TransactionID, CancelID)

    def AsyncRefresh(self, Source=defaultNamedNotOptArg, TransactionID=defaultNamedNotOptArg,
                     CancelID=pythoncom.Missing):
        return self._ApplyTypes_(1610743832, 1, (24, 0), ((2, 1), (3, 1), (16387, 2)), 'AsyncRefresh', None, Source
                                 , TransactionID, CancelID)

    def AsyncWrite(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg,
                   Values=defaultNamedNotOptArg, Errors=pythoncom.Missing
                   , TransactionID=defaultNamedNotOptArg, CancelID=pythoncom.Missing):
        return self._ApplyTypes_(1610743831, 1, (24, 0),
                                 ((3, 1), (24579, 1), (24588, 1), (24579, 2), (3, 1), (16387, 2)), 'AsyncWrite', None,
                                 NumItems
                                 , ServerHandles, Values, Errors, TransactionID, CancelID
                                 )

    def SyncRead(self, Source=defaultNamedNotOptArg, NumItems=defaultNamedNotOptArg,
                 ServerHandles=defaultNamedNotOptArg, Values=pythoncom.Missing
                 , Errors=pythoncom.Missing, Qualities=pythoncom.Missing, TimeStamps=pythoncom.Missing):
        return self._ApplyTypes_(1610743828, 1, (24, 0),
                                 ((2, 1), (3, 1), (24579, 1), (24588, 2), (24579, 2), (16396, 18), (16396, 18)),
                                 'SyncRead', None, Source
                                 , NumItems, ServerHandles, Values, Errors, Qualities
                                 , TimeStamps)

    def SyncWrite(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg,
                  Values=defaultNamedNotOptArg, Errors=pythoncom.Missing):
        return self._ApplyTypes_(1610743829, 1, (24, 0), ((3, 1), (24579, 1), (24588, 1), (24579, 2)), 'SyncWrite',
                                 None, NumItems
                                 , ServerHandles, Values, Errors)

    _prop_map_get_ = {
        "ClientHandle": (1610743816, 2, (3, 0), (), "ClientHandle", None),
        "DeadBand": (1610743823, 2, (4, 0), (), "DeadBand", None),
        "IsActive": (1610743812, 2, (11, 0), (), "IsActive", None),
        "IsPublic": (1610743811, 2, (11, 0), (), "IsPublic", None),
        "IsSubscribed": (1610743814, 2, (11, 0), (), "IsSubscribed", None),
        "LocaleID": (1610743819, 2, (3, 0), (), "LocaleID", None),
        "Name": (1610743809, 2, (8, 0), (), "Name", None),
        # Method 'OPCItems' returns object of type 'OPCItems'
        "OPCItems": (0, 2, (9, 0), (), "OPCItems", '{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}'),
        # Method 'Parent' returns object of type 'IOPCAutoServer'
        "Parent": (1610743808, 2, (9, 0), (), "Parent", '{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}'),
        "ServerHandle": (1610743818, 2, (3, 0), (), "ServerHandle", None),
        "TimeBias": (1610743821, 2, (3, 0), (), "TimeBias", None),
        "UpdateRate": (1610743825, 2, (3, 0), (), "UpdateRate", None),
    }
    _prop_map_put_ = {
        "ClientHandle": ((1610743816, LCID, 4, 0), ()),
        "DeadBand": ((1610743823, LCID, 4, 0), ()),
        "IsActive": ((1610743812, LCID, 4, 0), ()),
        "IsSubscribed": ((1610743814, LCID, 4, 0), ()),
        "LocaleID": ((1610743819, LCID, 4, 0), ()),
        "Name": ((1610743809, LCID, 4, 0), ()),
        "TimeBias": ((1610743821, LCID, 4, 0), ()),
        "UpdateRate": ((1610743825, LCID, 4, 0), ()),
    }

    # Default property for this class is 'OPCItems'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (9, 0), (), "OPCItems", '{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}'))

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IOPCGroups(DispatchBaseClass):
    'Collection of OPC Group objects'
    CLSID = IID('{636E85DC-B386-4E13-B224-DC86FF6A96FA}')
    coclass_clsid = IID('{3088F151-40A7-4B34-9384-56F1BC1DEE9C}')

    # Result is of type OPCGroup
    def Add(self, Name=defaultNamedOptArg):
        'Adds an OPCGroup to the collection'
        ret = self._oleobj_.InvokeTypes(1610743822, LCID, 1, (13, 0), ((12, 17),), Name
                                        )
        if ret is not None:
            # See if this IUnknown is really an IDispatch
            try:
                ret = ret.QueryInterface(pythoncom.IID_IDispatch)
            except pythoncom.error:
                return ret
            ret = Dispatch(ret, 'Add', '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
        return ret

    # Result is of type OPCGroup
    def ConnectPublicGroup(self, Name=defaultNamedNotOptArg):
        'Adds an existing public OPCGroup to the collection'
        ret = self._oleobj_.InvokeTypes(1610743826, LCID, 1, (13, 0), ((8, 1),), Name
                                        )
        if ret is not None:
            # See if this IUnknown is really an IDispatch
            try:
                ret = ret.QueryInterface(pythoncom.IID_IDispatch)
            except pythoncom.error:
                return ret
            ret = Dispatch(ret, 'ConnectPublicGroup', '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
        return ret

    # Result is of type OPCGroup
    def GetOPCGroup(self, ItemSpecifier=defaultNamedNotOptArg):
        'Returns an OPCGroup specified by server handle or name'
        ret = self._oleobj_.InvokeTypes(1610743823, LCID, 1, (13, 0), ((12, 1),), ItemSpecifier
                                        )
        if ret is not None:
            # See if this IUnknown is really an IDispatch
            try:
                ret = ret.QueryInterface(pythoncom.IID_IDispatch)
            except pythoncom.error:
                return ret
            ret = Dispatch(ret, 'GetOPCGroup', '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
        return ret

    # Result is of type OPCGroup
    def Item(self, ItemSpecifier=defaultNamedNotOptArg):
        'Returns an OPCGroup by index (starts at 1) or name'
        ret = self._oleobj_.InvokeTypes(0, LCID, 1, (13, 0), ((12, 1),), ItemSpecifier
                                        )
        if ret is not None:
            # See if this IUnknown is really an IDispatch
            try:
                ret = ret.QueryInterface(pythoncom.IID_IDispatch)
            except pythoncom.error:
                return ret
            ret = Dispatch(ret, 'Item', '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
        return ret

    def Remove(self, ItemSpecifier=defaultNamedNotOptArg):
        'Removes an OPCGroup specified by server handle or name'
        return self._oleobj_.InvokeTypes(1610743825, LCID, 1, (24, 0), ((12, 1),), ItemSpecifier
                                         )

    def RemoveAll(self):
        'Remove all groups and their items'
        return self._oleobj_.InvokeTypes(1610743824, LCID, 1, (24, 0), (), )

    def RemovePublicGroup(self, ItemSpecifier=defaultNamedNotOptArg):
        'Removes a public OPCGroup specified by server handle or name'
        return self._oleobj_.InvokeTypes(1610743827, LCID, 1, (24, 0), ((12, 1),), ItemSpecifier
                                         )

    _prop_map_get_ = {
        "Count": (1610743819, 2, (3, 0), (), "Count", None),
        "DefaultGroupDeadband": (1610743813, 2, (4, 0), (), "DefaultGroupDeadband", None),
        "DefaultGroupIsActive": (1610743809, 2, (11, 0), (), "DefaultGroupIsActive", None),
        "DefaultGroupLocaleID": (1610743815, 2, (3, 0), (), "DefaultGroupLocaleID", None),
        "DefaultGroupTimeBias": (1610743817, 2, (3, 0), (), "DefaultGroupTimeBias", None),
        "DefaultGroupUpdateRate": (1610743811, 2, (3, 0), (), "DefaultGroupUpdateRate", None),
        # Method 'Parent' returns object of type 'IOPCAutoServer'
        "Parent": (1610743808, 2, (9, 0), (), "Parent", '{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}'),
    }
    _prop_map_put_ = {
        "DefaultGroupDeadband": ((1610743813, LCID, 4, 0), ()),
        "DefaultGroupIsActive": ((1610743809, LCID, 4, 0), ()),
        "DefaultGroupLocaleID": ((1610743815, LCID, 4, 0), ()),
        "DefaultGroupTimeBias": ((1610743817, LCID, 4, 0), ()),
        "DefaultGroupUpdateRate": ((1610743811, LCID, 4, 0), ()),
    }

    # Default method for this class is 'Item'
    def __call__(self, ItemSpecifier=defaultNamedNotOptArg):
        'Returns an OPCGroup by index (starts at 1) or name'
        ret = self._oleobj_.InvokeTypes(0, LCID, 1, (13, 0), ((12, 1),), ItemSpecifier
                                        )
        if ret is not None:
            # See if this IUnknown is really an IDispatch
            try:
                ret = ret.QueryInterface(pythoncom.IID_IDispatch)
            except pythoncom.error:
                return ret
            ret = Dispatch(ret, '__call__', '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
        return ret

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 2, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')

    # This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1610743819, 2, (3, 0), (), "Count", None))

    # This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True


class OPCBrowser(DispatchBaseClass):
    'OPC Browser'
    CLSID = IID('{E79CC822-741F-4D1E-974E-1CE76B155FD6}')
    coclass_clsid = None

    def GetAccessPaths(self, ItemID=defaultNamedNotOptArg):
        'Returns an array of Access Paths for an ItemID'
        return self._ApplyTypes_(1610743826, 1, (12, 0), ((8, 1),), 'GetAccessPaths', None, ItemID
                                 )

    def GetItemID(self, Leaf=defaultNamedNotOptArg):
        'Converts a leaf name to an ItemID'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(1610743825, LCID, 1, (8, 0), ((8, 1),), Leaf
                                         )

    def Item(self, ItemSpecifier=defaultNamedNotOptArg):
        'An indexer (starts at 1) for the current set of branch or leaf names.'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(1610743818, LCID, 1, (8, 0), ((12, 1),), ItemSpecifier
                                         )

    def MoveDown(self, Branch=defaultNamedNotOptArg):
        'Move down into this branch.'
        return self._oleobj_.InvokeTypes(1610743823, LCID, 1, (24, 0), ((8, 1),), Branch
                                         )

    def MoveTo(self, Branches=defaultNamedNotOptArg):
        'Move to this absolute position.'
        return self._oleobj_.InvokeTypes(1610743824, LCID, 1, (24, 0), ((24584, 1),), Branches
                                         )

    def MoveToRoot(self):
        'Move up to the top (root) of the tree.'
        return self._oleobj_.InvokeTypes(1610743822, LCID, 1, (24, 0), (), )

    def MoveUp(self):
        'Move up a level in the tree.'
        return self._oleobj_.InvokeTypes(1610743821, LCID, 1, (24, 0), (), )

    def ShowBranches(self):
        'Returns all branch names that match the current filters.'
        return self._oleobj_.InvokeTypes(1610743819, LCID, 1, (24, 0), (), )

    def ShowLeafs(self, Flat=defaultNamedOptArg):
        'Returns all leaf names that match the current filters.'
        return self._oleobj_.InvokeTypes(1610743820, LCID, 1, (24, 0), ((12, 17),), Flat
                                         )

    _prop_map_get_ = {
        "AccessRights": (1610743813, 2, (3, 0), (), "AccessRights", None),
        "Count": (1610743816, 2, (3, 0), (), "Count", None),
        "CurrentPosition": (1610743815, 2, (8, 0), (), "CurrentPosition", None),
        "DataType": (1610743811, 2, (2, 0), (), "DataType", None),
        "Filter": (1610743809, 2, (8, 0), (), "Filter", None),
        "Organization": (1610743808, 2, (3, 0), (), "Organization", None),
    }
    _prop_map_put_ = {
        "AccessRights": ((1610743813, LCID, 4, 0), ()),
        "DataType": ((1610743811, LCID, 4, 0), ()),
        "Filter": ((1610743809, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 2, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)

    # This class has Item property/method which allows indexed access with the object[key] syntax.
    # Some objects will accept a string or other type of key in addition to integers.
    # Note that many Office objects do not use zero-based indexing.
    def __getitem__(self, key):
        return self._get_good_object_(self._oleobj_.Invoke(*(1610743818, LCID, 1, 1, key)), "Item", None)

    # This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1610743816, 2, (3, 0), (), "Count", None))

    # This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True


class OPCItem(DispatchBaseClass):
    'OPC Item object'
    CLSID = IID('{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')
    coclass_clsid = None

    def Read(self, Source=defaultNamedNotOptArg, Value=pythoncom.Missing, Quality=pythoncom.Missing,
             TimeStamp=pythoncom.Missing):
        return self._ApplyTypes_(1610743825, 1, (24, 0), ((2, 1), (16396, 18), (16396, 18), (16396, 18)), 'Read', None,
                                 Source
                                 , Value, Quality, TimeStamp)

    def Write(self, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(1610743826, LCID, 1, (24, 0), ((12, 1),), Value
                                         )

    _prop_map_get_ = {
        "AccessPath": (1610743812, 2, (8, 0), (), "AccessPath", None),
        "AccessRights": (1610743813, 2, (3, 0), (), "AccessRights", None),
        "CanonicalDataType": (1610743822, 2, (2, 0), (), "CanonicalDataType", None),
        "ClientHandle": (1610743809, 2, (3, 0), (), "ClientHandle", None),
        "EUInfo": (1610743824, 2, (12, 0), (), "EUInfo", None),
        "EUType": (1610743823, 2, (2, 0), (), "EUType", None),
        "IsActive": (1610743815, 2, (11, 0), (), "IsActive", None),
        "ItemID": (1610743814, 2, (8, 0), (), "ItemID", None),
        # Method 'Parent' returns object of type 'OPCGroup'
        "Parent": (1610743808, 2, (13, 0), (), "Parent", '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}'),
        "Quality": (1610743820, 2, (3, 0), (), "Quality", None),
        "RequestedDataType": (1610743817, 2, (2, 0), (), "RequestedDataType", None),
        "ServerHandle": (1610743811, 2, (3, 0), (), "ServerHandle", None),
        "TimeStamp": (1610743821, 2, (7, 0), (), "TimeStamp", None),
        "Value": (0, 2, (12, 0), (), "Value", None),
    }
    _prop_map_put_ = {
        "ClientHandle": ((1610743809, LCID, 4, 0), ()),
        "IsActive": ((1610743815, LCID, 4, 0), ()),
        "RequestedDataType": ((1610743817, LCID, 4, 0), ()),
    }

    # Default property for this class is 'Value'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Value", None))

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class OPCItems(DispatchBaseClass):
    'Collection of OPC Item objects'
    CLSID = IID('{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}')
    coclass_clsid = None

    # Result is of type OPCItem
    def AddItem(self, ItemID=defaultNamedNotOptArg, ClientHandle=defaultNamedNotOptArg):
        'Adds an OPCItem object to the collection'
        ret = self._oleobj_.InvokeTypes(1610743819, LCID, 1, (9, 0), ((8, 1), (3, 1)), ItemID
                                        , ClientHandle)
        if ret is not None:
            ret = Dispatch(ret, 'AddItem', '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')
        return ret

    def AddItems(self, NumItems=defaultNamedNotOptArg, ItemIDs=defaultNamedNotOptArg,
                 ClientHandles=defaultNamedNotOptArg, ServerHandles=pythoncom.Missing
                 , Errors=pythoncom.Missing, RequestedDataTypes=defaultNamedOptArg, AccessPaths=defaultNamedOptArg):
        'Adds OPCItem objects to the collection'
        return self._ApplyTypes_(1610743820, 1, (24, 0),
                                 ((3, 1), (24584, 1), (24579, 1), (24579, 2), (24579, 2), (12, 17), (12, 17)),
                                 'AddItems', None, NumItems
                                 , ItemIDs, ClientHandles, ServerHandles, Errors, RequestedDataTypes
                                 , AccessPaths)

    # Result is of type OPCItem
    def GetOPCItem(self, ServerHandle=defaultNamedNotOptArg):
        'Returns an OPCItem specified by server handle'
        ret = self._oleobj_.InvokeTypes(1610743818, LCID, 1, (9, 0), ((3, 1),), ServerHandle
                                        )
        if ret is not None:
            ret = Dispatch(ret, 'GetOPCItem', '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')
        return ret

    # Result is of type OPCItem
    def Item(self, ItemSpecifier=defaultNamedNotOptArg):
        'Returns an OPCItem by index (starts at 1)'
        ret = self._oleobj_.InvokeTypes(0, LCID, 1, (9, 0), ((12, 1),), ItemSpecifier
                                        )
        if ret is not None:
            ret = Dispatch(ret, 'Item', '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')
        return ret

    def Remove(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg, Errors=pythoncom.Missing):
        'Removes OPCItem objects from the collection'
        return self._ApplyTypes_(1610743821, 1, (24, 0), ((3, 1), (24579, 1), (24579, 2)), 'Remove', None, NumItems
                                 , ServerHandles, Errors)

    def SetActive(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg,
                  ActiveState=defaultNamedNotOptArg, Errors=pythoncom.Missing):
        'Set the active state of OPCItem objects'
        return self._ApplyTypes_(1610743823, 1, (24, 0), ((3, 1), (24579, 1), (11, 1), (24579, 2)), 'SetActive', None,
                                 NumItems
                                 , ServerHandles, ActiveState, Errors)

    def SetClientHandles(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg,
                         ClientHandles=defaultNamedNotOptArg, Errors=pythoncom.Missing):
        'Set the Client handles of OPCItem objects'
        return self._ApplyTypes_(1610743824, 1, (24, 0), ((3, 1), (24579, 1), (24579, 1), (24579, 2)),
                                 'SetClientHandles', None, NumItems
                                 , ServerHandles, ClientHandles, Errors)

    def SetDataTypes(self, NumItems=defaultNamedNotOptArg, ServerHandles=defaultNamedNotOptArg,
                     RequestedDataTypes=defaultNamedNotOptArg, Errors=pythoncom.Missing):
        'Set the Data Types of OPCItem objects'
        return self._ApplyTypes_(1610743825, 1, (24, 0), ((3, 1), (24579, 1), (24579, 1), (24579, 2)), 'SetDataTypes',
                                 None, NumItems
                                 , ServerHandles, RequestedDataTypes, Errors)

    def Validate(self, NumItems=defaultNamedNotOptArg, ItemIDs=defaultNamedNotOptArg, Errors=pythoncom.Missing,
                 RequestedDataTypes=defaultNamedOptArg
                 , AccessPaths=defaultNamedOptArg):
        'Validates a set of item ids without adding them to the collection.'
        return self._ApplyTypes_(1610743822, 1, (24, 0), ((3, 1), (24584, 1), (24579, 2), (12, 17), (12, 17)),
                                 'Validate', None, NumItems
                                 , ItemIDs, Errors, RequestedDataTypes, AccessPaths)

    _prop_map_get_ = {
        "Count": (1610743815, 2, (3, 0), (), "Count", None),
        "DefaultAccessPath": (1610743811, 2, (8, 0), (), "DefaultAccessPath", None),
        "DefaultIsActive": (1610743813, 2, (11, 0), (), "DefaultIsActive", None),
        "DefaultRequestedDataType": (1610743809, 2, (2, 0), (), "DefaultRequestedDataType", None),
        # Method 'Parent' returns object of type 'OPCGroup'
        "Parent": (1610743808, 2, (13, 0), (), "Parent", '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}'),
    }
    _prop_map_put_ = {
        "DefaultAccessPath": ((1610743811, LCID, 4, 0), ()),
        "DefaultIsActive": ((1610743813, LCID, 4, 0), ()),
        "DefaultRequestedDataType": ((1610743809, LCID, 4, 0), ()),
    }

    # Default method for this class is 'Item'
    def __call__(self, ItemSpecifier=defaultNamedNotOptArg):
        'Returns an OPCItem by index (starts at 1)'
        ret = self._oleobj_.InvokeTypes(0, LCID, 1, (9, 0), ((12, 1),), ItemSpecifier
                                        )
        if ret is not None:
            ret = Dispatch(ret, '__call__', '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')
        return ret

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 2, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')

    # This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1610743815, 2, (3, 0), (), "Count", None))

    # This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True


from win32com.client import CoClassBaseClass


# This CoClass is known by the name 'Graybox.OPC.DAWrapper.Activator.1'
class OPCActivator(CoClassBaseClass):  # A CoClass
    # OPC Automation Server Activator
    CLSID = IID('{2596B3D9-E937-4BA1-A3B1-8B72124AF57D}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IOPCActivator,
    ]
    default_interface = IOPCActivator


class OPCGroup(CoClassBaseClass):  # A CoClass
    # OPC Automation Group
    CLSID = IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')
    coclass_sources = [
        DIOPCGroupEvent,
    ]
    default_source = DIOPCGroupEvent
    coclass_interfaces = [
        IOPCGroup,
    ]
    default_interface = IOPCGroup


class OPCGroups(CoClassBaseClass):  # A CoClass
    # OPC Automation Groups Collection
    CLSID = IID('{3088F151-40A7-4B34-9384-56F1BC1DEE9C}')
    coclass_sources = [
        DIOPCGroupsEvent,
    ]
    default_source = DIOPCGroupsEvent
    coclass_interfaces = [
        IOPCGroups,
    ]
    default_interface = IOPCGroups


# This CoClass is known by the name 'Graybox.OPC.DAWrapper.1'
class OPCServer(CoClassBaseClass):  # A CoClass
    # OPC Automation Server
    CLSID = IID('{2A1B069C-BC3D-41AD-B73C-1161A8578A8D}')
    coclass_sources = [
        DIOPCServerEvent,
    ]
    default_source = DIOPCServerEvent
    coclass_interfaces = [
        IOPCAutoServer,
    ]
    default_interface = IOPCAutoServer


IOPCActivator_vtables_dispatch_ = 1
IOPCActivator_vtables_ = [
    (('Attach', 'Server', 'ProgID', 'NodeName', 'ppWrapper',
      ), 1610743808, (1610743808, (), [(13, 1, None, None), (8, 1, None, None), (12, 17, None, None),
                                       (16393, 10, None, "IID('{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}')"), ], 1, 1, 4,
                      1, 28, (3, 0, None, None), 0,)),
]

IOPCAutoServer_vtables_dispatch_ = 1
IOPCAutoServer_vtables_ = [
    (('StartTime', 'StartTime',), 1610743808,
     (1610743808, (), [(16391, 10, None, None), ], 1, 2, 4, 0, 28, (3, 0, None, None), 0,)),
    (('CurrentTime', 'CurrentTime',), 1610743809,
     (1610743809, (), [(16391, 10, None, None), ], 1, 2, 4, 0, 32, (3, 0, None, None), 0,)),
    (('LastUpdateTime', 'LastUpdateTime',), 1610743810,
     (1610743810, (), [(16391, 10, None, None), ], 1, 2, 4, 0, 36, (3, 0, None, None), 0,)),
    (('MajorVersion', 'MajorVersion',), 1610743811,
     (1610743811, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 40, (3, 0, None, None), 0,)),
    (('MinorVersion', 'MinorVersion',), 1610743812,
     (1610743812, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 44, (3, 0, None, None), 0,)),
    (('BuildNumber', 'BuildNumber',), 1610743813,
     (1610743813, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 48, (3, 0, None, None), 0,)),
    (('VendorInfo', 'VendorInfo',), 1610743814,
     (1610743814, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 52, (3, 0, None, None), 0,)),
    (('ServerState', 'ServerState',), 1610743815,
     (1610743815, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 56, (3, 0, None, None), 0,)),
    (('ServerName', 'ServerName',), 1610743816,
     (1610743816, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 60, (3, 0, None, None), 0,)),
    (('ServerNode', 'ServerNode',), 1610743817,
     (1610743817, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 64, (3, 0, None, None), 0,)),
    (('ClientName', 'ClientName',), 1610743818,
     (1610743818, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 68, (3, 0, None, None), 0,)),
    (('ClientName', 'ClientName',), 1610743818,
     (1610743818, (), [(8, 1, None, None), ], 1, 4, 4, 0, 72, (3, 0, None, None), 0,)),
    (('LocaleID', 'LocaleID',), 1610743820,
     (1610743820, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 76, (3, 0, None, None), 0,)),
    (('LocaleID', 'LocaleID',), 1610743820,
     (1610743820, (), [(3, 1, None, None), ], 1, 4, 4, 0, 80, (3, 0, None, None), 0,)),
    (('Bandwidth', 'Bandwidth',), 1610743822,
     (1610743822, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 84, (3, 0, None, None), 0,)),
    (('OPCGroups', 'ppGroups',), 0, (
    0, (), [(16397, 10, None, "IID('{3088F151-40A7-4B34-9384-56F1BC1DEE9C}')"), ], 1, 2, 4, 0, 88, (3, 0, None, None),
    0,)),
    (('PublicGroupNames', 'PublicGroups',), 1610743824,
     (1610743824, (), [(16396, 10, None, None), ], 1, 2, 4, 0, 92, (3, 0, None, None), 0,)),
    (('GetOPCServers', 'Node', 'OPCServers',), 1610743825, (1610743825, (), [(12, 17, None, None),
                                                                             (16396, 10, None, None), ], 1, 1, 4, 1, 96,
                                                            (3, 0, None, None), 0,)),
    (('Connect', 'ProgID', 'Node',), 1610743826, (1610743826, (), [(8, 1, None, None),
                                                                   (12, 17, None, None), ], 1, 1, 4, 1, 100,
                                                  (3, 0, None, None), 0,)),
    (('Disconnect',), 1610743827, (1610743827, (), [], 1, 1, 4, 0, 104, (3, 0, None, None), 0,)),
    (('CreateBrowser', 'ppBrowser',), 1610743828, (
    1610743828, (), [(16393, 10, None, "IID('{E79CC822-741F-4D1E-974E-1CE76B155FD6}')"), ], 1, 1, 4, 0, 108,
    (3, 0, None, None), 0,)),
    (('GetErrorString', 'ErrorCode', 'ErrorString',), 1610743829, (1610743829, (), [(3, 1, None, None),
                                                                                    (16392, 10, None, None), ], 1, 1, 4,
                                                                   0, 112, (3, 0, None, None), 0,)),
    (('QueryAvailableLocaleIDs', 'LocaleIDs',), 1610743830,
     (1610743830, (), [(16396, 10, None, None), ], 1, 1, 4, 0, 116, (3, 0, None, None), 0,)),
    (('QueryAvailableProperties', 'ItemID', 'Count', 'PropertyIDs', 'Descriptions',
      'DataTypes',), 1610743831, (1610743831, (), [(8, 1, None, None), (16387, 2, None, None), (24579, 2, None, None),
                                                   (24584, 2, None, None), (24578, 2, None, None), ], 1, 1, 4, 0, 120,
                                  (3, 0, None, None), 0,)),
    (('GetItemProperties', 'ItemID', 'Count', 'PropertyIDs', 'PropertyValues',
      'Errors',), 1610743832, (1610743832, (), [(8, 1, None, None), (3, 1, None, None), (24579, 1, None, None),
                                                (24588, 2, None, None), (24579, 2, None, None), ], 1, 1, 4, 0, 124,
                               (3, 0, None, None), 0,)),
    (('LookupItemIDs', 'ItemID', 'Count', 'PropertyIDs', 'NewItemIDs',
      'Errors',), 1610743833, (1610743833, (), [(8, 1, None, None), (3, 1, None, None), (24579, 1, None, None),
                                                (24584, 2, None, None), (24579, 2, None, None), ], 1, 1, 4, 0, 128,
                               (3, 0, None, None), 0,)),
]

IOPCGroup_vtables_dispatch_ = 1
IOPCGroup_vtables_ = [
    (('Parent', 'ppParent',), 1610743808, (
    1610743808, (), [(16393, 10, None, "IID('{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}')"), ], 1, 2, 4, 0, 28,
    (3, 0, None, None), 0,)),
    (('Name', 'Name',), 1610743809,
     (1610743809, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 32, (3, 0, None, None), 0,)),
    (('Name', 'Name',), 1610743809, (1610743809, (), [(8, 1, None, None), ], 1, 4, 4, 0, 36, (3, 0, None, None), 0,)),
    (('IsPublic', 'IsPublic',), 1610743811,
     (1610743811, (), [(16395, 10, None, None), ], 1, 2, 4, 0, 40, (3, 0, None, None), 0,)),
    (('IsActive', 'IsActive',), 1610743812,
     (1610743812, (), [(16395, 10, None, None), ], 1, 2, 4, 0, 44, (3, 0, None, None), 0,)),
    (('IsActive', 'IsActive',), 1610743812,
     (1610743812, (), [(11, 1, None, None), ], 1, 4, 4, 0, 48, (3, 0, None, None), 0,)),
    (('IsSubscribed', 'IsSubscribed',), 1610743814,
     (1610743814, (), [(16395, 10, None, None), ], 1, 2, 4, 0, 52, (3, 0, None, None), 0,)),
    (('IsSubscribed', 'IsSubscribed',), 1610743814,
     (1610743814, (), [(11, 1, None, None), ], 1, 4, 4, 0, 56, (3, 0, None, None), 0,)),
    (('ClientHandle', 'ClientHandle',), 1610743816,
     (1610743816, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 60, (3, 0, None, None), 0,)),
    (('ClientHandle', 'ClientHandle',), 1610743816,
     (1610743816, (), [(3, 1, None, None), ], 1, 4, 4, 0, 64, (3, 0, None, None), 0,)),
    (('ServerHandle', 'ServerHandle',), 1610743818,
     (1610743818, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 68, (3, 0, None, None), 0,)),
    (('LocaleID', 'LocaleID',), 1610743819,
     (1610743819, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 72, (3, 0, None, None), 0,)),
    (('LocaleID', 'LocaleID',), 1610743819,
     (1610743819, (), [(3, 1, None, None), ], 1, 4, 4, 0, 76, (3, 0, None, None), 0,)),
    (('TimeBias', 'TimeBias',), 1610743821,
     (1610743821, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 80, (3, 0, None, None), 0,)),
    (('TimeBias', 'TimeBias',), 1610743821,
     (1610743821, (), [(3, 1, None, None), ], 1, 4, 4, 0, 84, (3, 0, None, None), 0,)),
    (('DeadBand', 'DeadBand',), 1610743823,
     (1610743823, (), [(16388, 10, None, None), ], 1, 2, 4, 0, 88, (3, 0, None, None), 0,)),
    (('DeadBand', 'DeadBand',), 1610743823,
     (1610743823, (), [(4, 1, None, None), ], 1, 4, 4, 0, 92, (3, 0, None, None), 0,)),
    (('UpdateRate', 'UpdateRate',), 1610743825,
     (1610743825, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 96, (3, 0, None, None), 0,)),
    (('UpdateRate', 'UpdateRate',), 1610743825,
     (1610743825, (), [(3, 1, None, None), ], 1, 4, 4, 0, 100, (3, 0, None, None), 0,)),
    (('OPCItems', 'ppItems',), 0, (
    0, (), [(16393, 10, None, "IID('{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}')"), ], 1, 2, 4, 0, 104, (3, 0, None, None),
    0,)),
    (('SyncRead', 'Source', 'NumItems', 'ServerHandles', 'Values',
      'Errors', 'Qualities', 'TimeStamps',), 1610743828, (1610743828, (), [(2, 1, None, None),
                                                                           (3, 1, None, None), (24579, 1, None, None),
                                                                           (24588, 2, None, None),
                                                                           (24579, 2, None, None),
                                                                           (16396, 18, None, None),
                                                                           (16396, 18, None, None), ], 1, 1, 4, 2, 108,
                                                          (3, 0, None, None), 0,)),
    (('SyncWrite', 'NumItems', 'ServerHandles', 'Values', 'Errors',
      ), 1610743829, (
     1610743829, (), [(3, 1, None, None), (24579, 1, None, None), (24588, 1, None, None), (24579, 2, None, None), ], 1,
     1, 4, 0, 112, (3, 0, None, None), 0,)),
    (('AsyncRead', 'NumItems', 'ServerHandles', 'Errors', 'TransactionID',
      'CancelID',), 1610743830, (1610743830, (), [(3, 1, None, None), (24579, 1, None, None), (24579, 2, None, None),
                                                  (3, 1, None, None), (16387, 2, None, None), ], 1, 1, 4, 0, 116,
                                 (3, 0, None, None), 0,)),
    (('AsyncWrite', 'NumItems', 'ServerHandles', 'Values', 'Errors',
      'TransactionID', 'CancelID',), 1610743831, (1610743831, (), [(3, 1, None, None), (24579, 1, None, None),
                                                                   (24588, 1, None, None), (24579, 2, None, None),
                                                                   (3, 1, None, None), (16387, 2, None, None), ], 1, 1,
                                                  4, 0, 120, (3, 0, None, None), 0,)),
    (('AsyncRefresh', 'Source', 'TransactionID', 'CancelID',), 1610743832, (1610743832, (), [
        (2, 1, None, None), (3, 1, None, None), (16387, 2, None, None), ], 1, 1, 4, 0, 124, (3, 0, None, None), 0,)),
    (('AsyncCancel', 'CancelID',), 1610743833,
     (1610743833, (), [(3, 1, None, None), ], 1, 1, 4, 0, 128, (3, 0, None, None), 0,)),
]

IOPCGroups_vtables_dispatch_ = 1
IOPCGroups_vtables_ = [
    (('Parent', 'ppParent',), 1610743808, (
    1610743808, (), [(16393, 10, None, "IID('{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}')"), ], 1, 2, 4, 0, 28,
    (3, 0, None, None), 0,)),
    (('DefaultGroupIsActive', 'DefaultGroupIsActive',), 1610743809,
     (1610743809, (), [(16395, 10, None, None), ], 1, 2, 4, 0, 32, (3, 0, None, None), 0,)),
    (('DefaultGroupIsActive', 'DefaultGroupIsActive',), 1610743809,
     (1610743809, (), [(11, 1, None, None), ], 1, 4, 4, 0, 36, (3, 0, None, None), 0,)),
    (('DefaultGroupUpdateRate', 'DefaultGroupUpdateRate',), 1610743811,
     (1610743811, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 40, (3, 0, None, None), 0,)),
    (('DefaultGroupUpdateRate', 'DefaultGroupUpdateRate',), 1610743811,
     (1610743811, (), [(3, 1, None, None), ], 1, 4, 4, 0, 44, (3, 0, None, None), 0,)),
    (('DefaultGroupDeadband', 'DefaultGroupDeadband',), 1610743813,
     (1610743813, (), [(16388, 10, None, None), ], 1, 2, 4, 0, 48, (3, 0, None, None), 0,)),
    (('DefaultGroupDeadband', 'DefaultGroupDeadband',), 1610743813,
     (1610743813, (), [(4, 1, None, None), ], 1, 4, 4, 0, 52, (3, 0, None, None), 0,)),
    (('DefaultGroupLocaleID', 'DefaultGroupLocaleID',), 1610743815,
     (1610743815, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 56, (3, 0, None, None), 0,)),
    (('DefaultGroupLocaleID', 'DefaultGroupLocaleID',), 1610743815,
     (1610743815, (), [(3, 1, None, None), ], 1, 4, 4, 0, 60, (3, 0, None, None), 0,)),
    (('DefaultGroupTimeBias', 'DefaultGroupTimeBias',), 1610743817,
     (1610743817, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 64, (3, 0, None, None), 0,)),
    (('DefaultGroupTimeBias', 'DefaultGroupTimeBias',), 1610743817,
     (1610743817, (), [(3, 1, None, None), ], 1, 4, 4, 0, 68, (3, 0, None, None), 0,)),
    (('Count', 'Count',), 1610743819,
     (1610743819, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 72, (3, 0, None, None), 0,)),
    (('_NewEnum', 'ppUnk',), -4, (-4, (), [(16397, 10, None, None), ], 1, 2, 4, 0, 76, (3, 0, None, None), 1,)),
    (('Item', 'ItemSpecifier', 'ppGroup',), 0, (0, (), [(12, 1, None, None),
                                                        (16397, 10, None,
                                                         "IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')"), ], 1, 1, 4,
                                                0, 80, (3, 0, None, None), 0,)),
    (('Add', 'Name', 'ppGroup',), 1610743822, (1610743822, (), [(12, 17, None, None),
                                                                (16397, 10, None,
                                                                 "IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')"), ], 1,
                                               1, 4, 1, 84, (3, 0, None, None), 0,)),
    (('GetOPCGroup', 'ItemSpecifier', 'ppGroup',), 1610743823, (1610743823, (), [(12, 1, None, None),
                                                                                 (16397, 10, None,
                                                                                  "IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')"), ],
                                                                1, 1, 4, 0, 88, (3, 0, None, None), 0,)),
    (('RemoveAll',), 1610743824, (1610743824, (), [], 1, 1, 4, 0, 92, (3, 0, None, None), 0,)),
    (('Remove', 'ItemSpecifier',), 1610743825,
     (1610743825, (), [(12, 1, None, None), ], 1, 1, 4, 0, 96, (3, 0, None, None), 0,)),
    (('ConnectPublicGroup', 'Name', 'ppGroup',), 1610743826, (1610743826, (), [(8, 1, None, None),
                                                                               (16397, 10, None,
                                                                                "IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')"), ],
                                                              1, 1, 4, 0, 100, (3, 0, None, None), 0,)),
    (('RemovePublicGroup', 'ItemSpecifier',), 1610743827,
     (1610743827, (), [(12, 1, None, None), ], 1, 1, 4, 0, 104, (3, 0, None, None), 0,)),
]

OPCBrowser_vtables_dispatch_ = 1
OPCBrowser_vtables_ = [
    (('Organization', 'Organization',), 1610743808,
     (1610743808, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 28, (3, 0, None, None), 0,)),
    (('Filter', 'Filter',), 1610743809,
     (1610743809, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 32, (3, 0, None, None), 0,)),
    (('Filter', 'Filter',), 1610743809,
     (1610743809, (), [(8, 1, None, None), ], 1, 4, 4, 0, 36, (3, 0, None, None), 0,)),
    (('DataType', 'DataType',), 1610743811,
     (1610743811, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 40, (3, 0, None, None), 0,)),
    (('DataType', 'DataType',), 1610743811,
     (1610743811, (), [(2, 1, None, None), ], 1, 4, 4, 0, 44, (3, 0, None, None), 0,)),
    (('AccessRights', 'AccessRights',), 1610743813,
     (1610743813, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 48, (3, 0, None, None), 0,)),
    (('AccessRights', 'AccessRights',), 1610743813,
     (1610743813, (), [(3, 1, None, None), ], 1, 4, 4, 0, 52, (3, 0, None, None), 0,)),
    (('CurrentPosition', 'CurrentPosition',), 1610743815,
     (1610743815, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 56, (3, 0, None, None), 0,)),
    (('Count', 'Count',), 1610743816,
     (1610743816, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 60, (3, 0, None, None), 0,)),
    (('_NewEnum', 'ppUnk',), -4, (-4, (), [(16397, 10, None, None), ], 1, 2, 4, 0, 64, (3, 0, None, None), 1,)),
    (('Item', 'ItemSpecifier', 'Item',), 1610743818, (1610743818, (), [(12, 1, None, None),
                                                                       (16392, 10, None, None), ], 1, 1, 4, 0, 68,
                                                      (3, 0, None, None), 0,)),
    (('ShowBranches',), 1610743819, (1610743819, (), [], 1, 1, 4, 0, 72, (3, 0, None, None), 0,)),
    (('ShowLeafs', 'Flat',), 1610743820,
     (1610743820, (), [(12, 17, None, None), ], 1, 1, 4, 1, 76, (3, 0, None, None), 0,)),
    (('MoveUp',), 1610743821, (1610743821, (), [], 1, 1, 4, 0, 80, (3, 0, None, None), 0,)),
    (('MoveToRoot',), 1610743822, (1610743822, (), [], 1, 1, 4, 0, 84, (3, 0, None, None), 0,)),
    (('MoveDown', 'Branch',), 1610743823,
     (1610743823, (), [(8, 1, None, None), ], 1, 1, 4, 0, 88, (3, 0, None, None), 0,)),
    (('MoveTo', 'Branches',), 1610743824,
     (1610743824, (), [(24584, 1, None, None), ], 1, 1, 4, 0, 92, (3, 0, None, None), 0,)),
    (('GetItemID', 'Leaf', 'ItemID',), 1610743825, (1610743825, (), [(8, 1, None, None),
                                                                     (16392, 10, None, None), ], 1, 1, 4, 0, 96,
                                                    (3, 0, None, None), 0,)),
    (('GetAccessPaths', 'ItemID', 'AccessPaths',), 1610743826, (1610743826, (), [(8, 1, None, None),
                                                                                 (16396, 10, None, None), ], 1, 1, 4, 0,
                                                                100, (3, 0, None, None), 0,)),
]

OPCItem_vtables_dispatch_ = 1
OPCItem_vtables_ = [
    (('Parent', 'Parent',), 1610743808, (
    1610743808, (), [(16397, 10, None, "IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')"), ], 1, 2, 4, 0, 28,
    (3, 0, None, None), 0,)),
    (('ClientHandle', 'ClientHandle',), 1610743809,
     (1610743809, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 32, (3, 0, None, None), 0,)),
    (('ClientHandle', 'ClientHandle',), 1610743809,
     (1610743809, (), [(3, 1, None, None), ], 1, 4, 4, 0, 36, (3, 0, None, None), 0,)),
    (('ServerHandle', 'ServerHandle',), 1610743811,
     (1610743811, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 40, (3, 0, None, None), 0,)),
    (('AccessPath', 'AccessPath',), 1610743812,
     (1610743812, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 44, (3, 0, None, None), 0,)),
    (('AccessRights', 'AccessRights',), 1610743813,
     (1610743813, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 48, (3, 0, None, None), 0,)),
    (('ItemID', 'ItemID',), 1610743814,
     (1610743814, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 52, (3, 0, None, None), 0,)),
    (('IsActive', 'IsActive',), 1610743815,
     (1610743815, (), [(16395, 10, None, None), ], 1, 2, 4, 0, 56, (3, 0, None, None), 0,)),
    (('IsActive', 'IsActive',), 1610743815,
     (1610743815, (), [(11, 1, None, None), ], 1, 4, 4, 0, 60, (3, 0, None, None), 0,)),
    (('RequestedDataType', 'RequestedDataType',), 1610743817,
     (1610743817, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 64, (3, 0, None, None), 0,)),
    (('RequestedDataType', 'RequestedDataType',), 1610743817,
     (1610743817, (), [(2, 1, None, None), ], 1, 4, 4, 0, 68, (3, 0, None, None), 0,)),
    (('Value', 'CurrentValue',), 0, (0, (), [(16396, 10, None, None), ], 1, 2, 4, 0, 72, (3, 0, None, None), 0,)),
    (('Quality', 'Quality',), 1610743820,
     (1610743820, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 76, (3, 0, None, None), 0,)),
    (('TimeStamp', 'TimeStamp',), 1610743821,
     (1610743821, (), [(16391, 10, None, None), ], 1, 2, 4, 0, 80, (3, 0, None, None), 0,)),
    (('CanonicalDataType', 'CanonicalDataType',), 1610743822,
     (1610743822, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 84, (3, 0, None, None), 0,)),
    (('EUType', 'EUType',), 1610743823,
     (1610743823, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 88, (3, 0, None, None), 0,)),
    (('EUInfo', 'EUInfo',), 1610743824,
     (1610743824, (), [(16396, 10, None, None), ], 1, 2, 4, 0, 92, (3, 0, None, None), 0,)),
    (('Read', 'Source', 'Value', 'Quality', 'TimeStamp',
      ), 1610743825, (
     1610743825, (), [(2, 1, None, None), (16396, 18, None, None), (16396, 18, None, None), (16396, 18, None, None), ],
     1, 1, 4, 3, 96, (3, 0, None, None), 0,)),
    (('Write', 'Value',), 1610743826,
     (1610743826, (), [(12, 1, None, None), ], 1, 1, 4, 0, 100, (3, 0, None, None), 0,)),
]

OPCItems_vtables_dispatch_ = 1
OPCItems_vtables_ = [
    (('Parent', 'ppParent',), 1610743808, (
    1610743808, (), [(16397, 10, None, "IID('{DFE64768-CCD1-4576-A47D-05ACA1E69CED}')"), ], 1, 2, 4, 0, 28,
    (3, 0, None, None), 0,)),
    (('DefaultRequestedDataType', 'DefaultRequestedDataType',), 1610743809,
     (1610743809, (), [(16386, 10, None, None), ], 1, 2, 4, 0, 32, (3, 0, None, None), 0,)),
    (('DefaultRequestedDataType', 'DefaultRequestedDataType',), 1610743809,
     (1610743809, (), [(2, 1, None, None), ], 1, 4, 4, 0, 36, (3, 0, None, None), 0,)),
    (('DefaultAccessPath', 'DefaultAccessPath',), 1610743811,
     (1610743811, (), [(16392, 10, None, None), ], 1, 2, 4, 0, 40, (3, 0, None, None), 0,)),
    (('DefaultAccessPath', 'DefaultAccessPath',), 1610743811,
     (1610743811, (), [(8, 1, None, None), ], 1, 4, 4, 0, 44, (3, 0, None, None), 0,)),
    (('DefaultIsActive', 'DefaultIsActive',), 1610743813,
     (1610743813, (), [(16395, 10, None, None), ], 1, 2, 4, 0, 48, (3, 0, None, None), 0,)),
    (('DefaultIsActive', 'DefaultIsActive',), 1610743813,
     (1610743813, (), [(11, 1, None, None), ], 1, 4, 4, 0, 52, (3, 0, None, None), 0,)),
    (('Count', 'Count',), 1610743815,
     (1610743815, (), [(16387, 10, None, None), ], 1, 2, 4, 0, 56, (3, 0, None, None), 0,)),
    (('_NewEnum', 'ppUnk',), -4, (-4, (), [(16397, 10, None, None), ], 1, 2, 4, 0, 60, (3, 0, None, None), 1,)),
    (('Item', 'ItemSpecifier', 'ppItem',), 0, (0, (), [(12, 1, None, None),
                                                       (16393, 10, None,
                                                        "IID('{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')"), ], 1, 1, 4, 0,
                                               64, (3, 0, None, None), 0,)),
    (('GetOPCItem', 'ServerHandle', 'ppItem',), 1610743818, (1610743818, (), [(3, 1, None, None),
                                                                              (16393, 10, None,
                                                                               "IID('{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')"), ],
                                                             1, 1, 4, 0, 68, (3, 0, None, None), 0,)),
    (('AddItem', 'ItemID', 'ClientHandle', 'ppItem',), 1610743819, (1610743819, (), [
        (8, 1, None, None), (3, 1, None, None), (16393, 10, None, "IID('{6CD1DF31-FCAC-45F7-9470-36F1423B5112}')"), ],
                                                                    1, 1, 4, 0, 72, (3, 0, None, None), 0,)),
    (('AddItems', 'NumItems', 'ItemIDs', 'ClientHandles', 'ServerHandles',
      'Errors', 'RequestedDataTypes', 'AccessPaths',), 1610743820, (1610743820, (), [(3, 1, None, None),
                                                                                     (24584, 1, None, None),
                                                                                     (24579, 1, None, None),
                                                                                     (24579, 2, None, None),
                                                                                     (24579, 2, None, None),
                                                                                     (12, 17, None, None),
                                                                                     (12, 17, None, None), ], 1, 1, 4,
                                                                    2, 76, (3, 0, None, None), 0,)),
    (('Remove', 'NumItems', 'ServerHandles', 'Errors',), 1610743821, (1610743821, (), [
        (3, 1, None, None), (24579, 1, None, None), (24579, 2, None, None), ], 1, 1, 4, 0, 80, (3, 0, None, None), 0,)),
    (('Validate', 'NumItems', 'ItemIDs', 'Errors', 'RequestedDataTypes',
      'AccessPaths',), 1610743822, (1610743822, (), [(3, 1, None, None), (24584, 1, None, None), (24579, 2, None, None),
                                                     (12, 17, None, None), (12, 17, None, None), ], 1, 1, 4, 2, 84,
                                    (3, 0, None, None), 0,)),
    (('SetActive', 'NumItems', 'ServerHandles', 'ActiveState', 'Errors',
      ), 1610743823, (
     1610743823, (), [(3, 1, None, None), (24579, 1, None, None), (11, 1, None, None), (24579, 2, None, None), ], 1, 1,
     4, 0, 88, (3, 0, None, None), 0,)),
    (('SetClientHandles', 'NumItems', 'ServerHandles', 'ClientHandles', 'Errors',
      ), 1610743824, (
     1610743824, (), [(3, 1, None, None), (24579, 1, None, None), (24579, 1, None, None), (24579, 2, None, None), ], 1,
     1, 4, 0, 92, (3, 0, None, None), 0,)),
    (('SetDataTypes', 'NumItems', 'ServerHandles', 'RequestedDataTypes', 'Errors',
      ), 1610743825, (
     1610743825, (), [(3, 1, None, None), (24579, 1, None, None), (24579, 1, None, None), (24579, 2, None, None), ], 1,
     1, 4, 0, 96, (3, 0, None, None), 0,)),
]

RecordMap = {
}

CLSIDToClassMap = {
    '{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}': IOPCAutoServer,
    '{636E85DC-B386-4E13-B224-DC86FF6A96FA}': IOPCGroups,
    '{7801E80B-3F5B-4F65-9AC8-2C50213D6E13}': DIOPCGroupsEvent,
    '{3088F151-40A7-4B34-9384-56F1BC1DEE9C}': OPCGroups,
    '{DC37E960-DAEA-4F78-A551-76D115F50045}': IOPCGroup,
    '{9F752E9F-E509-4B5F-B607-B4FE4781D99B}': DIOPCGroupEvent,
    '{DFE64768-CCD1-4576-A47D-05ACA1E69CED}': OPCGroup,
    '{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}': OPCItems,
    '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}': OPCItem,
    '{E79CC822-741F-4D1E-974E-1CE76B155FD6}': OPCBrowser,
    '{ABAC1580-2CAE-469C-B35E-E2BAB7DDD919}': DIOPCServerEvent,
    '{48BA9C63-26ED-4210-BE97-396CFD08658A}': IOPCActivator,
    '{2596B3D9-E937-4BA1-A3B1-8B72124AF57D}': OPCActivator,
    '{2A1B069C-BC3D-41AD-B73C-1161A8578A8D}': OPCServer,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict(CLSIDToClassMap)
VTablesToPackageMap = {}
VTablesToClassMap = {
    '{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}': 'IOPCAutoServer',
    '{636E85DC-B386-4E13-B224-DC86FF6A96FA}': 'IOPCGroups',
    '{DC37E960-DAEA-4F78-A551-76D115F50045}': 'IOPCGroup',
    '{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}': 'OPCItems',
    '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}': 'OPCItem',
    '{E79CC822-741F-4D1E-974E-1CE76B155FD6}': 'OPCBrowser',
    '{48BA9C63-26ED-4210-BE97-396CFD08658A}': 'IOPCActivator',
}

NamesToIIDMap = {
    'IOPCAutoServer': '{CAB0C53A-E6A6-4223-8AA2-14CAD6F14A3E}',
    'IOPCGroups': '{636E85DC-B386-4E13-B224-DC86FF6A96FA}',
    'DIOPCGroupsEvent': '{7801E80B-3F5B-4F65-9AC8-2C50213D6E13}',
    'IOPCGroup': '{DC37E960-DAEA-4F78-A551-76D115F50045}',
    'DIOPCGroupEvent': '{9F752E9F-E509-4B5F-B607-B4FE4781D99B}',
    'OPCItems': '{8A360CA7-F8D5-4A92-AB3C-D5DD4BF630F4}',
    'OPCItem': '{6CD1DF31-FCAC-45F7-9470-36F1423B5112}',
    'OPCBrowser': '{E79CC822-741F-4D1E-974E-1CE76B155FD6}',
    'DIOPCServerEvent': '{ABAC1580-2CAE-469C-B35E-E2BAB7DDD919}',
    'IOPCActivator': '{48BA9C63-26ED-4210-BE97-396CFD08658A}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)
