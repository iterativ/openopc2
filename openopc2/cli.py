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
from openopc2.ae_client import OpcAeClient
from openopc2.ae_types import AeEventType, AeFilter
from openopc2.da_client import OpcDaClient
from openopc2.logger import log

from openopc2.opc_types import ProtocolMode, DataSource, LogLevel

open_opc_config = OpenOpcConfig()

TagsArgument = typer.Argument(..., help='Tags to read')
TagValuePairsArgument = typer.Argument(...,
                                       help='Tag value pairs to write (use ITEM=VALUE)'
                                       )
OpcServerOption = typer.Option(open_opc_config.OPC_SERVER, help='OPC Server to connect to')
OpcAeServerOption = typer.Option(open_opc_config.OPC_AE_SERVER, help='OPC AE Server to connect to')
OpcHostOption = typer.Option(open_opc_config.OPC_HOST, help='OPC Host to connect to')
GatewayHostOption = typer.Option(open_opc_config.OPC_GATEWAY_HOST, help='OPC Gateway Host to connect to')
GatewayPortOption = typer.Option(open_opc_config.OPC_GATEWAY_PORT,help='OPC Gateway Port to connect to')
ProtocolModeOption = typer.Option(ProtocolMode.GATEWAY,help='Protocol mode', case_sensitive=False)
GroupSizeOption = typer.Option(None, help='Group tags into group_size tags per transaction')
DataSourceOption = typer.Option(DataSource.HYBRID,help='Data SOURCE for reads (cache, device, hybrid)', case_sensitive=False)
IncludeErrorMessagesOption = typer.Option(False,help='Include descriptive error message strings')
PauseOption = typer.Option(0, help='Sleep time between transactionsin milliseconds')
UpdateRateOption = typer.Option(0, help='Update rate for group in milliseconds')
TimeoutOption = typer.Option(10000, help='Read timeout in milliseconds')
LogLevelOption = typer.Option(LogLevel.WARNING, help='Log level')
OutputCsvOption = typer.Option(False, help='Output in CSV format')
RecursiveOption = typer.Option(False, help="Recursively read sub-tags")
AeEventTypeOption = typer.Option("condition", help="AE event type: simple, tracking, condition, all")
AeSeverityMinOption = typer.Option(1, help="Minimum AE severity")
AeSeverityMaxOption = typer.Option(1000, help="Maximum AE severity")
AeCategoryOption = typer.Option(None, help="AE event category ID")
AeAreaOption = typer.Option(None, help="AE area filter")
AeSourceOption = typer.Option(None, help="AE source filter")

app = typer.Typer()


def get_connected_da_client(
        protocol_mode: ProtocolMode,
        opc_server: str,
        opc_host: str,
        gateway_host: str,
        gateway_port: int
) -> OpcDaClient:
    """
    Returns a OPC DA Client based on the given protocol mode
    """
    client: Optional[OpcDaClient] = None
    if ProtocolMode.COM == protocol_mode:
        client = OpcDaClient(open_opc_config)

    if ProtocolMode.GATEWAY == protocol_mode:
        client = cast(OpcDaClient, OpenOpcGatewayProxy(gateway_host, gateway_port).get_opc_da_client_proxy())
    if client is not None:
        client.connect(opc_server, opc_host)
        return client
    raise NotImplementedError(f"Protocol mode {protocol_mode} is unrecognized")


def _parse_ae_event_type(event_type: str) -> AeEventType:
    event_types = AeEventType(0)
    for item in event_type.split(","):
        clean = item.strip().lower()
        if clean == "simple":
            event_types |= AeEventType.SIMPLE
        elif clean == "tracking":
            event_types |= AeEventType.TRACKING
        elif clean == "condition":
            event_types |= AeEventType.CONDITION
        elif clean == "all":
            event_types |= AeEventType.ALL
        else:
            raise typer.BadParameter(f"Unknown AE event type: {item}")
    return event_types


def _build_ae_filter(event_type: str, severity_min: int, severity_max: int, category: Optional[int],
                     area: Optional[str], source: Optional[str]) -> AeFilter:
    return AeFilter(
        event_types=_parse_ae_event_type(event_type),
        categories=tuple([category] if category is not None else []),
        low_severity=severity_min,
        high_severity=severity_max,
        areas=tuple([area] if area else []),
        sources=tuple([source] if source else []),
    )


