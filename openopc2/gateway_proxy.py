# -*- coding: utf-8 -*-
#
# Iterativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2015 Iterativ GmbH. All rights reserved.
#
# Created on 2022-10-24
# @author: lorenz.padberg@iterativ.ch
import Pyro5.client
from Pyro5.api import register_class_to_dict, register_dict_to_class

from openopc2.opc_types import TagProperties


class OpenOpcGatewayProxy:
    def __init__(self, host: str = 'localhost', port: int = 7766):
        self.host = host
        self.port = port

        # Register custom serializers
        register_class_to_dict(TagProperties, TagProperties.class_to_dict)
        register_dict_to_class("opc_types.TagProperties", TagProperties.dict_to_class)


    def get_server_proxy(self):
        with Pyro5.client.Proxy(f"PYRO:OpenOpcGatewayServer@{self.host}:{self.port}") as open_opc_gateway_server:
            return open_opc_gateway_server

    def get_opc_da_client_proxy(self):
        with Pyro5.client.Proxy(f"PYRO:OpcDaClient@{self.host}:{self.port}") as opc_da_client_proxy:
            return opc_da_client_proxy


