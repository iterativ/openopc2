from unittest import TestCase
from openopc2.gateway_server import OpenOpcGatewayServer
from test_config import test_config


class TestOpcGatewayServer(TestCase):
    def test_init(self):
        server = OpenOpcGatewayServer(test_config().OPC_GATEWAY_HOST, test_config().OPC_GATEWAY_PORT)

    def test_create_client(self):
        server = OpenOpcGatewayServer(test_config().OPC_GATEWAY_HOST, test_config().OPC_GATEWAY_PORT)
        opc_client = server.create_client(test_config())
        opc_client.connect(test_config().OPC_SERVER)
        tags = opc_client.list()
        self.assertEqual(['Simulation Items', 'Configured Aliases'], tags)

    def test_get_clients(self):
        server = OpenOpcGatewayServer(test_config().OPC_GATEWAY_HOST, test_config().OPC_GATEWAY_PORT)
        opc_client = server.create_client(test_config())
        clients = server.get_clients()

    def test_print_clients(self):
        server = OpenOpcGatewayServer(test_config().OPC_GATEWAY_HOST, test_config().OPC_GATEWAY_PORT)
        server.create_client(test_config())
        server.create_client(test_config())
        server.print_clients()
