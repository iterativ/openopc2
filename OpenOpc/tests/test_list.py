from unittest import TestCase

from OpenOpc.OpenOPC import client
from OpenOpc.tests.opc_server_config import OPC_SERVER, OPC_HOST


class TestListTags(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER, opc_host=OPC_HOST)

    def test_list_flat_return_tags(self):
        tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        for p in tags:
            print(p)
        self.assertIs(type(tags), list)
        self.assertIs(type(tags[0]), str)
        self.assertTrue("Triangle Waves.UInt4" in tags)

    def test_list_type_return_tags_incude_type(self):
        tags = self.opc_client.list(recursive=False, include_type=True, flat=False)
        self.assertIs(type(tags), list)
        self.assertIs(type(tags[0]), tuple)
        self.assertTrue(('Simulation Items', 'Branch') in tags)

    def test_list_recursive_return_tags_recursive(self):
        tags = self.opc_client.list(recursive=True, include_type=False, flat=False)
        self.assertIs(type(tags), list)
        self.assertIs(type(tags[0]), str)
        self.assertTrue("Triangle Waves.UInt4" in tags)