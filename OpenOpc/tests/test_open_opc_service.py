from unittest import TestCase

from OpenOpc.OpenOPC import open_client
from opc_server_config import OPC_HOST, OPC_SERVER


class TestOpenOPCService(TestCase):

    def test_get_clients(self):
        client = open_client(OPC_HOST)
        client.connect(OPC_SERVER, OPC_HOST)
        tags = client.list(flat=True)
        for l in tags:
            print(l)
