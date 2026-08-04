import os

from openopc2.config import OpenOpcConfig
from openopc2.exceptions import OPCError


class OpcAeCom:
    """
    Low-level OPC AE COM boundary.

    The public AE client depends on this small interface so tests and gateway code
    can use fakes while the Windows custom COM implementation is filled in.
    """

    def __init__(self, open_opc_config: OpenOpcConfig = OpenOpcConfig()):
        self.config = open_opc_config
        self.server = None
        self.host = "localhost"
        self.opc_client = None

    def connect(self, server: str | None, host: str):
        if os.name != "nt":
            raise OPCError("OPC AE COM access is only available on Windows. Use gateway mode from non-Windows clients.")
        try:
            import comtypes.client  # noqa: F401
        except ImportError as error:
            raise OPCError("OPC AE COM access requires the 'comtypes' package") from error

        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def disconnect(self):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def get_status(self):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def query_available_filters(self):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def query_event_categories(self, event_types):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def query_event_attributes(self, category_id):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def query_condition_names(self, category_id):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def query_subcondition_names(self, condition_name):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def query_source_conditions(self, source):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def create_subscription(self, active, buffer_time, max_size, client_handle):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def get_condition_state(self, source, condition_name, attribute_ids):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")

    def ack_condition(self, references, acknowledger_id, comment):
        raise NotImplementedError("Raw OPC AE custom COM binding is not implemented yet")
