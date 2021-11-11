from unittest import TestCase

from src.OpenOPC import client

OPC_SERVER = "Matrikon.OPC.Simulation.1"
import pywintypes

pywintypes.datetime = pywintypes.TimeType


class TestServerInfo(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER)

    def test_get_server(self):
        available_servers = self.opc_client.servers()
        print(available_servers)
        self.assertIsNotNone(available_servers)


class TestListTags(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER)

    def test_list_flat_return_tags(self):
        tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        for p in tags:
            print(p)
        self.assertIs(type(tags), list)
        self.assertIs(type(tags[0]), str)
        self.assertTrue("Triangle Waves.UInt4" in tags)

    def test_list_type_return_tags(self):
        tags = self.opc_client.list(recursive=False, include_type=True, flat=False)
        self.assertIs(type(tags), list)
        self.assertIs(type(tags[0]), tuple)
        self.assertTrue(('Simulation Items', 'Branch') in tags)

    def test_list_recursive_return_tags(self):
        tags = self.opc_client.list(recursive=True, include_type=False, flat=False)
        self.assertIs(type(tags), list)
        self.assertIs(type(tags[0]), str)
        self.assertTrue("Triangle Waves.UInt4" in tags)


class TestReadTags(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER)
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_read_all_tags_single_reads(self):
        """
        Not really a test but if it runs through it most datatypes work
        """
        for tag in self.tags:
            value = self.opc_client.read(tag)
            print(f"{tag} {value}")

    def test_read_tags_list(self):
        values = self.opc_client.read(self.no_system_tags)
        print(f"{values}")

    def test_group_read(self):
        square_wave_tags = [tag for tag in self.tags if "square" in tag]
        values = self.opc_client.read(square_wave_tags, group="square_group")
        values_group = self.opc_client.read(group='square_group')
        self.assertEqual(len(values_group), len(values))
        self.assertEqual(values_group, values)


class TestProperties(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER)
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_read_property(self):
        properties = self.opc_client.properties(self.no_system_tags[1])
        for prop in properties:
            print(f"{prop}")

    def test_read_properties(self):
        properties = self.opc_client.properties(self.no_system_tags)
        for prop in properties:
            print(f"{prop}")
