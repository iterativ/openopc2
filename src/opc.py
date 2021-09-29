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
import OpenOPC

try:
   import Pyro
except ImportError:
   pyro_found = False
else:
   pyro_found = True

# Common function aliases

write = sys.stdout.write

# Initialize default settings

if os.name == 'nt':
   opc_mode = 'dcom'
else:
   opc_mode = 'open'

opc_class = OpenOPC.OPC_CLASS
client_name = OpenOPC.OPC_CLIENT
opc_host = 'localhost'
opc_server = OpenOPC.OPC_SERVER
open_host = 'localhost'
open_port = 7766

action = 'read'
style = 'table'
append = ''
num_columns = 0
pipe = False
verbose = False
recursive = False
read_function = 'async'
data_source = 'hybrid'
group_size = None
update_rate = None
timeout = 5000
tx_pause = 0
repeat = 1
repeat_pause = None
property_ids = None
include_err_msg = False

if environ.has_key('OPC_MODE'):         opc_mode = environ['OPC_MODE']
if environ.has_key('OPC_CLASS'):        opc_class = environ['OPC_CLASS']
if environ.has_key('OPC_CLIENT'):       client_name = environ['OPC_CLIENT']
if environ.has_key('OPC_HOST'):         opc_host = environ['OPC_HOST']
if environ.has_key('OPC_SERVER'):       opc_server = environ['OPC_SERVER']
if environ.has_key('OPC_GATE_HOST'):    open_host = environ['OPC_GATE_HOST']
if environ.has_key('OPC_GATE_PORT'):    open_port = environ['OPC_GATE_PORT']
if environ.has_key('OPC_TIMEOUT'):      timeout = int(environ['OPC_TIMEOUT'])

# FUNCTION: Print comand line usage summary

def usage():
   print 'OpenOPC Command Line Client', OpenOPC.__version__
   print 'Copyright (c) 2007-2015 Barry Barnreiter (barrybb@gmail.com)'
   print ''
   print 'Usage:  opc [OPTIONS] [ACTION] [ITEM|PATH...]'
   print ''
   print 'Actions:'
   print '  -r, --read                 Read ITEM values (default action)'
   print '  -w, --write                Write values to ITEMs (use ITEM=VALUE)'
   print '  -p, --properties           View properties of ITEMs'
   print '  -l, --list                 List items at specified PATHs (tree browser)'
   print '  -f, --flat                 List all ITEM names (flat browser)'
   print '  -i, --info                 Display OPC server information'
   print '  -q, --servers              Query list of available OPC servers'
   print '  -S, --sessions             List sessions in OpenOPC Gateway Service'
   print ''
   print 'Options:'
   print '  -m MODE, --mode=MODE       Protocol MODE (dcom, open) (default: OPC_MODE)'
   print '  -C CLASS,--class=CLASS     OPC Automation CLASS (default: OPC_CLASS)'
   print '  -n NAME, --name=NAME       Set OPC Client NAME (default: OPC_CLIENT)'
   print '  -h HOST, --host=HOST       DCOM OPC HOST (default: OPC_HOST)'
   print '  -s SERV, --server=SERVER   DCOM OPC SERVER (default: OPC_SERVER)'
   print '  -H HOST, --gate-host=HOST  OpenOPC Gateway HOST (default: OPC_GATE_HOST)'
   print '  -P PORT, --gate-port=PORT  OpenOPC Gateway PORT (default: OPC_GATE_PORT)'
   print ''
   print '  -F FUNC, --function=FUNC   Read FUNCTION to use (sync, async)'
   print '  -c SRC,  --source=SOURCE   Set data SOURCE for reads (cache, device, hybrid)'
   print '  -g SIZE, --size=SIZE       Group tags into SIZE items per transaction'
   print '  -z MSEC, --pause=MSEC      Sleep MSEC milliseconds between transactions'
   print '  -u MSEC, --update=MSEC     Set update rate for group to MSEC milliseconds'
   print '  -t MSEC, --timeout=MSEC    Set read timeout to MSEC mulliseconds'
   print ''
   print '  -o FMT,  --output=FORMAT   Output FORMAT (table, values, pairs, csv, html)'
   print '  -L SEC,  --repeat=SEC      Loop ACTION every SEC seconds until stopped'
   print '  -y ID,   --id=ID,...       Retrieve only specific Property IDs'
   print '  -a STR,  --append=STR,...  Append STRINGS to each input item name'
   print '  -x N     --rotate=N        Rotate output orientation in groups of N values'
   print '  -v,      --verbose         Verbose mode showing all OPC function calls'
   print '  -e,      --errors          Include descriptive error message strings'
   print '  -R,      --recursive       List items recursively when browsing tree'
   print '  -,       --pipe            Pipe item/value list from standard input'

