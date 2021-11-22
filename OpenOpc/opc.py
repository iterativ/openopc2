###########################################################################
#
# OpenOPC Command Line Client
#
# A cross-platform OPC-DA client built using the OpenOPC for Python
# library module.
#
# Copyright (c) 2007-2015 Barry Barnreiter (barrybb@gmail.com)
#
###########################################################################

from sys import *
from getopt import *
from os import *
import signal
import sys
import os
import types
import datetime
import re, time, csv
from OpenOpc.OpenOPC import OPC_CLASS, client, OPC_CLIENT, win32com_found, OPCError, open_client, TimeoutError, \
    get_sessions, OPC_SERVER

# https://realpython.com/command-line-interfaces-python-argparse/


try:
    import Pyro
except ImportError:
    pyro_found = False
else:
    pyro_found = True



def irotate(data, num_columns, value_idx=1):
    if num_columns == 0:
        for row in data: yield row
        return

    new_row = []

    for i, row in enumerate(data):
        if type(row) not in (list, tuple):
            value_idx = 0
            row = [row]

        new_row.append(row[value_idx])
        if (i + 1) % num_columns == 0:
            yield new_row
            new_row = []

    if len(new_row) > 0:
        yield new_row


# FUNCTION: Rotate the values of every N rows to form N columns

def rotate(data, num_columns, value_idx=1):
    return list(irotate(data, num_columns, value_idx))


# FUNCTION: Print output in the specified style from a list of data

def output(data, style='table', value_idx=1):
    global write
    name_idx = 0

    # Cast value to a stirng (trap Unicode errors)
    def to_str(value):
        try:
            if type(value) == float:
                return '%.4f' % value
            else:
                return str(value)
        except:
            return ''

    # Generator passed (single row passed at a time)
    if type(data) == types.GeneratorType:
        generator = True
        pad_length = []

    # List passed (multiple rows passed all at once)
    elif type(data) in (list, tuple):
        generator = False

        if len(data) == 0:
            return

        if type(data[0]) not in (list, tuple):
            data = [[e] for e in data]

        if style == 'table' or style == '':
            pad_length = []
            num_columns = len(data[0])
            for i in range(num_columns - 1):
                pad_length.append(len(max([to_str(row[i]) for row in data], key=len)) + 5)
            pad_length.append(0)
    else:
        raise TypeError("output(): 'data' parameter must be a list or a generator")

    if style == 'html':
        write('<table border=1>\n')

    rows = []

    for i, row in enumerate(data):
        rows.append(row)

        if style == 'values':
            write('%s' % str(row[value_idx]))
        elif style == 'pairs':
            write('%s,%s' % (row[name_idx], row[value_idx]))
        else:

            if generator and (style == 'table' or style == ''):

                # Convert single value into a single element list, thus making it
                # represent a 1-column wide table.
                if type(row) not in (list, tuple):
                    row = [row]

                num_columns = len(row)

                # Allow columns widths to always grow wider, but never shrink.
                # Unfortunetly we won't know the required width until the generator is finished!
                for k in range(num_columns - 1):
                    new_length = len(to_str(row[k]))
                    if i == 0:
                        pad_length.append(new_length + 5)
                    else:
                        if new_length - pad_length[k] > 0:  pad_length[k] = new_length
                if i == 0:
                    pad_length.append(0)

            for j, item in enumerate(row):
                if style == 'csv':
                    if j > 0: write(',')
                    write('%s' % to_str(item))
                elif style == 'html':
                    if j == 0: write('  <tr>\n')
                    if len(to_str(item)) < 40:
                        write('    <td nowrap>%s</td>\n' % to_str(item))
                    else:
                        write('    <td>%s</td>\n' % to_str(item))
                    if j == len(row) - 1: write('  </tr>')
                else:
                    if num_columns > 1:
                        write('%s' % to_str(item).ljust(pad_length[j]))
                    else:
                        write('%s' % to_str(item))

        write('\n')

    if style == 'html':
        write('</table>')

    return rows


# FUNCTION: Convert Unix time to formatted time string

def time2str(t):
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime('%x %H:%M:%S')


######## MAIN ########


class SigHandler:
    def __init__(self):
        self.signaled = 0
        self.sn = None

    def __call__(self, sn, sf):
        self.sn = sn
        self.signaled += 1


