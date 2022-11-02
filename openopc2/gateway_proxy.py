# -*- coding: utf-8 -*-
#
# Iterativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2015 Iterativ GmbH. All rights reserved.
#
# Created on 2022-10-24
# @author: lorenz.padberg@iterativ.ch
import logging
import Pyro5.client

logger = logging.getLogger(__name__)


class OpenOpcGatewayProxy:
    def __init__(self, host: str = 'localhost', port: int = 7766):
        self.host = host
        self.port = port

    def get_server_proxy(self):
        with Pyro5.client.Proxy(f"PYRO:OpenOpcGatewayServer@{self.host}:{self.port}") as open_opc_gateway_server:
            return open_opc_gateway_server

    def get_opc_da_client_proxy(self):
        with Pyro5.client.Proxy(f"PYRO:OpcDaClient@{self.host}:{self.port}") as opc_da_client_proxy:
            return opc_da_client_proxy


