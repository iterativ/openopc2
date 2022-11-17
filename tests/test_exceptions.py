from unittest import TestCase, skipIf
from openopc2.exceptions import  OPCError
from test_config import test_config


@skipIf(test_config().OPC_MODE != 'com', "COM interface tests ony if OPC_MODE is com is disabled")
class TestOpcError(TestCase):

    def test_raise(self):
        self.assertRaises(OPCError, raise_error)

    def test_serialize_opc_error(self):
        import win32com.client
        import pythoncom

        try:
            pythoncom.CoInitialize()
            self.opc_client = win32com.client.gencache.EnsureDispatch('Foo', 0)
        except pythoncom.com_error as err:
            pythoncom.CoUninitialize()
            opc_error = OPCError(f'Dispatch: {err}')
            as_dict = opc_error.class_to_dict()
            as_exception = OPCError('').dict_to_class('sd', as_dict)
            pass


def raise_error():
    raise OPCError('Bad OPC Error')