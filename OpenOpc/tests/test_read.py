from unittest import TestCase

from OpenOpc.OpenOPC import client
from OpenOpc.tests.opc_server_config import OPC_SERVER


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

    def test_read_tag_include_error(self):
        values = self.opc_client.read(self.no_system_tags[0], include_error=True)
        print(f"{values}")

    def test_read_tag_sync(self):
        values = self.opc_client.read(self.no_system_tags[0], sync=True)
        print(f"{values}")

    def test_read_tags_list_include_error(self):
        values = self.opc_client.read(self.no_system_tags, include_error=True)
        print(f"{values}")

    def test_non_existent_tag(self):
        tag_name = "idont_exist"
        values = self.opc_client.read(tag_name)

        # values = self.opc_client.read(tag_name, include_error=True)
        # values = self.opc_client.read(tag_name, sync=True)
        print(f"{values}")

    def test_non_existent_tags(self):
        tag_names = ["idont_exist", "test"]
        values = self.opc_client.read(tag_names)

        # values = self.opc_client.read(tag_names, include_error=True)
        # values = self.opc_client.read(tag_names, sync=True)
        print(f"{values}")

    def test_group_read(self):
        square_wave_tags = [tag for tag in self.tags if "square" in tag]
        values = self.opc_client.read(square_wave_tags, group="square_group")
        values_group = self.opc_client.read(group='square_group')
        self.assertEqual(len(values_group), len(values))
        self.assertEqual(values_group, values)

    def test_read_system_tags(self):
        system_tags = [
            '@MemFree', '@MemUsed', '@MemTotal', '@MemPercent', '@MemPercent', '@DiskFree', '@SineWave', '@SawWave',
            '@CpuUsage'
        ]
        system_values = self.opc_client.read(system_tags)
        for value in system_values:
            print(value)

    def test_sytem_tag_task_info(self):
        task_name = "python"
        task_info_tags = [f"@TaskMem({task_name})", f"@TaskCpu({task_name})", f"@TaskExists({task_name})"]

        system_values = self.opc_client.read(task_info_tags)
        for value in system_values:
            print(value)
        self.assertTrue(system_values[0][1] > 1000)

