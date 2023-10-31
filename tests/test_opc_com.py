import time
from unittest import TestCase, skipIf

from openopc2.da_com import OpcCom
from test_config import test_config

TAG = 'Bucket Brigade.Int1'


@skipIf(test_config().OPC_MODE != 'com', "COM interface tests ony if OPC_MODE is com is disabled")
class TestOpenOpcCom(TestCase):
    def setUp(self):
        self.opccom = OpcCom(test_config().OPC_CLASS)
        self.opccom.connect(test_config().OPC_HOST, test_config().OPC_SERVER)

    def test_init(self):
        opc_com = OpcCom(test_config().OPC_CLASS)

    def test_connect(self):
        opc_com = OpcCom(test_config().OPC_CLASS)
        opc_com.connect(test_config().OPC_HOST, test_config().OPC_SERVER)

    def test_create_browser(self):
        browser = self.opccom.create_browser()

    def test_disconnect(self):
        self.opccom.disconnect()

    def test_server_name(self):
        server_name = self.opccom.server_name

    def test_get_opc_servers(self):
        opc_servers = self.opccom.get_opc_servers(test_config().OPC_HOST)
        for server in opc_servers:
            self.assertTrue(test_config().OPC_SERVER in server)

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
