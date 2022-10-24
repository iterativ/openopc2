from openopc120.OpenOPC import OpcDaClient
from opc_gateway_proxy import OpenOpcGatewayProxy

OPC_SERVER = "Matrikon.OPC.Simulation.1"
OPC_HOST = "192.168.0.115"
OPC_CLASS = "OPC.Automation"
USE_GATEWAY = True


def connect_opc_client(use_gateway=USE_GATEWAY):
    opc_da_client = OpenOpcGatewayProxy(OPC_HOST).open_client() if use_gateway else OpcDaClient(OPC_CLASS)
    opc_da_client.connect(OPC_SERVER, OPC_HOST)
    return opc_da_client
