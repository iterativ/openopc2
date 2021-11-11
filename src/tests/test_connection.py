from unittest import TestCase

from src.OpenOPC import client

OPC_SERVER = "Matrikon.OPC.Simulation.1"


class TestConnection(TestCase):
    def test_get_server(self):
        opc_client = client()
        available_servers = opc_client.servers()
        print(available_servers)
        self.assertIsNotNone(available_servers)

    def test_list_flat_return_parameters(self):
        opc_client = client()
        opc_client.connect(OPC_SERVER)
        parameters = opc_client.list(recursive=False, include_type=False, flat=True)
        for p in parameters:
            print(p)
        self.assertIs(type(parameters), list)
        self.assertIs(type(parameters[0]), str)
        self.assertTrue("Triangle Waves.UInt4" in parameters)

    def test_list_type_return_parameters(self):
        opc_client = client()
        opc_client.connect(OPC_SERVER)
        parameters = opc_client.list(recursive=False, include_type=True, flat=False)
        for p in parameters:
            print(p)
        self.assertIs(type(parameters), list)
        self.assertIs(type(parameters[0]), tuple)
        self.assertTrue(('Simulation Items', 'Branch') in parameters)

    def test_list_recursive_return_parameters(self):
        opc_client = client()
        opc_client.connect(OPC_SERVER)
        parameters = opc_client.list(recursive=True, include_type=False, flat=False)
        for p in parameters:
            print(p)
        self.assertIs(type(parameters), list)
        self.assertIs(type(parameters[0]), str)
        self.assertTrue("Triangle Waves.UInt4" in parameters)



