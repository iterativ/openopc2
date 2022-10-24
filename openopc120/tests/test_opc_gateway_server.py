import time
from unittest import TestCase, skipIf
from opc_server_config import OPC_HOST, OPC_CLASS, OPC_SERVER
from openopc120.opc_gateway_server import OpenOpcGatewayServer, OPC_CLASS


class TestOpcGatewayServer(TestCase):
    def test_init(self):
        server = OpenOpcGatewayServer()

    def test_create_client(self):
        server = OpenOpcGatewayServer()
        opc_client = server.create_client("OPC.Automation")
        opc_client.connect(OPC_SERVER)
        tags = opc_client.list()
        self.assertEqual(['Simulation Items', 'Configured Aliases'], tags)

    def test_get_clients(self):
        server = OpenOpcGatewayServer()
        opc_client = server.create_client("OPC.Automation")


        clients = server.get_clients()
        pass