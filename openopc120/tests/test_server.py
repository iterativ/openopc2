from unittest import TestCase

from opc_server_config import connect_opc_client, USE_GATEWAY


class TestServerInfo(TestCase):
    def setUp(self) -> None:
        self.opc_client = connect_opc_client()

    def test_get_server(self):
        available_servers = self.opc_client.servers()
        print(available_servers)
        self.assertIsNotNone(available_servers)

    def test_get_info(self):
        info = self.opc_client.info()
        if USE_GATEWAY:
            self.assertEqual(('Protocol', 'OpenOPC'), info[0])
            self.assertEqual('Gateway Host', info[1][0])
            self.assertEqual('Gateway Version', info[2][0])
            self.assertEqual(('Class', 'Matrikon.OPC.Automation'), info[3] )

        else:
            self.assertEqual(('Protocol', 'DCOM'), info[0])
            self.assertEqual(('Client Name', ''), info[2])
            self.assertEqual('OPC Host', info[3][0], )
            self.assertEqual(('Class', 'OPC.Automation'), info[1])


    #
    # def test_close_connection(self):
    #     self.opc_client.close()
    #     self.assertRaises(IndexError, self.opc_client.info)

    def test_ping(self):
        ping = self.opc_client.ping()
        self.assertTrue(ping)
