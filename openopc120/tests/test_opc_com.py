import time
from unittest import TestCase, skipIf

from openopc120.Opc_Da import OpcCom, TagPropertyId
from opc_server_config import OPC_HOST, OPC_SERVER, USE_GATEWAY, OPC_CLASS

TAG = 'Bucket Brigade.Int1'


@skipIf(USE_GATEWAY, "COM interface tests ony if USE Gateway is disabled")
class TestOpenOpcCom(TestCase):
    def setUp(self):
        self.opccom = OpcCom(OPC_CLASS)
        self.opccom.connect(OPC_HOST, OPC_SERVER)

    def test_init(self):
        opc_com = OpcCom(OPC_CLASS)

    def test_connect(self):
        opc_com = OpcCom(OPC_CLASS)
        opc_com.connect(OPC_HOST, OPC_SERVER)

    def test_create_browser(self):
        browser = self.opccom.create_browser()

    def test_disconnect(self):
        self.opccom.disconnect()

    def test_server_name(self):
        server_name = self.opccom.server_name

    def test_get_opc_servers(self):
        opc_servers = self.opccom.get_opc_servers(OPC_HOST)
        self.assertTrue(OPC_SERVER in opc_servers)
        print(opc_servers)

    def test_get_available_properties(self):
        properties = self.opccom.get_available_properties(TAG)
        self.assertIsInstance(properties, tuple)
        print(properties)

    def test_get_tag_properties(self):

        start = time.time()
        for i in range(100):
            properties = self.opccom.get_tag_properties(TAG, [2, 3])

        print(f"selection {time.time() - start}")

    def test_get_all_tag_properties(self):
        start = time.time()
        for i in range(100):
            print(TAG)
            properties = self.opccom.get_tag_properties(TAG)
        print(f"all {time.time() - start}")


