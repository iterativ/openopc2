from unittest import TestCase

from opc_server_config import OPC_SERVER, OPC_HOST
from openopc2.open_opc_cli import OpcCli


class TestOpcCli(TestCase):
    def setUp(self) -> None:
        self.opc_cli = OpcCli()
        self.opc_cli.opc_host = OPC_HOST
        self.opc_cli.opc_server = OPC_SERVER
        self.opc_cli.cli_connect()

    def test_help(self):
        self.opc_cli.usage()

    def test_list(self):
        result = self.opc_cli.cli_list('*')

    def test_list_recursive(self):
        self.opc_cli.recursive = True
        self.opc_cli.cli_list('*')

    def test_read_tag(self):
        self.opc_cli.cli_read('Bucket Brigade.Int1')

    def test_read_tags(self):
        self.opc_cli.cli_read(['Bucket Brigade.Int1', 'Bucket Brigade.Int2'])

    def test_info(self):
        self.opc_cli.cli_info()

    def test_servers(self):
        self.opc_cli.cli_servers()

    def test_properties(self):
        self.opc_cli.cli_properties('Bucket Brigade.Boolean')

    def test_write_tags(self):
        self.opc_cli.cli_write([('Bucket Brigade.Boolean', True)])