# Helper class for handling signals (i.e. Ctrl-C)

class SigHandler:
  def __init__(self):
      self.signaled = 0
      self.sn = None
  def __call__(self, sn, sf):
      self.sn = sn 
      self.signaled += 1

# FUNCTION: Iterable version of rotate()

def irotate(data, num_columns, value_idx = 1):
   if num_columns == 0:
      for row in data: yield row
      return
   
   new_row = []

   for i, row in enumerate(data):
      if type(row) not in (types.ListType, types.TupleType):
         value_idx = 0
         row = [row]

      new_row.append(row[value_idx])
      if (i + 1) % num_columns == 0:
         yield new_row
         new_row = []

   if len(new_row) > 0:
      yield new_row

# FUNCTION: Rotate the values of every N rows to form N columns

def rotate(data, num_columns, value_idx = 1):
   return list(irotate(data, num_columns, value_idx))

# FUNCTION: Print output in the specified style from a list of data
   
def output(data, style = 'table', value_idx = 1):
   global write
   name_idx = 0

   # Cast value to a stirng (trap Unicode errors)
   def to_str(value):
      try:
         if type(value) == types.FloatType:
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
   elif type(data) in (types.ListType, types.TupleType):
      generator = False
      
      if len(data) == 0: return

      if type(data[0]) not in (types.ListType, types.TupleType):
         data = [[e] for e in data]
         
      if style == 'table' or style == '':
         pad_length = []
         num_columns = len(data[0])
         for i in range(num_columns-1):
            pad_length.append(len(max([to_str(row[i]) for row in data], key=len)) + 5)
         pad_length.append(0)
   else:
      raise TypeError, "output(): 'data' parameter must be a list or a generator"

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
            if type(row) not in (types.ListType, types.TupleType):
               row = [row]

            num_columns = len(row)

            # Allow columns widths to always grow wider, but never shrink.
            # Unfortunetly we won't know the required width until the generator is finished!
            for k in range(num_columns-1):
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
               if j == len(row)-1: write('  </tr>')
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

# Parse command line arguments

if argv.count('-') > 0:
   argv[argv.index('-')] = '--pipe'
   pipe = True

try:
   opts, args = gnu_getopt(argv[1:], 'rwlpfiqRSevx:m:C:H:P:c:h:s:L:F:z:o:a:u:t:g:y:n:', ['read','write','list','properties','flat','info','mode=','gate-host=','gate-port=','class=','host=','server=','output=','pause=','pipe','servers','sessions','repeat=','function=','append=','update=','timeout=','size=','source=','id=','verbose','recursive','rotate=','errors','name='])
except GetoptError:
   usage()
   exit()   

for o, a in opts:
   if o in ['-m', '--mode']       : opc_mode = a
   if o in ['-C', '--class']      : opc_class = a
   if o in ['-n', '--name']       : client_name = a
   if o in ['-H', '--open-host']  : open_host = a;  opc_mode = 'open' 
   if o in ['-P', '--open-port']  : open_port = a;  opc_mode = 'open'
   if o in ['-h', '--host']       : opc_host = a
   if o in ['-s', '--server']     : opc_server = a
   
   if o in ['-r', '--read']       : action = 'read'
   if o in ['-w', '--write']      : action = 'write'
   if o in ['-l', '--list']       : action = 'list'
   if o in ['-f', '--flat']       : action = 'flat'
   if o in ['-p', '--properties'] : action = 'properties'
   if o in ['-i', '--info']       : action = 'info'
   if o in ['-q', '--servers']    : action = 'servers'
   if o in ['-S', '--sessions']   : action = 'sessions'

   if o in ['-o', '--output']     : style = a
   if o in ['-L', '--repeat']     : repeat_pause = float(a);
   if o in ['-F', '--function']   : read_function = a;
   if o in ['-z', '--pause']      : tx_pause = int(a)
   if o in ['-u', '--update']     : update_rate = int(a)
   if o in ['-t', '--timeout']    : timeout = int(a)
   if o in ['-g', '--size']       : group_size = int(a)
   if o in ['-c', '--source']     : data_source = a
   if o in ['-y', '--id']         : property_ids = a
   if o in ['-a', '--append']     : append = a
   if o in ['-x', '--rotate']     : num_columns = int(a)
   if o in ['-v', '--verbose']    : verbose = True
   if o in ['-e', '--errors']     : include_err_msg = True
   if o in ['-R', '--recursive']  : recursive = True
   if o in ['--pipe']             : pipe = True

