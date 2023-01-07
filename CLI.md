# `openopc2 CLI`

**Usage**:

```console
$ openopc2 CLI [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `list-clients`: \[EXPERIMENTAL\] List clients of OpenOPC...
- `list-tags`: List tags (items) of OPC server
- `properties`: Show properties of given tags
- `read`: Read tags
- `server-info`: Display OPC server information
- `write`: Write values

## `openopc2 CLI list-clients`

\[EXPERIMENTAL\] List clients of OpenOPC Gateway Server

**Usage**:

```console
$ openopc2 CLI list-clients [OPTIONS]
```

**Options**:

- `--log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]`: Log level  \[default: WARNING\]
- `--help`: Show this message and exit.

## `openopc2 CLI list-tags`

List tags (items) of OPC server

**Usage**:

```console
$ openopc2 CLI list-tags [OPTIONS]
```

**Options**:

- `--protocol-mode [com|gateway]`: Protocol mode  \[default: gateway\]
- `--opc-server TEXT`: OPC Server to connect to  \[default: Matrikon.OPC.Simulation\]
- `--opc-host TEXT`: OPC Host to connect to  \[default: localhost\]
- `--gateway-host TEXT`: OPC Gateway Host to connect to  \[default: 192.168.0.115\]
- `--gateway-port INTEGER`: OPC Gateway Port to connect to  \[default: 7766\]
- `--recursive / --no-recursive`: Recursively read sub-tags  \[default: False\]
- `--output-csv / --no-output-csv`: Output in CSV format  \[default: False\]
- `--log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]`: Log level  \[default: WARNING\]
- `--help`: Show this message and exit.

## `openopc2 CLI properties`

Show properties of given tags

**Usage**:

```console
$ openopc2 CLI properties [OPTIONS] TAGS...
```

**Arguments**:

- `TAGS...`: Tags to read  \[required\]

**Options**:

- `--protocol-mode [com|gateway]`: Protocol mode  \[default: gateway\]
- `--opc-server TEXT`: OPC Server to connect to  \[default: Matrikon.OPC.Simulation\]
- `--opc-host TEXT`: OPC Host to connect to  \[default: localhost\]
- `--gateway-host TEXT`: OPC Gateway Host to connect to  \[default: 192.168.0.115\]
- `--gateway-port INTEGER`: OPC Gateway Port to connect to  \[default: 7766\]
- `--log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]`: Log level  \[default: WARNING\]
- `--help`: Show this message and exit.

## `openopc2 CLI read`

Read tags

**Usage**:

```console
$ openopc2 CLI read [OPTIONS] TAGS...
```

**Arguments**:

- `TAGS...`: Tags to read  \[required\]

**Options**:

- `--protocol-mode [com|gateway]`: Protocol mode  \[default: gateway\]
- `--opc-server TEXT`: OPC Server to connect to  \[default: Matrikon.OPC.Simulation\]
- `--opc-host TEXT`: OPC Host to connect to  \[default: localhost\]
- `--gateway-host TEXT`: OPC Gateway Host to connect to  \[default: 192.168.0.115\]
- `--gateway-port INTEGER`: OPC Gateway Port to connect to  \[default: 7766\]
- `--group-size INTEGER`: Group tags into group_size tags per transaction
- `--pause INTEGER`: Sleep time between transactionsin milliseconds  \[default: 0\]
- `--source [cache|device|hybrid]`: Data SOURCE for reads (cache, device, hybrid)  \[default: hybrid\]
- `--update-rate INTEGER`: Update rate for group in milliseconds  \[default: 0\]
- `--timeout INTEGER`: Read timeout in milliseconds  \[default: 10000\]
- `--include-error-messages / --no-include-error-messages`: Include descriptive error message strings  \[default: False\]
- `--output-csv / --no-output-csv`: Output in CSV format  \[default: False\]
- `--log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]`: Log level  \[default: WARNING\]
- `--help`: Show this message and exit.

## `openopc2 CLI server-info`

Display OPC server information

**Usage**:

```console
$ openopc2 CLI server-info [OPTIONS]
```

**Options**:

- `--protocol-mode [com|gateway]`: Protocol mode  \[default: gateway\]
- `--opc-server TEXT`: OPC Server to connect to  \[default: Matrikon.OPC.Simulation\]
- `--opc-host TEXT`: OPC Host to connect to  \[default: localhost\]
- `--gateway-host TEXT`: OPC Gateway Host to connect to  \[default: 192.168.0.115\]
- `--gateway-port INTEGER`: OPC Gateway Port to connect to  \[default: 7766\]
- `--log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]`: Log level  \[default: WARNING\]
- `--help`: Show this message and exit.

## `openopc2 CLI write`

Write values

**Usage**:

```console
$ openopc2 CLI write [OPTIONS] TAG_VALUE_PAIRS...
```

**Arguments**:

- `TAG_VALUE_PAIRS...`: Tag value pairs to write (use ITEM,VALUE)  \[required\]

**Options**:

- `--protocol-mode [com|gateway]`: Protocol mode  \[default: gateway\]
- `--opc-server TEXT`: OPC Server to connect to  \[default: Matrikon.OPC.Simulation\]
- `--opc-host TEXT`: OPC Host to connect to  \[default: localhost\]
- `--gateway-host TEXT`: OPC Gateway Host to connect to  \[default: 192.168.0.115\]
- `--gateway-port INTEGER`: OPC Gateway Port to connect to  \[default: 7766\]
- `--group-size INTEGER`: Group tags into group_size tags per transaction
- `--pause INTEGER`: Sleep time between transactionsin milliseconds  \[default: 0\]
- `--include-error-messages / --no-include-error-messages`: Include descriptive error message strings  \[default: False\]
- `--log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]`: Log level  \[default: WARNING\]
- `--help`: Show this message and exit.
