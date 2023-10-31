from unittest import TestCase

from typer.testing import CliRunner

from openopc2.cli import app
from test_config import test_config

config = test_config()
OPTIONS = ["--protocol-mode", config.OPC_MODE,
           "--opc-server", config.OPC_SERVER,
           "--gateway-host", config.OPC_GATEWAY_HOST,
           "--gateway-port", config.OPC_GATEWAY_PORT]


class TestOpcCli(TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "--install-completion" in result.stdout

    def test_list(self):
        result = self.runner.invoke(app, ["list-tags"] + OPTIONS)
        assert result.exit_code == 0

    def test_list_recursive(self):
        result = self.runner.invoke(app, ["list-tags", "--recursive"] + OPTIONS)
        assert result.exit_code == 0

    def test_read_tag(self):
        result = self.runner.invoke(app, ["read", 'Bucket Brigade.Int1'] + OPTIONS)
        assert result.exit_code == 0

    def test_read_tags(self):
        result = self.runner.invoke(app, ["read", 'Bucket Brigade.Int1', 'Bucket Brigade.Int2'] + OPTIONS)
        assert result.exit_code == 0

    def test_server_info(self):
        result = self.runner.invoke(app, ["server-info"] + OPTIONS)
        assert result.exit_code == 0

    def test_list_servers(self):
        result = self.runner.invoke(app, ["list-servers"] + OPTIONS)
        assert result.exit_code == 0

    def test_list_config(self):
        result = self.runner.invoke(app, ["list-config"])
        print(result)
        assert result.exit_code == 0

    def test_properties(self):
        result = self.runner.invoke(app, ["properties", 'Bucket Brigade.Int1'] + OPTIONS)
        assert result.exit_code == 0

    def test_write_tags(self):
        result = self.runner.invoke(app, ["write", "Bucket Brigade.Int1=3"] + OPTIONS)
        assert result.exit_code == 0