# Check validity of command line options

if num_columns > 0 and style in ('values', 'pairs'):
   print "'%s' style format may not be used with rotate" % style
   exit()
   
if opc_mode not in ('open', 'dcom'):
   print "'%s' is not a valid protocol mode (options: dcom, open)" % opc_mode
   exit()

if opc_mode == 'dcom' and not OpenOPC.win32com_found:
   print "win32com modules required when using DCOM protocol mode (http://pywin32.sourceforge.net/)"
   exit()

if opc_mode == 'open' and not pyro_found:
   print "Pyro module required when using Open protocol mode (http://pyro.sourceforge.net)"
   exit()

if style not in ('table', 'values', 'pairs', 'csv', 'html'):
   print "'%s' is not a valid style format (options: table, values, pairs, csv, html)" % style
   exit()

if read_function not in ('sync', 'async'):
   print "'%s' is not a valid read function (options: sync, async)" % read_function
   exit()
else:
   sync = (read_function == 'sync')
   
if data_source not in ('cache', 'device', 'hybrid'):
   print "'%s' is not a valid data source mode (options: cache, device, hybrid)" % data_source
   exit()

if len(argv[1:]) == 0 or argv[1] == '/?' or argv[1] == '--help':
   usage()
   exit()

if opc_server == '' and action not in ('servers', 'sessions'):
   print 'OPC server name missing: use -s option or set OPC_SERVER environment variable'
   exit()

if data_source in ('cache', 'hybrid') and read_function == 'async' and update_rate == None and repeat_pause != None:
   update_rate = int(repeat_pause * 1000.0)
elif update_rate == None:
   update_rate = -1

# Build tag list

tags = []

# Tag list passed via standrd input
if pipe:
   try:
      reader = csv.reader(sys.stdin)
      tags_nested = list(reader)
   except KeyboardInterrupt:
      exit()

   tags = [line[0] for line in tags_nested if len(line) > 0]
   if len(tags) == 0:
      print 'Input stream must contain ITEMs (one per line)'
      exit()
      
   if action == 'write':
      try:
         tag_value_pairs = [(item[0], item[1]) for item in tags_nested]
      except IndexError:
         print 'Write input must be in ITEM,VALUE (CSV) format'
         exit()

# Tag list passed via command line arguments
else:
   for a in args:
      tags.append(a.replace('+', ' '))
   tags_nested = [[tag] for tag in tags]

   if action == 'write':
      if len(tags) % 2 == 0:
         tag_value_pairs = [(tags[i], tags[i+1]) for i in range(0, len(tags), 2)]
      elif len([t for t in tags if t.find('=') != -1]) == len(tags):
         tag_value_pairs = [t.split('=') for t in tags]
      else:
         print 'Write arguments must be supplied in ITEM=VALUE or ITEM VALUE format'
         exit()

if len(append) > 0:
   tags = [t + a  for t in tags for a in append.split(',')]

if property_ids != None:
   try:
      property_ids = [int(p) for p in property_ids.split(',')]
   except ValueError:
      print 'Property ids must be numeric'
      exit()
   
if action in ('read','write') and not pipe and len(tags) == 0:
   usage()
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
signal.signal(signal.SIGINT,sh)
if os.name == 'nt':
    signal.signal(signal.SIGBREAK,sh)
signal.signal(signal.SIGTERM,sh)

# ACTION: List active sessions in OpenOPC service

if action == 'sessions':
   print '  %-38s %-18s %-18s' % ('Remote Client', 'Start Time', 'Last Transaction')
   try:
      for guid, host, init_time, tx_time in OpenOPC.get_sessions(open_host, open_port):
         print '  %-38s %-18s %-18s'  % (host, time2str(init_time), time2str(tx_time))
   except:
      error_msg = sys.exc_info()[1]
      print "Cannot connect to OpenOPC service at %s:%s - %s" % (open_host, open_port, error_msg)
   exit()
   
# Connect to OpenOPC service (Open mode)

if opc_mode == 'open':
   try:
      opc = OpenOPC.open_client(open_host, open_port)
   except:
      error_msg = sys.exc_info()[1]
      print "Cannot connect to OpenOPC Gateway Service at %s:%s - %s" % (open_host, open_port, error_msg)
      exit()

# Dispatch to COM class (DCOM mode)

else:
   try:
      opc = OpenOPC.client(opc_class, client_name)
   except OpenOPC.OPCError, error_msg:
      print "Failed to initialize an OPC Automation Class from the search list '%s' - %s" % (opc_class, error_msg)
      exit()

# Connect to OPC server

