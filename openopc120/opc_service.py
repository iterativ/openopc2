###########################################################################
#
# OpenOPC Gateway Service
#
# A Windows service providing remote access to the OpenOPC library.
#
# Copyright (c) 2007-2012 Barry Barnreiter (barry_b@users.sourceforge.net)
# Copyright (c) 2014 Anton D. Kachalov (mouse@yandex.ru)
# Copyright (c) 2017 José A. Maita (jose.a.maita@gmail.com)
#
###########################################################################

import os
import select
import sys

import logging

import servicemanager
import win32event
import win32service
import win32serviceutil
import winerror

import Pyro4.core

from opc_gateway_server import OpenOpcGatewayServer
from openopc120.opc_da_client import __version__

logger = logging.getLogger(__name__)

Pyro4.config.SERVERTYPE = 'thread'

OPC_GATE_HOST = os.environ.get('OPC_GATE_HOST', 'localhost')
OPC_GATE_PORT = os.environ.get('OPC_GATE_PORT', 7766)
OPC_CLASS = os.environ.get('OPC_GATE_Clas', "OPC.Automation")


class OpcService(win32serviceutil.ServiceFramework):
    _svc_name_ = "zzzOpenOPCService"
    _svc_display_name_ = "OpenOPC Gateway Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.print_config()
        self.host = os.environ.get('OPC_GATE_HOST', OPC_GATE_HOST)
        self.port = os.environ.get('OPC_GATE_PORT', OPC_GATE_PORT)
        self.opc_class = os.environ.get('OPC_GATE_Clas', OPC_CLASS)
        self.print_config()

    def SvcStop(self):
        servicemanager.LogInfoMsg('\nOpenOpcService Stopping service')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg(f'\nOpenOpcService Starting service on port {self.port}')

        open_opc_gateway_server = OpenOpcGatewayServer(host=self.host, port=self.port)
        daemon = open_opc_gateway_server.pyro_deamon
        socks = daemon.sockets

        while win32event.WaitForSingleObject(self.hWaitStop, 0) != win32event.WAIT_OBJECT_0:
            ins, outs, exs = select.select(socks, [], [], 1)
            if ins:
                daemon.events(ins)

        daemon.shutdown()

    def print_config(self):
        welcome_message = f"""
        Started OpenOpcService
        Version:    {__version__}
        
        OPC_GATE_HOST:  {self.host}
        OPC_GATE_PORT:  {self.port}
        OPC_CLASS:      {self.opc_class}
        """
        print(welcome_message)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(OpcService)
            servicemanager.Initialize('zzzOpenOPCService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details.winerror == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
                logger.info(' --foreground: Run OpenOPCService in foreground.')
            logger.exception(details)

    else:
        if sys.argv[1] == '--foreground':
            print('Starting OpenOPC Service in the foreground')
            open_opc_gateway_server = OpenOpcGatewayServer(host=OPC_GATE_HOST, port=OPC_GATE_PORT)
            daemon = open_opc_gateway_server.pyro_deamon
            while True:
                ins, outs, exs = select.select(daemon.sockets, [], [], 1)
                if ins:
                    daemon.events(ins)
        else:
            win32serviceutil.HandleCommandLine(OpcService)
