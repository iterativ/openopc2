from openopc2.gateway_proxy import OpenOpcGatewayProxy
from openopc2.da_client import OpcDaClient

OPC_SERVER = "Matrikon.OPC.Simulation.1"
OPC_HOST = "192.168.0.115"
OPC_CLASS = "OPC.Automation"
USE_GATEWAY = True


def connect_opc_client(use_gateway=USE_GATEWAY):
    if use_gateway:
        host = OpenOpcGatewayProxy(OPC_HOST)
        opc_server_proxy = host.get_server_proxy()
        opc_da_client = host.get_opc_da_client_proxy()
    else:
        opc_da_client = OpcDaClient(OPC_CLASS)

    opc_da_client.connect(OPC_SERVER, OPC_HOST)
    return opc_da_client
