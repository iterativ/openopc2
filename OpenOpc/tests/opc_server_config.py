from OpenOpc.OpenOPC import client, open_client

OPC_SERVER = "Matrikon.OPC.Simulation.1"
OPC_HOST = "192.168.0.115"


def connect_opc_client(use_gateway=True):
    opc_da_client = open_client(OPC_HOST) if use_gateway else client()
    opc_da_client.connect(OPC_SERVER, OPC_HOST)
    return opc_da_client
