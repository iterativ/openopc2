from unittest import TestCase

from openopc120.config import open_opc_config


class TestConfig(TestCase):

    def test_print_config(self):
        config = open_opc_config
        config.print_config()

    def test_overwrite_config_runtime(self):
        config = open_opc_config
        self.assertEqual(config.OPC_CLIENT, 'OpenOPC')
        config.OPC_CLIENT = 'Shubi'
        self.assertEqual(config.OPC_CLIENT, 'Shubi')

