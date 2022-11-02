from unittest import TestCase

from test_config import test_config
from utils import get_opc_da_client


class TestServerInfo(TestCase):
    def setUp(self) -> None:
        self.opc_client = get_opc_da_client(test_config())

    def test_get_server(self):
        available_servers = self.opc_client.servers()
        print(available_servers)
        self.assertIsNotNone(available_servers)

    def test_get_info(self):
        info = self.opc_client.info()
        if test_config().OPC_MODE == 'gateway':
            self.assertEqual(('Protocol', 'DCOM'), info[0])
            self.assertEqual(('Class', 'OPC.Automation'), info[1])
            self.assertEqual('Client Name', info[2][0])
            self.assertEqual(('OPC Server', 'Matrikon.OPC.Simulation.1'), info[4])

        else:
            self.assertEqual(('Protocol', 'DCOM'), info[0])
            self.assertEqual(('Client Name', ''), info[2])
            self.assertEqual('OPC Host', info[3][0], )
            self.assertEqual(('Class', 'OPC.Automation'), info[1])

    def test_ping(self):
        ping = self.opc_client.ping()
        self.assertTrue(ping)
