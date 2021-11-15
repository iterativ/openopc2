from unittest import TestCase

from OpenOpc.OpenOPCService import opc, OpcService
from OpenOpc.tests.opc_server_config import OPC_SERVER


class TestOpenOPCService(TestCase):
    def setUp(self) -> None:
        self.opc_client = opc()

    def test_get_clients(self):
        self.opc_client.create_client()

        self.opc_client.get_clients()

