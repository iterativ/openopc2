from unittest import TestCase

from src.OpenOPC import client
from src.tests.opc_server_config import OPC_SERVER
import numbers


class TestWriteTags(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER)
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]

    def test_write_all_tags_single_writes(self):
        """
        Not really a test but if it runs through it most datatypes work
        """
        for tag in self.tags:
            old_value = self.opc_client.read(tag)[0]
            if old_value:
                if isinstance(old_value, numbers.Number):
                    new_value = old_value + 1
                if isinstance(old_value, str):
                    new_value = "OPC Test"
                if isinstance(old_value, tuple):
                    new_value = range(len(old_value))
                write = self.opc_client.write((tag, new_value))
                written_value = self.opc_client.read(tag)[0]
                if new_value == written_value:
                    print(f"Write Success: {tag:20} old: {old_value} new: {written_value} ")
                else:
                    print(f"Write Failed : {tag:20} old: {old_value} new: {written_value} ")

                # self.assertEqual(new_value, writen_value)
                # write = self.opc_client.write((tag, old_value))

    def test_write_all_tags_single_writes_include_error(self):
        """
        Not really a test but if it runs through it most datatypes work
        """
        for tag in self.tags:
            old_value = self.opc_client.read(tag)[0]
            if old_value:
                if isinstance(old_value, numbers.Number):
                    new_value = old_value + 1
                if isinstance(old_value, str):
                    new_value = "OPC Test"
                if isinstance(old_value, tuple):
                    new_value = range(len(old_value))
                write = self.opc_client.write((tag, new_value), include_error=True)
                print(write)
                written_value = self.opc_client.read(tag)[0]
                if new_value == written_value:
                    print(f"Write Success: {tag:20} old: {old_value} new: {written_value} ")
                else:
                    print(f"Write Failed : {tag:20} old: {old_value} new: {written_value} ")

                # self.assertEqual(new_value, writen_value)
                # write = self.opc_client.write((tag, old_value))

    def test_write_tags_list(self):
        values = self.opc_client.write(list(zip([self.no_system_tags[4], self.no_system_tags[5]],  [1, 10])))
        print(f"{values}")
