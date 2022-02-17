from openopc120.OpenOPC import client, open_client

OPC_SERVER = "Matrikon.OPC.Simulation.1"
OPC_HOST = "192.168.0.115"
USE_GATEWAY = False


def connect_opc_client(use_gateway=USE_GATEWAY):
    opc_da_client = open_client(OPC_HOST) if use_gateway else client(OPC_SERVER)
    opc_da_client.connect(OPC_SERVER, OPC_HOST)
    return opc_da_client
