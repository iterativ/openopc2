from unittest import TestCase

from test_config import test_config
from openopc2.utils import get_opc_da_client

READ_TIMEOUT = 500
N = 150


class TestReadTags(TestCase):
    def setUp(self) -> None:
        self.opc_client = get_opc_da_client(test_config())
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_read_all_tags_single_reads(self):
        """
        Not really a test but if it runs through it most datatypes work
        """
        values = [self.opc_client.read(tag, timeout=READ_TIMEOUT) for tag in self.tags]
        print_values(values)

    def test_read_tags_list(self):
        values = self.opc_client.read(self.no_system_tags)
        print_values(values)

    def test_read_specific_tags(self):
        specific_tags_results = [('Bucket Brigade.Boolean', 3, 'Good', '2021-12-02 16:35:53.162000+00:00'),
                                 ('Bucket Brigade.Int1', 1, 'Good', '2021-12-02 16:37:41.377000+00:00'),
                                 ('Bucket Brigade.Int2', 10, 'Good', '2021-12-02 16:37:41.377000+00:00'),
                                 ('Bucket Brigade.Int4', 2, 'Good', '2021-12-02 16:35:53.767000+00:00'),
                                 ('Bucket Brigade.Money', 2, 'Good', '2021-12-02 16:35:53.972000+00:00'),
                                 ('Bucket Brigade.Real4', 2.0, 'Good', '2021-12-02 16:35:54.177000+00:00'),
                                 ('Bucket Brigade.Real8', 2.0, 'Good', '2021-12-02 16:35:54.372000+00:00'),
                                 ('Bucket Brigade.String', 'OPC Test', 'Good', '2021-12-02 16:35:54.572000+00:00'),
                                 ('Bucket Brigade.Time', 'OPC Test', 'Good', '2021-12-02 16:35:54.772000+00:00'),
                                 ('Bucket Brigade.UInt1', 2, 'Good', '2021-12-02 16:35:54.972000+00:00'),
                                 ('Bucket Brigade.UInt2', 2, 'Good', '2021-12-02 16:35:55.182000+00:00'),
                                 ('Bucket Brigade.UInt4', 2.0, 'Good', '2021-12-02 16:35:55.377000+00:00')
                                 ]
        specific_tag_names = [tag_result[0] for tag_result in specific_tags_results]
        values = self.opc_client.read(specific_tag_names)
        tag_names = [tag_result[0] for tag_result in specific_tags_results]
        self.assertEqual(specific_tag_names, tag_names)
        qualities = [tag_result[2] for tag_result in specific_tags_results]
        self.assertEqual(qualities, ['Good'] * len(values))

    def test_read_tags_list_sync(self):
        values = self.opc_client.read(self.no_system_tags[0:N], sync=True, timeout=READ_TIMEOUT)
        print_values(values)

    def test_read_tag_include_error(self):
        values = self.opc_client.read(self.no_system_tags[0:N], include_error=True, timeout=READ_TIMEOUT)
        print_values(values)

    def test_read_tag_sync(self):
        values = self.opc_client.read(self.no_system_tags[0:N], sync=True, timeout=READ_TIMEOUT)
        print_values(values)

    def test_read_tags_list_include_error(self):
        values = self.opc_client.read(self.no_system_tags[0:N], include_error=True, timeout=READ_TIMEOUT)
        print_values(values)

    def test_non_existent_tag_error(self):
        value = self.opc_client.read("idont_exist", include_error=True)
        self.assertEqual(value, (None, 'Error', None, "The item ID does not conform to the server's syntax. "))

    def test_non_existent_tag(self):
        value = self.opc_client.read("idont_exist")
        self.assertEqual(value, (None, 'Error', None))

    def test_non_existent_tag_sync(self):
        value = self.opc_client.read("idont_exist", sync=True)
        self.assertEqual(value, (None, 'Error', None))

    def test_non_existent_tags(self):
        values = self.opc_client.read(["idont_exist", "test", 'Bucket Brigade.Int1'], timeout=READ_TIMEOUT)
        self.assertEqual(values[0], ("idont_exist", None, 'Error', None))
        self.assertEqual(values[1], ("test", None, 'Error', None))
        self.assertEqual(values[2][0], "Bucket Brigade.Int1")
        self.assertEqual(values[2][2], 'Good')

    def test_non_existent_tags_error(self):
        values = self.opc_client.read(["idont_exist", "test", 'Bucket Brigade.Int1'], timeout=READ_TIMEOUT,
                                      include_error=True)
        self.assertEqual(values[0],
                         ("idont_exist", None, 'Error', None, "The item ID does not conform to the server's syntax. "))
        self.assertEqual(values[1],
                         ("test", None, 'Error', None, "The item ID does not conform to the server's syntax. "))

        self.assertEqual(values[2][0], "Bucket Brigade.Int1")
        self.assertEqual(values[2][2], 'Good')

    def test_non_existent_tags_sync(self):
        values = self.opc_client.read(["idont_exist", "test", 'Bucket Brigade.Int1'], timeout=READ_TIMEOUT, sync=True)
        self.assertEqual(values[0], ("idont_exist", None, 'Error', None))
        self.assertEqual(values[1], ("test", None, 'Error', None))
        self.assertEqual(values[2][0], "Bucket Brigade.Int1")
        self.assertEqual(values[2][2], 'Good')

    # def test_group_read(self):
    #     square_wave_tags = [tag for tag in self.tags if "Square" in tag]
    #     values = self.opc_client.read(square_wave_tags, group="square_group", timeout=READ_TIMEOUT)
    #     values_group = self.opc_client.read(square_wave_tags, group='square_group')
    #     self.assertEqual(len(values_group), len(values))
    #     self.assertEqual(values_group, values)

    def test_read_system_tags(self):
        system_tags = [
            '@MemFree', '@MemUsed', '@MemTotal', '@MemPercent', '@MemPercent', '@DiskFree', '@SineWave', '@SawWave',
            '@CpuUsage'
        ]
        system_values = self.opc_client.read(system_tags)
        print_values(system_values)

    def test_sytem_tag_task_info(self):
        task_name = "OpenOpcService"
        task_info_tags = [f"@TaskMem({task_name})", f"@TaskCpu({task_name})", f"@TaskExists({task_name})"]

        system_values = self.opc_client.read(task_info_tags)
        print_values(system_values)
        self.assertTrue(system_values[0][1] > 1000)


def print_values(values):
    for k, value in enumerate(values):
        print(k, value)