class OpcCli:
    def __init__(self):
        # Common function aliases
        write = sys.stdout.write

        # Initialize default settings

        if os.name == 'nt':
            opc_mode = 'dcom'
        else:
            opc_mode = 'open'
        self.opc_client = None
        self.action = 'read'
        self.style = 'table'
        self.append = ''
        self.num_columns = 0
        self.pipe = False
        self.verbose = False
        self.recursive = False
        self.read_function = 'async'
        self.data_source = 'hybrid'
        self.group_size = None
        self.update_rate = None
        self.tx_pause = 0
        self.repeat = 1
        self.repeat_pause = None
        self.property_ids = None
        self.include_err_msg = False
        self.opc_mode = environ.get('OPC_MODE', opc_mode)
        self.opc_class = environ.get('OPC_CLASS', OPC_CLASS)
        self.client_name = environ.get('OPC_CLIENT', OPC_CLIENT)
        self.opc_host = environ.get('OPC_HOST', 'localhost')
        self.opc_server = environ.get('OPC_SERVER', OPC_SERVER)
        self.open_host = environ.get('OPC_GATE_HOST', 'localhost')
        self.open_port = environ.get('OPC_GATE_PORT', 7766)
        self.timeout = int(environ.get('OPC_TIMEOUT', 5000)

    def parse_arguments(self):
        # Parse command line arguments

        if argv.count('-') > 0:
            argv[argv.index('-')] = '--pipe'
            pipe = True

        try:
            opts, args = gnu_getopt(argv[1:], 'rwlpfiqRSevx:m:C:H:P:c:h:s:L:F:z:o:a:u:t:g:y:n:',
                                    ['read', 'write', 'list', 'properties', 'flat', 'info', 'mode=', 'gate-host=',
                                     'gate-port=',
                                     'class=', 'host=', 'server=', 'output=', 'pause=', 'pipe', 'servers',
                                     'sessions',
                                     'repeat=', 'function=', 'append=', 'update=', 'timeout=', 'size=', 'source=',
                                     'id=',
                                     'verbose', 'recursive', 'rotate=', 'errors', 'name='])
        except GetoptError:
            usage()
            exit()

        for o, a in opts:
            if o in ['-m', '--mode']: self.opc_mode = a
            if o in ['-C', '--class']: self.opc_class = a
            if o in ['-n', '--name']: self.client_name = a
            if o in ['-H', '--open-host']: self.open_host = a;  opc_mode = 'open'
            if o in ['-P', '--open-port']: self.open_port = a;  opc_mode = 'open'
            if o in ['-h', '--host']: self.opc_host = a
            if o in ['-s', '--server']: self.opc_server = a

            if o in ['-r', '--read']:self.action= 'read'
            if o in ['-w', '--write']:self.action= 'write'
            if o in ['-l', '--list']:self.action= 'list'
            if o in ['-f', '--flat']:self.action= 'flat'
            if o in ['-p', '--properties']:self.action= 'properties'
            if o in ['-i', '--info']:self.action= 'info'
            if o in ['-q', '--servers']:self.action= 'servers'
            if o in ['-S', '--sessions']:self.action= 'sessions'

            if o in ['-o', '--output']: style = a
            if o in ['-L', '--repeat']: self.repeat_pause = float(a);
            if o in ['-F', '--function']: self.read_function = a;
            if o in ['-z', '--pause']: self.tx_pause = int(a)
            if o in ['-u', '--update']: self.update_rate = int(a)
            if o in ['-t', '--timeout']: self.timeout = int(a)
            if o in ['-g', '--size']: self.group_size = int(a)
            if o in ['-c', '--source']: self.data_source = a
            if o in ['-y', '--id']: self.property_ids = a
            if o in ['-a', '--append']: self.append = a
            if o in ['-x', '--rotate']:self.num_columns = int(a)
            if o in ['-v', '--verbose']: self.verbose = True
            if o in ['-e', '--errors']: self.include_err_msg = True
            if o in ['-R', '--recursive']: self.recursive = True
            if o in ['--pipe']: self.pipe = True

        # Check validity of command line options

        if self.num_columns > 0 and self.style in ('values', 'pairs'):
            print("'%s' style format may not be used with rotate" % self.style)
            exit()

        if self.opc_mode not in ('open', 'dcom'):
            print("'%s' is not a valid protocol mode (options: dcom, open)" %self.opc_mode)
            exit()

        if self.opc_mode == 'dcom' and not win32com_found:
            print("win32com modules required when using DCOM protocol mode (http://pywin32.sourceforge.net/)")
            exit()

        if self.opc_mode == 'open' and not pyro_found:
            print("Pyro module required when using Open protocol mode (http://pyro.sourceforge.net)")
            exit()

        if self.style not in ('table', 'values', 'pairs', 'csv', 'html'):
            print("'%s' is not a valid style format (options: table, values, pairs, csv, html)" % self.style)
            exit()

        if self.read_function not in ('sync', 'async'):
            print("'%s' is not a valid read function (options: sync, async)" % self.read_function)
            exit()
        else:
            sync = (self.read_function == 'sync')

        if self.data_source not in ('cache', 'device', 'hybrid'):
            print("'%s' is not a valid data source mode (options: cache, device, hybrid)" % self.data_source)
            exit()

        if len(argv[1:]) == 0 or argv[1] == '/?' or argv[1] == '--help':
            self.usage()
            exit()

        if self.opc_server == '' and self.action not in ('servers', 'sessions'):
            print('OPC server name missing: use -s option or set OPC_SERVER environment variable')
            exit()

        if self.data_source in (
        'cache', 'hybrid') and self.read_function == 'async' and self.update_rate == None and self.repeat_pause != None:
            self.update_rate = int(self.repeat_pause * 1000.0)
        elif self.update_rate == None:
            self.update_rate = -1

        # Build tag list

        tags = []

        # Tag list passed via standrd input
        if self.pipe:
            try:
                reader = csv.reader(sys.stdin)
                tags_nested = list(reader)
            except KeyboardInterrupt:
                exit()

            tags = [line[0] for line in tags_nested if len(line) > 0]
            if len(tags) == 0:
                print('Input stream must contain ITEMs (one per line)')
                exit()

            elif self.action == 'write':
                try:
                    tag_value_pairs = [(item[0], item[1]) for item in tags_nested]
                except IndexError:
                    print('Write input must be in ITEM,VALUE (CSV) format')
                    exit()

        # Tag list passed via command line arguments
        else:
            for a in args:
                tags.append(a.replace('+', ' '))
            tags_nested = [[tag] for tag in tags]

        if self.action == 'write':
            if len(tags) % 2 == 0:
                tag_value_pairs = [(tags[i], tags[i + 1]) for i in range(0, len(tags), 2)]
            else:
                print('Write arguments must be supplied in ITEM=VALUE or ITEM VALUE format')
                exit()

        if len(append) > 0:
            tags = [t + a for t in tags for a in append.split(',')]

        if property_ids is not None:
            try:
                property_ids = [int(p) for p in property_ids.split(',')]
            except ValueError:
                print('Property ids must be numeric')
                exit()

        if self.actionin ('read', 'write') and not self.pipe and len(tags) == 0:
            self.usage()
            exit()

        # Were only health monitoring "@" tags supplied?

        health_tags = [t for t in tags if t[:1] == '@']
        opc_tags = [t for t in tags if t[:1] != '@']
        if len(health_tags) > 0 and len(opc_tags) == 0:
            health_only = True
        else:
            health_only = False

        # Establish signal handler for keyboard interrupts

        sh = SigHandler()
        signal.signal(signal.SIGINT, sh)
        if os.name == 'nt':
            signal.signal(signal.SIGBREAK, sh)
        signal.signal(signal.SIGTERM, sh)

        # ACTION: List active sessions in OpenOPC service

        if  self.action == 'sessions':
            print('  %-38s %-18s %-18s' % ('Remote Client', 'Start Time', 'Last Transaction'))
            try:
                for guid, host, init_time, tx_time in get_sessions(self.open_host, self.open_port):
                    print('  %-38s %-18s %-18s' % (host, time2str(init_time), time2str(tx_time)))
            except:
                error_msg = sys.exc_info()[1]
                print("Cannot connect to OpenOPC service at %s:%s - %s" % (self.open_host, open_port, error_msg))
            exit()

        # Connect to OpenOPC service (Open mode)

        if self.opc_mode == 'open':
            try:
                opc = open_client(self.open_host,self.open_port)
            except:
                error_msg = sys.exc_info()[1]
                print("Cannot connect to OpenOPC Gateway Service at %s:%s - %s" % (self.open_host,self.open_port, error_msg))
                exit()

        # Dispatch to COM class (DCOM mode)

        else:
            try:
                opc = client(self.opc_class, self.client_name)
            except OPCError as error_msg:
                print("Failed to initialize an OPC Automation Class from the search list '%s' - %s" % (
                self.opc_class, error_msg))
                exit()

        # Connect to OPC server

        if self.action not in ['servers'] and not health_only:
            try:
                self.opc_client.connect(self.opc_server, self.opc_host)
            except OPCError as error_msg:
                if self.opc_mode == 'open': error_msg = error_msg[0]
                print("Connect to OPC server '%s' on '%s' failed - %s" % (self.opc_server, self.opc_host, error_msg))
                exit()

        # Perform requested action...

        start_time = time.time()

        # ACTION: Read Items
        if self.action == 'read':
            opc = self.cli_read(tags)


        # ACTION: Write Items
        elif self.action == 'write':
            self.cli_write(group_size, include_err_msg,self.num_columns, opc, self.opc_mode, start_time, style,
                           tag_value_pairs, tags, tx_pause)

        # ACTION: List Items (Tree Browser)

        elif self.action == 'list':
            self.cli_list(tags)


        # ACTION: List Items (Flat Browser)

        elif self.action == 'flat':
            self.cli_flat(tags)


        # ACTION: Item Properties

        elif self.action == 'properties':
            self.cli_properties(property_ids, tags)


        # ACTION: Server Info

        elif self.action == 'info':
            self.cli_info()


        # ACTION: List Servers

        elif self.action == 'servers':
            self.cli_servers()

        # Disconnect from OPC Server

        try:
            self.opc_client.close()
        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print(error_msg)


    def cli_servers(self):
        try:
            output(rotate(self.opc_client.servers(self.opc_host), self.num_columns), self.style)
        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print("Error getting server list from '%s' - %s" % (self.opc_host, error_msg))

    def cli_info(self):
        try:
            output(rotate(self.opc_client.info(), self.num_columns), self.style)
        except OPCError as error_msg:
            if self.opc_mode == 'open': error_msg = error_msg[0]
            print(error_msg)

    def cli_properties(self, roperty_ids, tags):
        if self.opc_mode == 'open':
            opc_properties = self.opc_client.properties
        else:
            opc_properties = self.opc_client.iproperties
            rotate = irotate
        if property_ids is not None:
            value_idx = 2
        else:
            value_idx = 3
        try:
            output(rotate(opc_properties(tags, property_ids), num_columns, value_idx), style, value_idx)
        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print(error_msg)

    def cli_flat(self, tags):
        try:
            output(self.opc_client.list(tags, flat=True), self.style)
        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print(error_msg)

    def cli_list(self, recursive, style, tags):
        if self.opc_mode == 'open':
            opc_list = self.opc_client.list
        else:
            opc_list = self.opc_client.ilist
            rotate = irotate
        try:
            output(rotate(opc_list(tags, recursive=recursive), num_columns), style)
        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print(error_msg)

    def cli_write(self, group_size, include_err_msg, start_time, tag_value_pairs,
                  tags, tx_pause):
        if group_size and len(tags) > group_size and self.opc_mode == 'dcom':
            opc_write = self.opc_client.iwrite
            rotate = irotate
        else:
            opc_write = self.opc_client.write
        try:
            status = output(rotate(opc_write(tag_value_pairs,
                                             size=self.group_size,
                                             pause=self.tx_pause,
                                             include_error=self.include_err_msg),
                                   self.num_columns), self.style)

        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print(error_msg)
        if self.style == 'table' and self.num_columns == 0:
            success = len([s for s in status if s[1] != 'Error'])
            print('\nWrote %d of %d items (%.2f seconds)' % (
                success, len(tag_value_pairs), time.time() - start_time)
                  )

    def cli_read(self, opc, opc_host, opc_server,
                 repeat_pause, sh, start_time, style,  tags,
                  verbose):


        if self.group_size and len(tags) > self.group_size and self.opc_mode == 'dcom':
            opc_read = self.opc_client.iread
            rotate = irotate
        else:
            opc_read = self.opc_client.read
        if verbose:
            def trace(msg):
                print(msg)

            self.opc_client.set_trace(trace)
        success_count = 0
        total_count = 0
        com_connected = True
        pyro_connected = True
        while not sh.signaled:

            try:
                if not pyro_connected:
                    opc = open_client(self.open_host, self.open_port)
                    self.opc_client.connect(opc_server, opc_host)
                    opc_read = self.opc_client.read
                    pyro_connected = True
                    com_connected = True

                if not com_connected:
                    self.opc_client.connect(opc_server, opc_host)
                    com_connected = True

                status = output(rotate(opc_read(tags,
                                                group='test',
                                                size=self.group_size,
                                                pause=self.tx_pause,
                                                source=self.data_source,
                                                update=self.update_rate,
                                                timeout=self.timeout,
                                                sync=self.sync,
                                                include_error=self.include_err_msg),
                                       self.num_columns), self.style)

            except TimeoutError as error_msg:
                if self.opc_mode == 'open':
                    error_msg = error_msg[0]
                print(error_msg)

                success = False

            except OPCError as error_msg:
                if self.opc_mode == 'open':
                    error_msg = error_msg[0]
                print(error_msg)

                success = False

                if self.opc_client.ping():
                    com_connected = True
                else:
                    com_connected = False

            except (Pyro.errors.ConnectionClosedError, Pyro.errors.ProtocolError) as error_msg:
                print('Gateway Service: %s' % error_msg)
                success = False
                pyro_connected = False

            except TypeError as error_msg:
                if self.opc_mode == 'open':
                    error_msg = error_msg[0]
                print(error_msg)
                break

            except IOError:
                self.opc_client.close()
                exit()

            else:
                success = True

            if success and self.self.num_columns == 0:
                success_count += len([s for s in status if s[2] != 'Error'])
                total_count += len(status)

            if repeat_pause is not None:
                try:
                    time.sleep(repeat_pause)
                except IOError:
                    break
            else:
                break
        if style == 'table' and self.num_columns == 0:
            print()
            '\nRead %d of %d items (%.2f seconds)' % (success_count, total_count, time.time() - start_time)
        try:
            self.opc_client.remove('test')
        except OPCError as error_msg:
            if self.opc_mode == 'open':
                error_msg = error_msg[0]
            print(error_msg)
        return opc

    def usage(self):
        """
        Print comand line usage summary
        """
        print(
            """
         
            OpenOPC Command Line Client', OpenOPC.__version__
            Copyright (c) 2007-2015 Barry Barnreiter (barrybb@gmail.com)'
            
            Usage:  opc [OPTIONS] [ACTION] [ITEM|PATH...]'
         
            
            Actions:'
              -r, --read                 Read ITEM values (default action)
              -w, --write                Write values to ITEMs (use ITEM=VALUE)'
              -p, --properties           View properties of ITEMs'
              -l, --list                 List items at specified PATHs (tree browser)'
              -f, --flat                 List all ITEM names (flat browser)'
              -i, --info                 Display OPC server information'
              -q, --servers              Query list of available OPC servers'
              -S, --sessions             List sessions in OpenOPC Gateway Service'
            
            Options:'
              -m MODE, --mode=MODE       Protocol MODE (dcom, open) (default: OPC_MODE)
              -C CLASS,--class=CLASS     OPC Automation CLASS (default: OPC_CLASS)
              -n NAME, --name=NAME       Set OPC Client NAME (default: OPC_CLIENT)
              -h HOST, --host=HOST       DCOM OPC HOST (default: OPC_HOST)'
              -s SERV, --server=SERVER   DCOM OPC SERVER (default: OPC_SERVER)'
              -H HOST, --gate-host=HOST  OpenOPC Gateway HOST (default: OPC_GATE_HOST)'
              -P PORT, --gate-port=PORT  OpenOPC Gateway PORT (default: OPC_GATE_PORT)'
            
              -F FUNC, --function=FUNC   Read FUNCTION to use (sync, async)'
              -c SRC,  --source=SOURCE   Set data SOURCE for reads (cache, device, hybrid)'
              -g SIZE, --size=SIZE       Group tags into SIZE items per transaction'
              -z MSEC, --pause=MSEC      Sleep MSEC milliseconds between transactions'
              -u MSEC, --update=MSEC     Set update rate for group to MSEC milliseconds'
              -t MSEC, --timeout=MSEC    Set read timeout to MSEC mulliseconds'
            
              -o FMT,  --output=FORMAT   Output FORMAT (table, values, pairs, csv, html)'
              -L SEC,  --repeat=SEC      Loop ACTION every SEC seconds until stopped'
              -y ID,   --id=ID,...       Retrieve only specific Property IDs'
              -a STR,  --append=STR,...  Append STRINGS to each input item name'
              -x N     --rotate=N        Rotate output orientation in groups of N values'
              -v,      --verbose         Verbose mode showing all OPC function calls'
              -e,      --errors          Include descriptive error message strings'
              -R,      --recursive       List items recursively when browsing tree'
              -,       --pipe            Pipe item/value list from standard input'
            """)


# Helper class for handling signals (i.e. Ctrl-C)


# FUNCTION: Iterable version of rotate()


if __name__ == '__main__':
    main()
