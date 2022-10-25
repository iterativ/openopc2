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

import Pyro5.core

from openopc120.opc_gateway_server import main
from openopc120.config import open_opc_config
from openopc120.opc_da_client import __version__

logger = logging.getLogger(__name__)

Pyro5.config.SERVERTYPE = 'thread'



class OpcService(win32serviceutil.ServiceFramework):
    _svc_name_ = "zzzOpenOPCService"
    _svc_display_name_ = "OpenOPC Gateway Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.print_config()
        self.host = open_opc_config.OPC_GATEWAY_HOST
        self.port = open_opc_config.OPC_GATEWAY_PORT
        self.opc_class = open_opc_config.OPC_CLASS
        self.print_config()
        self.pyro_deamon = None

    def SvcStop(self):
        servicemanager.LogInfoMsg('\nOpenOpcService Stopping service')
        self.pyro_deamon.close()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg(f'\nOpenOpcService Starting service on port {self.port}')
        daemon = main(host=self.host, port=self.port)
        socks = daemon.sockets
        self.pyro_deamon = daemon

        while win32event.WaitForSingleObject(self.hWaitStop, 0) != win32event.WAIT_OBJECT_0:
            ins, outs, exs = select.select(socks, [], [], 1)
            if ins:
                daemon.events(ins)

        daemon.shutdown()

    def print_config(self):
        welcome_message = f"""python
        
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
            logger.exception(details)
            if details.winerror == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
                logger.error(' --foreground: Run OpenOPCService in foreground.')

    else:
        if sys.argv[1] == '--foreground':
            print('Starting OpenOPC Service in the foreground')

            daemon = main(host=open_opc_config.OPC_GATEWAY_HOST, port=open_opc_config.OPC_GATEWAY_PORT)

            while True:
                ins, outs, exs = select.select(daemon.sockets, [], [], 1)
                if ins:
                    daemon.events(ins)
        else:
            win32serviceutil.HandleCommandLine(OpcService)
