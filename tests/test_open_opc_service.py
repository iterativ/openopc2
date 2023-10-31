from unittest import TestCase, skipIf

from openopc2.gateway_proxy import OpenOpcGatewayProxy
from test_config import test_config


@skipIf(test_config().OPC_MODE != 'gateway', "Skip test if OPC_Mode is not gateway")
class TestOpenOPCService(TestCase):
    def test_get_clients(self):
        open_opc_gateway_proxy = OpenOpcGatewayProxy(test_config().OPC_HOST).get_server_proxy()
        opc_da_client = open_opc_gateway_proxy.create_client(test_config().OPC_CLASS)

    def test_print_clients(self):
        open_opc_gateway_proxy = OpenOpcGatewayProxy(test_config().OPC_HOST).get_server_proxy()
        opc_da_client = open_opc_gateway_proxy.print_clients()
