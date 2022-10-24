from unittest import TestCase, skipIf

from opc_gateway_proxy import OpenOpcGatewayProxy
from opc_server_config import OPC_HOST, OPC_SERVER, USE_GATEWAY


@skipIf(not USE_GATEWAY, "USE_GATEWAY is disabled")
class TestOpenOPCService(TestCase):
    def test_get_clients(self):
        open_opc_gateway_proxy = OpenOpcGatewayProxy(OPC_HOST)
        opc_da_client = open_opc_gateway_proxy.open_client()
        opc_da_client.connect(OPC_SERVER, OPC_HOST)
        tags = opc_da_client.list(flat=True)
        for l in tags:
            print(l)
