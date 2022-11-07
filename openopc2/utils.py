from openopc2.config import OpenOpcConfig
from openopc2.da_client import OpcDaClient
from openopc2.gateway_proxy import OpenOpcGatewayProxy


def get_opc_da_client(config: OpenOpcConfig = OpenOpcConfig()) -> OpcDaClient:
    if config.OPC_MODE == "gateway":
        opc_da_client = OpenOpcGatewayProxy(config.OPC_GATEWAY_HOST, config.OPC_GATEWAY_PORT).get_opc_da_client_proxy()
        print("OpenOPC in gateway mode")
    else:
        opc_da_client = OpcDaClient(config)
        print("OpenOPC in com mode")

    opc_da_client.connect(config.OPC_SERVER, config.OPC_HOST)
    return opc_da_client
