import numbers
from unittest import TestCase

import structlog

from openopc2.utils import get_opc_da_client
from test_config import test_config

logger = structlog.getLogger('__name__')


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
            try:
                float(old_value)
                is_numeric = True
            except Exception as e:
                is_numeric = False

            if is_numeric:
                new_value = create_new_value(old_value)
                write = self.opc_client.write((tag, new_value))
                written_value = self.opc_client.read(tag)[0]
                self.assertEqual(new_value, written_value)

    def test_write_single_tag(self):
        """
        """
        tag = self.writeable_tags[0]
        old_value = self.opc_client.read(tag)[0]
        try:
            float(old_value)
            is_numeric = True
        except Exception as e:
            is_numeric = False

        if is_numeric:
            new_value = create_new_value(old_value)
            write = self.opc_client.write((tag, new_value))
            written_value = self.opc_client.read(tag)[0]
            self.assertEqual(new_value, written_value)

    def test_write_all_tags_single_writes_include_error(self):
        """
          Not really a test but if it runs through  most datatypes work
          """
        for tag in self.writeable_tags:
            old_value = self.opc_client.read(tag)[0]
            try:
                float(old_value)
                is_numeric = True
            except Exception:
                is_numeric = False

            if is_numeric:
                new_value = create_new_value(old_value)
                write = self.opc_client.write((tag, new_value), include_error=True)
                written_value = self.opc_client.read(tag)[0]
                self.assertEqual(new_value, written_value)





def create_new_value(old_value):
    if isinstance(old_value, bool):
        return not old_value
    if isinstance(old_value, numbers.Number):
        return old_value + 1
    if isinstance(old_value, str):
        return "OPC Test"
    if isinstance(old_value, tuple):
        return range(len(old_value))
