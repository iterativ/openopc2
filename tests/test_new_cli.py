from unittest import TestCase
import test_config
from openopc2.cli import cli

from typer.testing import CliRunner

from openopc2.cli import app


class TestOpcCli(TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "--install-completion" in result.stdout

    def test_list(self):
        result = self.runner.invoke(app, ["list", "*"])
        assert result.exit_code == 0

    def test_list_recursive(self):
        result = self.runner.invoke(app, ["list", "*", "-f"])

    def test_read_tag(self):
        result = self.runner.invoke(app, ["read", 'Bucket Brigade.Int1'])
        assert result.exit_code == 0

    def test_read_tags(self):
        result = self.runner.invoke(app, ["read", 'Bucket Brigade.Int1',  'Bucket Brigade.Int2'])
        assert result.exit_code == 0

    def test_info(self):
        result = self.runner.invoke(app, ["info"])
        assert result.exit_code == 0

    def test_servers(self):
        result = self.runner.invoke(app, ["servers"])

    def test_properties(self):
        result = self.runner.invoke(app, ["properties", 'Bucket Brigade.Int1'])
        assert result.exit_code == 0

    def test_write_tags(self):
        result = self.runner.invoke(app, 'Bucket Brigade.Boolean', "True")
        assert result.exit_code == 0
