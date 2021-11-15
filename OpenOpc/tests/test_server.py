from unittest import TestCase

import pywintypes

from OpenOpc.OpenOPC import client
from OpenOpc.tests.opc_server_config import OPC_SERVER

pywintypes.datetime = pywintypes.TimeType

class TestServerInfo(TestCase):
    def setUp(self) -> None:
        self.opc_client = client()
        self.opc_client.connect(OPC_SERVER)

    def test_get_server(self):
        available_servers = self.opc_client.servers()
        print(available_servers)
        self.assertIsNotNone(available_servers)

    def test_get_info(self):
        info = self.opc_client.info()
        self.assertEqual(info[0], ('Protocol', 'DCOM'))
        self.assertEqual(info[1],  ('Class', 'OPC.Automation'))
        self.assertEqual(info[2],  ('Client Name', 'OpenOPC'))
        self.assertEqual(info[3][0], 'OPC Host')

    def test_close_connection(self):
        self.opc_client.close()
        self.assertRaises(IndexError, self.opc_client.info)

    def test_ping(self):
        ping = self.opc_client.ping()
        self.assertTrue(ping)