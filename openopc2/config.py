import os
from typing import Literal


class OpenOpcConfig:
    def __init__(
        self,
        opc_host: str = "localhost",
        opc_server: str = os.environ.get("OPC_SERVER", "Matrikon.OPC.Simulation"),
        opc_client: str = "OpenOPC",
        opc_gateway_host: str = os.environ.get("OPC_GATE_HOST", "192.168.0.115"),
        opc_gateway_port: int = int(os.environ.get("OPC_GATE_PORT", 7766)),
        opc_class: str = os.environ.get("OPC_CLASS", "Graybox.OPC.DAWrapper"),
        opc_mode: Literal["GATEWAY", "COM"] = os.environ.get("OPC_MODE", "gateway"),
        opc_timeout: int = int(os.environ.get("OPC_TIMEOUT", 1000)),
    ):
        self.OPC_HOST = opc_host
        self.OPC_SERVER = opc_server
        self.OPC_CLIENT = opc_client
        self.OPC_GATEWAY_HOST = opc_gateway_host
        self.OPC_GATEWAY_PORT = opc_gateway_port
        self.OPC_CLASS = opc_class
        self.OPC_MODE = opc_mode
        self.OPC_TIMEOUT = opc_timeout

    def print_config(self):
        print("Open Opc Config:")
        for key, value in self.__dict__.items():
            print(f"{key:20}  : {value}")
