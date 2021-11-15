from unittest import TestCase

import pywintypes

from OpenOpc.tests.opc_server_config import connect_opc_client

pywintypes.datetime = pywintypes.TimeType


class TestProperties(TestCase):
    def setUp(self) -> None:
        self.opc_client = connect_opc_client()
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_read_property(self):
        properties = self.opc_client.properties(self.no_system_tags[1])
        for prop in properties:
            print(f"{prop}")

    def test_read_property_id(self):
        properties = self.opc_client.properties(self.no_system_tags[1], id=[1])
        for prop in properties:
            print(f"{prop}")

    def test_read_properties(self):
        properties = self.opc_client.properties(self.no_system_tags[1:24])
        for prop in properties:
            print(f"{prop}")

    def test_read_properties_id(self):
        properties = self.opc_client.properties(self.no_system_tags, id=[1])
        for prop in properties:
            print(f"{prop}")
