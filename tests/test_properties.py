from unittest import TestCase

from openopc2.utils import get_opc_da_client
from test_config import test_config


class TestProperties(TestCase):
    def setUp(self) -> None:
        self.opc_client = get_opc_da_client(test_config())
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_read_property(self):
        properties = self.opc_client.properties('Bucket Brigade.Int1')
        prop = properties[0]
        self.assertEqual('VT_I1', prop.data_type)
        self.assertEqual('Good', prop.quality)
        self.assertEqual(prop.server_scan_rate, 100.0)

    def test_read_properties(self):
        properties = self.opc_client.properties(self.no_system_tags[1:24])
        print_properties(properties)

    def test_read_properties_id(self):
        properties = self.opc_client.properties(self.no_system_tags, id=[1])
        print_properties(properties)


def print_properties(properties):
    for prop in properties:
        print(f"{prop}")
