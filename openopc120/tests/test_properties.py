from unittest import TestCase

import pywintypes

from opc_server_config import connect_opc_client

pywintypes.datetime = pywintypes.TimeType


class TestProperties(TestCase):
    def setUp(self) -> None:
        self.opc_client = connect_opc_client()
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_read_property(self):
        properties = self.opc_client.properties(self.no_system_tags[1])
        self.assertEqual(properties[0], (0, 'Item ID (virtual property)', 'Bucket Brigade.ArrayOfReal8'))
        self.assertEqual(properties[1][0], 1)
        self.assertEqual(properties[1][1], 'Item Canonical DataType')
        self.assertEqual(properties[2], (2, 'Item Value', ()))
        self.assertEqual(properties[3], (3, 'Item Quality', 'Good'))
        self.assertEqual(properties[4][1], 'Item Timestamp')
        self.assertEqual(properties[5], (5, 'Item Access Rights', 'Read/Write'))
        self.assertEqual(properties[6], (6, 'Server Scan Rate', 100.0))
        self.assertEqual(properties[7], (7, 'Item EU Type', 0))
        self.assertEqual(properties[8], (8, 'Item EUInfo', None))
        self.assertEqual(properties[9], (101, 'Item Description', 'Bucket brigade item.'))

    def test_read_property_id(self):
        tag = self.no_system_tags[5]
        properties = self.opc_client.properties(tag, id=[1, 3])
        self.assertEqual((1, 'Item Canonical DataType', 'VT_I2'), properties[0],)
        self.assertEqual((3, 'Item Quality', 'Good'), properties[1],)

    def test_read_properties(self):
        properties = self.opc_client.properties(self.no_system_tags[1:24])
        print_properties(properties)

    def test_read_properties_id(self):
        properties = self.opc_client.properties(self.no_system_tags, id=[1])
        print_properties(properties)


def print_properties(properties):
    for prop in properties:
        print(f"{prop}")
