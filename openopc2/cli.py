"""
Command line interface for OpenOPC Service
"""
from typing import Optional, List, Dict, Any, Tuple, cast

from Pyro5.errors import CommunicationError

import typer

# pylint: disable=redefined-builtin
from rich import print
from rich.console import Console
from rich.table import Table

from openopc2.config import OpenOpcConfig
from openopc2.gateway_proxy import OpenOpcGatewayProxy
from openopc2.da_client import OpcDaClient
from openopc2.logger import log

from openopc2.opc_types import ProtocolMode, DataSource, LogLevel

open_opc_config = OpenOpcConfig()

TagsArgument = typer.Argument(..., help='Tags to read')
ProtocolModeOption = typer.Option(
    ProtocolMode.GATEWAY,
    help='Protocol mode',
    case_sensitive=False
)
GroupSizeOption = typer.Option(
    None,
    help='Group tags into group_size items per transaction'
)
DataSourceOption = typer.Option(
    DataSource.HYBRID,
    help='Data SOURCE for reads (cache, device, hybrid)',
    case_sensitive=False
)
IncludeErrorMessagesOption = typer.Option(
    False,
    help='Include descriptive error message strings'
)
TagValuePairsArgument = typer.Argument(...,
                                       help='Tag value pairs to write (use ITEM,VALUE)'
                                       )
PauseOption = typer.Option(0, help='Sleep time between transactionsin milliseconds')
UpdateRateOption = typer.Option(0, help='Update rate for group in milliseconds')
TimeoutOption = typer.Option(10000, help='Read timeout in milliseconds')
LogLevelOption = typer.Option(LogLevel.WARNING, help='Log level')
OutputCsvOption = typer.Option(False, help='Output in CSV format')

app = typer.Typer()

def get_opc_da_client(protocol_mode: ProtocolMode) -> OpcDaClient:
    """
    Returns a OPC DA Client based on the given protocol mode
    """

    if ProtocolMode.COM == protocol_mode:
        return OpcDaClient(open_opc_config)
    if ProtocolMode.GATEWAY == protocol_mode:
        return OpenOpcGatewayProxy(open_opc_config.OPC_GATEWAY_HOST,
                                   open_opc_config.OPC_GATEWAY_PORT).get_opc_da_client_proxy()
    raise NotImplementedError(f"Protocol mode {protocol_mode} is unrecognized")


@app.command()
def read(
        tags: list[str] = TagsArgument,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        group_size: Optional[int] = GroupSizeOption,
        pause: int = PauseOption,
        source: DataSource = DataSourceOption,
        update_rate: int = UpdateRateOption,
        timeout: int = TimeoutOption,
        include_error_messages: bool = IncludeErrorMessagesOption,
        output_csv: bool = OutputCsvOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    Read values
    """
    log.setLevel(log_level.upper())
    client = get_opc_da_client(protocol_mode)
    client.connect(open_opc_config.OPC_HOST, open_opc_config.OPC_SERVER)
    response: list[str] = client.read(tags,
                                      group='test',
                                      size=group_size,
                                      pause=pause,
                                      source=source,
                                      update=update_rate,
                                      timeout=timeout,
                                      sync=True,
                                      include_error=include_error_messages
                                      )
    if output_csv:
        print(','.join(response))
    else:
        print(response)


@app.command()
def write(
        tag_value_pairs: list[str] = TagValuePairsArgument,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        group_size: Optional[int] = GroupSizeOption,
        pause: int = PauseOption,
        include_error_messages: bool = IncludeErrorMessagesOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    Write values
    """
    log.setLevel(log_level.upper())

    # Validate and transform tag value pairs
    tag_values: list[Tuple[str, str]] = []
    try:
        for tag in tag_value_pairs:
            tag_values.append(tuple(tag.split(',')))
    except IndexError:
        log.error('Write input must be in ITEM,VALUE (CSV) format')
        return

    try:
        response = get_opc_da_client(protocol_mode).write(
            tag_value_pairs=tag_values,
            size=group_size,
            pause=pause,
            include_error=include_error_messages
        )
        print(response)
    except CommunicationError as error:
        print(f"Could not write to OPC server: {error}")


@app.command()
def list_clients() -> None:
    """
    [EXPERIMENTAL] List clients of OpenOPC Gateway Server
    """
    console = Console()
    table = Table(title="OpenOPC Gateway Server Clients")
    with console.status("Getting clients..."):
        clients: List[Dict[str, Any]] = OpenOpcGatewayProxy().get_server_proxy().get_clients()
        if not clients:
            print('No clients found')
            return

        table.add_column("Client ID", style="cyan")
        table.add_column("TX time", style="magenta")
        table.add_column("Init time", style="green")

        for client in clients:
            table.add_row(client['client_id'], client['tx_time'], client['init_time'])
    console.print(table)


@app.command()
def properties(
        tags: list[str] = TagsArgument,
        protocol_mode: ProtocolMode = ProtocolModeOption,
) -> None:
    """
    Show properties of given tags
    """
    console = Console()
    with console.status("Reading properties..."):
        response = get_opc_da_client(protocol_mode).properties(
            tags
        )
    print(response)


@app.command()
def server_info(protocol_mode: ProtocolMode = ProtocolModeOption) -> None:
    """
    Display OPC server information
    """
    response: Optional[List[str]] = get_opc_da_client(protocol_mode).info()
    print(response)


def cli() -> None:
    """
    Command line interface for OpenOPC Gateway Service
    """
    try:
        app()
    except NameError:
        log.error("DCOM is only supported on Windows. Use --protocol_mode openopc")
    except CommunicationError as error:
        log.error(f"Could not connect to OPC server: {error}")


if __name__ == '__main__':
    cli()
