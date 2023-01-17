import os
from unittest import TestCase

from openopc2.config import OpenOpcConfig


def test_config():
    open_opc_config = OpenOpcConfig()
    open_opc_config.OPC_SERVER = "Matrikon.OPC.Simulation"
    open_opc_config.OPC_GATEWAY_HOST = "192.168.0.115"
    open_opc_config.OPC_CLASS = "Graybox.OPC.DAWrapper"
    open_opc_config.OPC_MODE = "gateway"
    return open_opc_config


class TestOpenOpcConfig(TestCase):
    def test_instantiation(self) -> None:
        # Confirm env vars won't mess up assertions
        for env_var in ["OPC_SERVER", "OPC_GATE_PORT", "OPC_TIMEOUT"]:
            self.assertNotIn(env_var, os.environ)

        default_config = OpenOpcConfig()
        self.assertEquals(default_config.OPC_SERVER, "Matrikon.OPC.Simulation")
        self.assertIsInstance(default_config.OPC_GATEWAY_PORT, int)
        self.assertEquals(default_config.OPC_GATEWAY_PORT, 7766)
        self.assertIsInstance(default_config.OPC_TIMEOUT, int)
        self.assertEquals(default_config.OPC_TIMEOUT, 1000)

        nondefault_config = OpenOpcConfig(opc_server="Another.Server")
        self.assertEquals(nondefault_config.OPC_SERVER, "Another.Server")
