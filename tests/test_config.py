from openopc2.config import OpenOpcConfig

def test_config():
    open_opc_config = OpenOpcConfig()
    open_opc_config.OPC_SERVER = "Matrikon.OPC.Simulation.1"
    open_opc_config.OPC_GATEWAY_HOST = "192.168.0.115"
    open_opc_config.OPC_CLASS = "Graybox.OPC.DAWrapper"
    open_opc_config.OPC_MODE = 'com'
    return open_opc_config

