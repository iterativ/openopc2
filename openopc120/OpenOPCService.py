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
import time

import logging

import servicemanager
import win32event
import win32service
import win32serviceutil
import winerror

import Pyro4.core

from openopc120.OpenOPC import client, OPC_CLIENT, OPC_CLASS,  __version__

logger = logging.getLogger(__name__)

Pyro4.config.SERVERTYPE = 'thread'

OPC_GATE_HOST = os.environ['OPC_GATE_HOST']
OPC_GATE_PORT = int(os.environ['OPC_GATE_PORT'])
OPC_CLASS =  "OPC.Automation"

@Pyro4.expose  # needed for version 4.55+
class opc(object):
    def __init__(self):
        self._remote_hosts = {}
        self._init_times = {}
        self._tx_times = {}
        self._pyroDaemon = None

    def get_clients(self):
        """Return list of server instances as a list of (GUID,host,time) tuples"""

        # reg = Pyro4.core.DaemonObject(self._pyroDaemon).registered()[2:]
        reg1 = Pyro4.core.DaemonObject(self._pyroDaemon).registered()  # needed for version 4.55
        reg2 = [si for si in reg1 if si.find('obj_') == 0]
        reg = ["PYRO:{0}@{1}:{2}".format(obj, OPC_GATE_HOST, OPC_GATE_PORT) for obj in reg2]
        hosts = self._remote_hosts
        init_times = self._init_times
        tx_times = self._tx_times
        hlist = [(hosts[k] if k in hosts else '', init_times[k], tx_times[k]) for k in reg]
        return hlist

    def create_client(self):
        """Create a new OpenOPC instance in the Pyro server"""

        opc_obj = client(OPC_CLASS)
        uri = self._pyroDaemon.register(opc_obj)

        uuid = uri.asString()
        opc_obj._open_serv = self
        opc_obj._open_self = opc_obj
        opc_obj._open_host = OPC_GATE_HOST
        opc_obj._open_port = OPC_GATE_PORT
        opc_obj._open_guid = uuid

        remote_ip = uuid  # self.getLocalStorage().caller.addr[0]
        #        try:
        #            remote_name = socket.gethostbyaddr(remote_ip)[0]
        #            self._remote_hosts[uuid] = '%s (%s)' % (remote_ip, remote_name)
        #        except socket.herror:
        #            self._remote_hosts[uuid] = '%s' % (remote_ip)
        self._remote_hosts[uuid] = str(remote_ip)
        self._init_times[uuid] = time.time()
        self._tx_times[uuid] = time.time()
        return Pyro4.Proxy(uri)

    def release_client(self, obj):
        """Release an OpenOPC instance in the Pyro server"""

        self._pyroDaemon.unregister(obj)
        del self._remote_hosts[obj.GUID()]
        del self._init_times[obj.GUID()]
        del self._tx_times[obj.GUID()]
        del obj


class OpcService(win32serviceutil.ServiceFramework):
    _svc_name_ = "zzzOpenOPCService"
    _svc_display_name_ = "OpenOPC Gateway Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.print_config()

    def SvcStop(self):
        servicemanager.LogInfoMsg('\nOpenOpcService Stopping service')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg(f'\nOpenOpcService Starting service on port {OPC_GATE_PORT}')

        daemon = Pyro4.core.Daemon(host=OPC_GATE_HOST, port=OPC_GATE_PORT)
        daemon.register(opc(), "opc")

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
        
        OPC_GATE_HOST:  {OPC_GATE_HOST}
        OPC_GATE_PORT:  {OPC_GATE_PORT}
        OPC_CLASS:      {OPC_CLASS}
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
            daemon = Pyro4.core.Daemon(host=OPC_GATE_HOST, port=OPC_GATE_PORT)
            daemon.register(opc(), 'opc')

            socks = set(daemon.sockets)
            while True:
                ins, outs, exs = select.select(socks, [], [], 1)
                if ins:
                    daemon.events(ins)

            daemon.shutdown()
        else:
            win32serviceutil.HandleCommandLine(OpcService)
