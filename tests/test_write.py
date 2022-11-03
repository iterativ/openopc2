import numbers
from unittest import TestCase

from test_config import test_config
from utils import get_opc_da_client


class TestWriteTags(TestCase):
    def setUp(self) -> None:
        self.opc_client = get_opc_da_client(test_config())
        self.tags = self.opc_client.list(recursive=False, include_type=False, flat=True)
        self.no_system_tags = [tag for tag in self.tags if "@" not in tag]
        self.writeable_tags = [tag for tag in self.tags if "Bucket Brigade" in tag]

    def test_write_all_tags_single_writes(self):
        """
        Not really a test but if it runs through  most datatypes work
        """
        for tag in self.writeable_tags:
            old_value = self.opc_client.read(tag)[0]
            if old_value is not None:
                new_value = create_new_value(old_value)
                write = self.opc_client.write(tag, new_value)
                written_value = self.opc_client.read(tag)[0]
                print_write_result(write, tag, old_value, written_value)
            else:
                print(old_value)

                # self.assertEqual(new_value, writen_value)
                # write = self.opc_client.write((tag, old_value))

    def test_write_all_tags_single_writes_include_error(self):
        """
        Not really a test but if it runs through  most datatypes work
        """
        for tag in self.writeable_tags:
            old_value = self.opc_client.read(tag)[0]
            new_value = create_new_value(old_value)
            write = self.opc_client.write((tag, new_value), include_error=True)
            written_value = self.opc_client.read(tag)[0]
            print_write_result(write, tag, old_value, written_value)
            # self.assertEqual(new_value, writen_value)
            # write = self.opc_client.write((tag, old_value))

    def test_write_tags_list(self):
        tag_values = list(zip([self.no_system_tags[4], self.no_system_tags[5]], [1, 10]))
        values = self.opc_client.write(tag_values)
        print(f"{values}")

    def test_write_tags_single(self):
        tag_values = (self.no_system_tags[4], 1)
        values = self.opc_client.write(tag_values)
        print(f"{values}")


def print_write_result(write_result, tag, old, new):
    if type(write_result) == list:
        write_result = write_result[0]
    success = write_result[0] == 'Success'
    if success:
        print(f"{write_result[0]}: {tag:20} old: {old} new: {new}")
    else:
        print(write_result)


def create_new_value(old_value):
    if isinstance(old_value, numbers.Number):
        return old_value + 1
    if isinstance(old_value, str):
        return "OPC Test"
    if isinstance(old_value, tuple):
        return range(len(old_value))
