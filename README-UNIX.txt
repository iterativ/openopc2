Note that when using OpenOPC on a non-Windows system you must be running the
OpenOPC Gateway Service (OpenOPCService.py) on a Windows box somewhere on
your network.   The OpenOPC Gateway Service then acts as a proxy for all
your OPC calls.

For example, if your Windows node which is running the Gateway Service
had the IP address of 192.168.1.20 then you would use the OpenOPC command
line client like this....

opc.py -H 192.168.1.20 -s Matrikon.OPC.Simulation -r Random.Real4

Or when using the OpenOPC.py module inside your own Python code, you
would create your opc object like this....

import OpenOPC
opc = opc.open_client('192.168.1.20')
opc.connect('Matrikon.OPC.Simulation')

The above examples all assume that the OPC server and the OpenOPC
Gateway Service are both installed on the same box.  This is the
recommended configuration in order to avoid any DCOM security issues.

If you downloaded this source code only version of OpenOPC for Unix, it
is recommended you also download one of the win32 labeld downloads
and use the pre-complied OpenOPCService.exe executible for Windows.
This file is self contained and does not require that Python
be installed on your Windows box.
