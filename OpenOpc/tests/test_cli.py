import os
from unittest import TestCase

import OpenOpc.opc as opc

class TestOpcCli(TestCase):
    def test_help(self):
        opc.main()
