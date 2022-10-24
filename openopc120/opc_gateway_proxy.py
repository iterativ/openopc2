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

from openopc120.opc_da_client import OpcDaClient
import Pyro4.core

logger = logging.getLogger(__name__)


class OpenOpcGatewayProxy:
    def __init__(self, host: str = 'localhost', port: int = 7766):
        self.host = host
        self.port = port
        self.open_opc_gateway: OpcDaClient = self.get_proxy()

    def get_proxy(self):
        with Pyro4.Proxy(f"PYRO:OpenOpcGatewayServer@{self.host}:{self.port}") as open_opc_gateway:
            return open_opc_gateway

    def get_sessions(self):
        logger.info("Get sessions Open Opc OpcDaClient")
        """Return sessions in OpenOPC Gateway Service as GUID:host hash"""
        return self.open_opc_gateway.get_clients()

    def open_client(self, opc_class: str) -> OpcDaClient:
        """Connect to the specified OpenOPC Gateway Service"""
        logger.info("Creating Open Opc OpcDaClient")
        return self.open_opc_gateway.create_client(opc_class)
