from unittest import TestCase

from src.OpenOPC import client

OPC_SERVER = "Matrikon.OPC.Simulation.1"
import pywintypes

pywintypes.datetime = pywintypes.TimeType


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
