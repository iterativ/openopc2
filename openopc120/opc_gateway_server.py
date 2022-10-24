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
import os

import Pyro4.core

from openopc120.opc_da_client import OpcDaClient, __version__

OPC_GATE_HOST = os.environ.get('OPC_GATE_HOST', 'localhost')
OPC_GATE_PORT = os.environ.get('OPC_GATE_PORT', 7766)
OPC_CLASS = os.environ.get('OPC_CLASS', "OPC.Automation")

@Pyro4.expose  # needed for version 4.55+
class OpenOpcGatewayServer:
    def __init__(self, host: str = 'localhost', port=OPC_GATE_PORT):
        self.host = str(host)
        self.port = int(port)

        self.remote_hosts = {}
        self.init_times = {}
        self.tx_times = {}
        self.pyro_daemon = None
        self.uri = None
        print(f'Initialized OpenOPC gateway Server uri: {self.uri}')

    def register_self(self):
        return

    def get_clients(self):
        """Return list of server instances as a list of (GUID,host,time) tuples"""
        registered_pyro_objects = Pyro4.core.DaemonObject(self.pyro_daemon).registered()  # needed for version 4.55
        registered_opd_da_clients = [proxy_name for proxy_name in registered_pyro_objects if"OpcDaClient" in proxy_name]
        reg = [f"PYRO:{obj}@{OPC_GATE_HOST}:{OPC_GATE_PORT}" for obj in registered_opd_da_clients]
        hosts = self.remote_hosts
        init_times = self.init_times
        tx_times = self.tx_times
        hlist = [(hosts[k] if k in hosts else '', init_times[k], tx_times[k]) for k in reg]
        return hlist

    def create_client(self, opc_class: str = OPC_CLASS):
        """Create a new OpenOPC instance in the Pyro server"""
        print(f"-"*80)

        opc_da_client = OpcDaClient(opc_class)
        #uri = self.pyro_daemon.register(opc_da_client)

        client_id = opc_da_client.client_id
        # TODO: This seems like a circular object tree...
        opc_da_client._open_serv = self
        opc_da_client._open_host = self.host
        opc_da_client._open_port = self.port
        opc_da_client._open_guid = client_id

        self.remote_hosts[client_id] = str(client_id)
        self.init_times[client_id] = time.time()
        self.tx_times[client_id] = time.time()
        self.pyro_daemon.register(opc_da_client, f"OpcDaClient-{client_id}")
        return opc_da_client

    def release_client(self, obj):
        """Release an OpenOPC instance in the Pyro server"""

        self.pyro_daemon.unregister(obj)
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


def main(host, port):
    server = OpenOpcGatewayServer()


    pyro_daemon = Pyro4.core.Daemon(host=host,
                                    port=int(port))

    server.pyro_daemon = pyro_daemon

    pyro_daemon.register(server, objectId="OpenOpcGatewayServer")


    print(f"server started {pyro_daemon}")
    pyro_daemon.requestLoop()


if __name__ == '__main__':
    main(OPC_GATE_HOST, OPC_GATE_PORT)
