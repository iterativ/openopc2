from unittest import TestCase
from openopc2.gateway_server import OpenOpcGatewayServer
from .opc_server_config import OPC_SERVER


new_client = "OPC.Automation"


class TestOpcGatewayServer(TestCase):
    def test_init(self):
        server = OpenOpcGatewayServer()

    def test_create_client(self):
        server = OpenOpcGatewayServer()
        opc_client = server.create_client(new_client)
        opc_client.connect(OPC_SERVER)
        tags = opc_client.list()
        self.assertEqual(['Simulation Items', 'Configured Aliases'], tags)

    def test_get_clients(self):
        server = OpenOpcGatewayServer()
        opc_client = server.create_client(new_client)
        clients = server.get_clients()

    def test_print_clients(self):
        server = OpenOpcGatewayServer()
        server.create_client(new_client)
        server.create_client(new_client)
        server.print_clients()
