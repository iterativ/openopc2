from openopc2.config import OpenOpcConfig
from openopc2.da_client import OpcDaClient
from openopc2.gateway_proxy import OpenOpcGatewayProxy
import structlog

logger = structlog.getLogger(__name__)

def get_opc_da_client(config: OpenOpcConfig = OpenOpcConfig()) -> OpcDaClient:
    if config.OPC_MODE == "gateway":
        opc_da_client = OpenOpcGatewayProxy(config.OPC_GATEWAY_HOST, config.OPC_GATEWAY_PORT).get_opc_da_client_proxy()
    else:
        opc_da_client = OpcDaClient(config)


    opc_da_client.connect(config.OPC_SERVER, config.OPC_HOST)
    logger.info("Successfully connected", opc_server=config.OPC_SERVER,opc_host=config.OPC_HOST, mode=config.OPC_MODE)

    return opc_da_client