def get_connected_ae_client(
        protocol_mode: ProtocolMode,
        opc_ae_server: str,
        opc_host: str,
        gateway_host: str,
        gateway_port: int
) -> OpcAeClient:
    """
    Returns an OPC AE Client based on the given protocol mode
    """
    client: Optional[OpcAeClient] = None
    if ProtocolMode.COM == protocol_mode:
        client = OpcAeClient(open_opc_config)

    if ProtocolMode.GATEWAY == protocol_mode:
        client = cast(OpcAeClient, OpenOpcGatewayProxy(gateway_host, gateway_port).get_opc_ae_client_proxy())
    if client is not None:
        client.connect(opc_ae_server, opc_host)
        return client
    raise NotImplementedError(f"Protocol mode {protocol_mode} is unrecognized")


@app.command()
def read(
        tags: List[str] = TagsArgument,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_server: str = OpcServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
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
    Read tags
    """
    log.setLevel(log_level.upper())
    client = get_connected_da_client(
        protocol_mode,
        opc_server,
        opc_host,
        gateway_host,
        gateway_port
    )
    responses: List[str] = client.read(tags,
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
        for response in responses:
            print(','.join(str(val) for val in response))
        return

    table = Table(title="Tags")
    table.add_column("Tag", style="cyan")
    table.add_column("Value", style="bold dark_green")
    table.add_column("Quality", style="gold3")
    table.add_column("Time", style="cyan")
    for response in responses:
        table.add_row(*(str(val) for val in response))
    Console().print(table)


@app.command()
def write(
        tag_value_pairs: List[str] = TagValuePairsArgument,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_server: str = OpcServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
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
    tag_values: List[Tuple[str, str]] = []
    try:
        for tag in tag_value_pairs:
            tag_values.append(tuple(tag.split('=')))
    except IndexError:
        log.error('Write input must be in TAG=VALUE format')
        return

    try:
        print(f"Writing {len(tag_values)} value(s)...")
        responses: List[Tuple[str, str]] = get_connected_da_client(
            protocol_mode,
            opc_server,
            opc_host,
            gateway_host,
            gateway_port
        ).write(
            tag_value_pairs=tag_values,
            size=group_size,
            pause=pause,
            include_error=include_error_messages
        )
        console = Console()
        failed = list(filter(lambda response: response[1] != "Success",
                             # Ugly hack to handle dynamic return value of write()
                             [responses] if isinstance(responses, Tuple) else responses
                             ))
        if failed:
            failed_tag_names = map(lambda response: response[0], failed)
            console.print(f"Failed to write {', '.join(failed_tag_names)}", style="bold red")
        else:
            print("Success")
    except CommunicationError as error:
        log.error(f"Could not write to OPC server: {error}")


@app.command()
def list_clients(log_level: LogLevel = LogLevelOption) -> None:
    """
    [EXPERIMENTAL] List clients of OpenOPC Gateway Server
    """
    log.setLevel(log_level.upper())
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
def list_tags(
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_server: str = OpcServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        recursive: bool = RecursiveOption,
        output_csv: bool = OutputCsvOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    List tags (items) of OPC server
    """
    log.setLevel(log_level.upper())
    console = Console()
    tags: List[str]
    with console.status("Getting tags..."):
        tags = get_connected_da_client(
            protocol_mode,
            opc_server,
            opc_host,
            gateway_host,
            gateway_port
        ).list(recursive=recursive)
    if output_csv:
        print(','.join(tags))
        return
    table = Table(title="Tags", style="green")
    table.add_column("#")
    table.add_column("Tag name")
    for i, tag in enumerate(tags):
        table.add_row(str(i), tag)
    Console().print(table)


@app.command()
def properties(
        tags: List[str] = TagsArgument,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_server: str = OpcServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    Show properties of given tags
    """
    log.setLevel(log_level.upper())
    properties: List[Tuple[int, str, Any]] = get_connected_da_client(
        protocol_mode,
        opc_server,
        opc_host,
        gateway_host,
        gateway_port
    ).properties(tags)
    if not properties:
        print('No properties found')
        return

    table = Table(title="Properties")
    table.add_column("index", style="green")
    table.add_column("Tag Name", style="cyan")
    table.add_column("Data Type", style="dark_orange3")
    table.add_column("Access Rights", style="dark_orange3")
    table.add_column("Value", style="dark_orange3")
    for index, property in enumerate(properties):
        table.add_row(str(index), str(property.tag_name), str(property.data_type), str(property.access_rights), str(property.value),)
    Console().print(table)


@app.command()
def list_servers(
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_server: str = OpcServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    List all OPC DA servers
    """
    log.setLevel(log_level.upper())
    servers = get_connected_da_client(
        protocol_mode,
        opc_server,
        opc_host,
        gateway_host,
        gateway_port
    ).servers()
    table = Table(title="Available OPC DA servers")
    table.add_column("#", style="green")
    table.add_column("Server Name", style="green")

    for i, value in enumerate(servers):
        table.add_row(str(i), value)
    Console().print(table)


@app.command()
def server_info(
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_server: str = OpcServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    Display OPC server information
    """
    log.setLevel(log_level.upper())
    response: List[Tuple[str, str]] = get_connected_da_client(
        protocol_mode,
        opc_server,
        opc_host,
        gateway_host,
        gateway_port
    ).info()
    table = Table(title="Server info")
    table.add_column("Name", style="green")
    table.add_column("Value", style="dark_orange3")

    for value in response:
        table.add_row(value[0], value[1])
    Console().print(table)


@app.command()
def ae_categories(
        event_type: str = AeEventTypeOption,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_ae_server: str = OpcAeServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        output_csv: bool = OutputCsvOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    List OPC AE event categories
    """
    log.setLevel(log_level.upper())
    categories = get_connected_ae_client(
        protocol_mode,
        opc_ae_server,
        opc_host,
        gateway_host,
        gateway_port
    ).categories(_parse_ae_event_type(event_type))
    if output_csv:
        for category in categories:
            print(f"{category.category_id},{category.description},{category.event_type}")
        return
    table = Table(title="Available OPC AE categories")
    table.add_column("#", style="green")
    table.add_column("Category ID", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Event Type", style="dark_orange3")
    for index, category in enumerate(categories):
        table.add_row(str(index), str(category.category_id), category.description, str(category.event_type))
    Console().print(table)


@app.command()
def ae_refresh(
        event_type: str = AeEventTypeOption,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_ae_server: str = OpcAeServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        severity_min: int = AeSeverityMinOption,
        severity_max: int = AeSeverityMaxOption,
        category: Optional[int] = AeCategoryOption,
        area: Optional[str] = AeAreaOption,
        source: Optional[str] = AeSourceOption,
        timeout: int = TimeoutOption,
        output_csv: bool = OutputCsvOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    Refresh current OPC AE condition events
    """
    log.setLevel(log_level.upper())
    events = get_connected_ae_client(
        protocol_mode,
        opc_ae_server,
        opc_host,
        gateway_host,
        gateway_port
    ).refresh(
        filter=_build_ae_filter(event_type, severity_min, severity_max, category, area, source),
        timeout=timeout / 1000,
    )
    if output_csv:
        for event in events:
            print(f"{event.source},{event.time},{event.severity},{event.message}")
        return
    table = Table(title="OPC AE refresh")
    table.add_column("Source", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Severity", style="dark_orange3")
    table.add_column("Message", style="green")
    for event in events:
        table.add_row(event.source, str(event.time), str(event.severity), event.message)
    Console().print(table)


@app.command()
def ae_subscribe(
        event_type: str = AeEventTypeOption,
        protocol_mode: ProtocolMode = ProtocolModeOption,
        opc_ae_server: str = OpcAeServerOption,
        opc_host: str = OpcHostOption,
        gateway_host: str = GatewayHostOption,
        gateway_port: int = GatewayPortOption,
        severity_min: int = AeSeverityMinOption,
        severity_max: int = AeSeverityMaxOption,
        category: Optional[int] = AeCategoryOption,
        area: Optional[str] = AeAreaOption,
        source: Optional[str] = AeSourceOption,
        timeout: int = TimeoutOption,
        output_csv: bool = OutputCsvOption,
        log_level: LogLevel = LogLevelOption,
) -> None:
    """
    Subscribe to OPC AE event batches until the timeout expires
    """
    log.setLevel(log_level.upper())
    client = get_connected_ae_client(
        protocol_mode,
        opc_ae_server,
        opc_host,
        gateway_host,
        gateway_port
    )
    subscription = client.subscribe(
        filter=_build_ae_filter(event_type, severity_min, severity_max, category, area, source),
    )
    batch = subscription.next_batch(timeout=timeout / 1000)
    if batch is None:
        print("No AE events received")
        return
    if output_csv:
        for event in batch.events:
            print(f"{event.source},{event.time},{event.severity},{event.message}")
        return
    table = Table(title="OPC AE events")
    table.add_column("Source", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Severity", style="dark_orange3")
    table.add_column("Message", style="green")
    for event in batch.events:
        table.add_row(event.source, str(event.time), str(event.severity), event.message)
    Console().print(table)

@app.command()
def list_config(
) -> None:
    """
    Write values
    """
    OpenOpcConfig().print_config()


def cli() -> None:
    """
    Command line interface for OpenOPC Gateway Service
    """
    try:
        app()
    except NameError:
        log.error("com is only supported on Windows. Use --protocol_mode gateway")
    except CommunicationError as error:
        log.error(f"Could not connect to OPC server: {error}")


if __name__ == '__main__':
    cli()
