from unittest import TestCase, skipIf

from openopc120.OpcCom import OpcCom
from opc_server_config import OPC_HOST, OPC_SERVER, USE_GATEWAY


class TestOpenOpcCom(TestCase):
    def test_init(self):
        opc_com = OpcCom(OPC_SERVER)
