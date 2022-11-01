from unittest import TestCase

from openopc2.config import OpenOpcConfig



class TestConfig(TestCase):

    def test_print_config(self):
        config = OpenOpcConfig()
        config.print_config()

    def test_overwrite_config_runtime(self):
        config = OpenOpcConfig()
        self.assertEqual(config.OPC_CLIENT, 'OpenOPC')
        config.OPC_CLIENT = 'Shubi'
        self.assertEqual(config.OPC_CLIENT, 'Shubi')
