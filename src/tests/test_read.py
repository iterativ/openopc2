from unittest import TestCase

from src.OpenOPC import client
from src.tests.test_properties import OPC_SERVER


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

    def test_read_tags_list_sync(self):
        values = self.opc_client.read(self.no_system_tags, sync=True)
        print(f"{values}")

    def test_read_tags_list_sync(self):
        values = self.opc_client.read(self.no_system_tags, include_error=True)
        print(f"{values}")

    def test_non_existent_tag(self):
        tag_name = "idont_exist"
        values = self.opc_client.read(tag_name, include_error=True)
        values = self.opc_client.read(tag_name, sync=True)
        values = self.opc_client.read(tag_name)
        print(f"{values}")

    def test_non_existent_tags(self):
        tag_names = ["idont_exist", "test"]
        values = self.opc_client.read(tag_names, include_error=True)
        values = self.opc_client.read(tag_names, sync=True)
        values = self.opc_client.read(tag_names)
        print(f"{values}")

    def test_group_read(self):
        square_wave_tags = [tag for tag in self.tags if "square" in tag]
        values = self.opc_client.read(square_wave_tags, group="square_group")
        values_group = self.opc_client.read(group='square_group')
        self.assertEqual(len(values_group), len(values))
        self.assertEqual(values_group, values)