# -*- coding: utf-8 -*-
#
# Iterativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2015 Iterativ GmbH. All rights reserved.
#
# Created on 2022-10-24
# @author: lorenz.padberg@iterativ.ch
import time

import Pyro4.core

from openopc120.opc_da_client import OpcDaClient, __version__
from openopc120.opc_service import OPC_GATE_PORT, OPC_GATE_HOST, OPC_CLASS


@Pyro4.expose  # needed for version 4.55+
class OpenOpcGatewayServer:
    def __init__(self, host: str = 'localhost', port=OPC_GATE_PORT):
        self.host = host
        self.port = port

        self.remote_hosts = {}
        self.init_times = {}
        self.tx_times = {}
        self.pyro_deamon: Pyro4.core.Daemon = Pyro4.core.Daemon(host=self.host, port=self.port)
        self.register_self()

    def register_self(self):
        self.pyro_deamon.register(OpenOpcGatewayServer(), "OpenOpcGatewayServer")

    def get_clients(self):
        """Return list of server instances as a list of (GUID,host,time) tuples"""
        reg1 = Pyro4.core.DaemonObject(self.pyro_deamon).registered()  # needed for version 4.55
        reg2 = [si for si in reg1 if si.find('obj_') == 0]
        reg = [f"PYRO:{obj}@{OPC_GATE_HOST}:{OPC_GATE_PORT}" for obj in reg2]
        hosts = self.remote_hosts
        init_times = self.init_times
        tx_times = self.tx_times
        hlist = [(hosts[k] if k in hosts else '', init_times[k], tx_times[k]) for k in reg]
        return hlist

    def create_client(self, opc_class: str = OPC_CLASS):
        """Create a new OpenOPC instance in the Pyro server"""

        opc_da_client = OpcDaClient(opc_class)
        uri = self.pyro_deamon.register(opc_da_client)

        uuid = uri.asString()
        # TODO: This seems like a circular object tree...
        opc_da_client._open_serv = self
        opc_da_client._open_self = opc_da_client
        opc_da_client._open_host = self.host
        opc_da_client._open_port = self.port
        opc_da_client._open_guid = uuid

        remote_ip = uuid  # self.getLocalStorage().caller.addr[0]
        #        try:
        #            remote_name = socket.gethostbyaddr(remote_ip)[0]
        #            self.remote_hosts[uuid] = '%s (%s)' % (remote_ip, remote_name)
        #        except socket.herror:
        #            self.remote_hosts[uuid] = '%s' % (remote_ip)
        self.remote_hosts[uuid] = str(remote_ip)
        self.init_times[uuid] = time.time()
        self.tx_times[uuid] = time.time()
        return Pyro4.Proxy(uri)

    def release_client(self, obj):
        """Release an OpenOPC instance in the Pyro server"""

        self.pyro_deamon.unregister(obj)
        del self.remote_hosts[obj.GUID()]
        del self.init_times[obj.GUID()]
        del self.tx_times[obj.GUID()]
        del obj

    def print_config(self):
        welcome_message = f"""
        Open Opc Gateway server
        Version:    {__version__}

        OPC_GATE_HOST:  {self.host}
        OPC_GATE_PORT:  {self.port}
        OPC_CLASS:      {self.opc_class}
        """
        print(welcome_message)