if action not in ['servers'] and not health_only:
   try:
      opc.connect(opc_server, opc_host)
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print "Connect to OPC server '%s' on '%s' failed - %s" % (opc_server, opc_host, error_msg)
      exit()

# Perform requested action...

start_time = time.time()

# ACTION: Read Items

if action == 'read':
   if group_size and len(tags) > group_size and opc_mode == 'dcom':
      opc_read = opc.iread
      rotate = irotate
   else:
      opc_read = opc.read
            
   if verbose:
      def trace(msg): print msg
      opc.set_trace(trace)

   success_count = 0
   total_count = 0
   com_connected = True
   pyro_connected = True

   while not sh.signaled:

      try:
         if not pyro_connected:
            opc = OpenOPC.open_client(open_host, open_port)
            opc.connect(opc_server, opc_host)
            opc_read = opc.read
            pyro_connected = True
            com_connected = True

         if not com_connected:
            opc.connect(opc_server, opc_host)
            com_connected = True

         status = output(rotate(opc_read(tags,
                                  group='test',
                                  size=group_size,
                                  pause=tx_pause,
                                  source=data_source,
                                  update=update_rate,
                                  timeout=timeout,
                                  sync=sync,
                                  include_error=include_err_msg),
                        num_columns), style)
                        
      except OpenOPC.TimeoutError, error_msg:
         if opc_mode == 'open': error_msg = error_msg[0]
         print error_msg
         success = False

      except OpenOPC.OPCError, error_msg:
         if opc_mode == 'open': error_msg = error_msg[0]
         print error_msg
         success = False
 
         if opc.ping():
            com_connected = True
         else:
            com_connected = False
            
      except (Pyro.errors.ConnectionClosedError, Pyro.errors.ProtocolError), error_msg:
         print 'Gateway Service: %s' % error_msg
         success = False
         pyro_connected = False

      except TypeError, error_msg:
         if opc_mode == 'open': error_msg = error_msg[0]
         print error_msg
         break

      except IOError:
         opc.close()
         exit()
            
      else:
         success = True

      if success and num_columns == 0:
         success_count += len([s for s in status if s[2] != 'Error'])
         total_count += len(status)

      if repeat_pause != None:
         try:
            time.sleep(repeat_pause)
         except IOError:
            break
      else:
         break

   if style == 'table' and num_columns == 0:
      print '\nRead %d of %d items (%.2f seconds)' % (success_count, total_count, time.time() - start_time)

   try:
      opc.remove('test')
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print error_msg
         
# ACTION: Write Items

elif action == 'write':
   if group_size and len(tags) > group_size and opc_mode == 'dcom':
      opc_write = opc.iwrite
      rotate = irotate
   else:
      opc_write = opc.write

   try:
      status = output(rotate(opc_write(tag_value_pairs,
                                size=group_size,
                                pause=tx_pause,
                                include_error=include_err_msg),
                         num_columns), style)

   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print error_msg

   if style == 'table' and num_columns == 0:
      success = len([s for s in status if s[1] != 'Error'])
      print '\nWrote %d of %d items (%.2f seconds)' % (success, len(tag_value_pairs), time.time() - start_time)

# ACTION: List Items (Tree Browser)
   
elif action == 'list':
   if opc_mode == 'open':
      opc_list = opc.list
   else:
      opc_list = opc.ilist
      rotate = irotate

   try:
      output(rotate(opc_list(tags, recursive=recursive), num_columns), style)
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print error_msg

# ACTION: List Items (Flat Browser)
   
elif action == 'flat':
   try:
      output(opc.list(tags, flat=True), style)
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print error_msg

# ACTION: Item Properties

elif action == 'properties':
   if opc_mode == 'open':
      opc_properties = opc.properties
   else:
      opc_properties = opc.iproperties
      rotate = irotate

   if property_ids != None:
      value_idx = 2
   else:
      value_idx = 3

   try:
      output(rotate(opc_properties(tags, property_ids), num_columns, value_idx), style, value_idx)
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print error_msg

# ACTION: Server Info

elif action == 'info':
   try:
      output(rotate(opc.info(), num_columns), style)
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print error_msg

# ACTION: List Servers

elif action == 'servers':
   try:
      output(rotate(opc.servers(opc_host), num_columns), style)
   except OpenOPC.OPCError, error_msg:
      if opc_mode == 'open': error_msg = error_msg[0]
      print "Error getting server list from '%s' - %s" % (opc_host, error_msg)

# Disconnect from OPC Server

try:
   opc.close()
except OpenOPC.OPCError, error_msg:
   if opc_mode == 'open': error_msg = error_msg[0]
   print error_msg
