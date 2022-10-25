import os


class OpenOpcConfig:
    def __init__(self):
        self.OPC_HOST: str = 'localhost'
        self.OPC_SERVER: str = 'Hci.TPNServer;HwHsc.OPCServer;OpenOpcGatewayServer.deltav.1;AIM.OPC.1;Yokogawa.ExaopcDAEXQ.1;OSI.DA.1;OPC.PHDServerDA.1;Aspen.Infoplus21_DA.1;National Instruments.OPCLabVIEW;RSLinx OPC Server;KEPware.KEPServerEx.V4;Matrikon.OPC.Simulation;Prosys.OPC.Simulation;CCOPC.XMLWrapper.1;OPC.SimaticHMI.CoRtHmiRTm.1'
        self.OPC_CLIENT: str = 'OpenOPC'
        self.OPC_GATEWAY_HOST: str = os.environ.get('OPC_GATE_HOST', 'localhost')
        self.OPC_GATEWAY_PORT: str = int(os.environ.get('OPC_GATE_PORT', 7766))
        self.OPC_CLASS: str = os.environ.get('OPC_CLASS', "OPC.Automation")
        self.OPC_MODE: str = os.environ.get('OPC_CLIENT', "OpenOPC")

    def print_config(self):
        print('Open Opc Config:')
        for key, value in self.__dict__.items():
            print(f'{key:20}  : {value}')


open_opc_config = OpenOpcConfig()
