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
            self.assertEqual(info[0], ('Protocol', 'OpenOPC'))
            self.assertEqual(info[1][0], 'Gateway Host')
            self.assertEqual(info[2][0], 'Gateway Version')
            self.assertEqual(info[3], ('Class', 'Matrikon.OPC.Automation'))

        else:
            self.assertEqual(info[0], ('Protocol', 'DCOM'))
            self.assertEqual(info[1], ('Class', 'OPC.Automation'))
            self.assertEqual(info[2], ('Client Name', 'OpenOPC'))
            self.assertEqual(info[3][0], 'OPC Host')
    #
    # def test_close_connection(self):
    #     self.opc_client.close()
    #     self.assertRaises(IndexError, self.opc_client.info)

    def test_ping(self):
        ping = self.opc_client.ping()
        self.assertTrue(ping)
