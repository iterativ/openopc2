import os
from typing import Literal


class OpenOpcConfig:
    def __init__(self):
        self.OPC_HOST: str = 'localhost'
        self.OPC_SERVER: str = 'Matrikon.OPC.Simulation'
        self.OPC_CLIENT: str = 'OpenOPC'
        self.OPC_GATEWAY_HOST: str = os.environ.get('OPC_GATE_HOST', '192.168.0.115')
        self.OPC_GATEWAY_PORT: int = int(os.environ.get('OPC_GATE_PORT', 7766))
        self.OPC_CLASS: str = "OPC.Automation"  # os.environ.get('OPC_CLASS', "OPC.Automation")
        self.OPC_MODE: Literal["GATEWAY", "COM"] = os.environ.get('OPC_MODE', "gateway")
        self.OPC_TIMEOUT: int = os.environ.get('OPC_TIMEOUT', 1000)

    def print_config(self):
        print('Open Opc Config:')
        for key, value in self.__dict__.items():
            print(f'{key:20}  : {value}')


