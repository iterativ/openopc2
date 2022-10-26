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

import Pyro5.server

from openopc.config import open_opc_config
from openopc.opc_da_client import OpcDaClient, __version__


@Pyro5.api.expose
class OpenOpcGatewayServer:
    def __init__(self, host: str = open_opc_config.OPC_GATEWAY_HOST, port=open_opc_config.OPC_GATEWAY_PORT):
        self.host = str(host)
        self.port = int(port)

        self.clients_by_uuid = {}

        self.remote_hosts = {}
        self.init_times = {}
        self.tx_times = {}
        self.pyro_daemon = None
        self.uri = None
        print(f'Initialized OpenOPC gateway Server uri: {self.uri}')

    def print_clients(self):
        for client in self.get_clients():
            print(client)
        print(self.pyro_daemon)

    def get_clients(self):
        """Return list of server instances as a list of (GUID,host,time) tuples"""
        out_list = []
        for client_id, client in self.clients_by_uuid.items():
            out_list.append({
                'client_id': client.client_id,
                'tx_time': self.tx_times.get(client.client_id),
                'init_time': self.init_times.get(client.client_id)
            })
        return out_list

    def create_client(self, opc_class: str = open_opc_config.OPC_CLASS):
        """Create a new OpenOPC instance in the Pyro server"""
        print(f"-" * 80)

        opc_da_client = OpcDaClient(opc_class)

        client_id = opc_da_client.client_id
        # TODO: This seems like a circular object tree...
        opc_da_client._open_serv = None
        opc_da_client._open_host = self.host
        opc_da_client._open_port = self.port
        opc_da_client._open_guid = client_id

        self.remote_hosts[client_id] = str(client_id)
        self.init_times[client_id] = time.time()
        self.tx_times[client_id] = time.time()
        self.clients_by_uuid[client_id] = opc_da_client
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

        open_opc_config.print_config()


def main(host, port):
    server = OpenOpcGatewayServer()
    pyro_daemon = Pyro5.server.Daemon(host=host, port=int(port))
    pyro_daemon.register(server, objectId="OpenOpcGatewayServer")
    pyro_daemon.register(OpcDaClient, objectId="OpcDaClient")
    print(f"server started {pyro_daemon}")
    return pyro_daemon


if __name__ == '__main__':
    pyro_daemon = main(open_opc_config.OPC_GATEWAY_HOST, open_opc_config.OPC_GATEWAY_PORT)
    pyro_daemon.requestLoop()
