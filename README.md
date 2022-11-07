<p align="center">
<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/open-opc.png" alt="LinuxSetup" width="700"/>
</p>


[![PyPI version](https://badge.fury.io/py/openopc2.svg)](https://badge.fury.io/py/openopc2)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openopc2)



**OpenOPC 2**  is a Python Library for OPC DA. It is Open source and free for everyone. It allows you to use
[OPC Classic](https://opcfoundation.org/about/opc-technologies/opc-classic/) (OPC Data Access) in 
modern Python environments. OPC Classic is a pure Windows technology by design, but this library includes a Gateway Server
that lets you use OPC Classic on any architecture (Linux, MacOS, Windows, Docker). So this Library creates a gateway 
between 2022 and the late 90ties. Like cruising into the sunset with Marty McFly in a Tesla. 

OpenOPC 2 is based on the OpenOPC Library that was initially created by Barry Barnleitner and hosted on Source Forge, but
It was completely refactorerd and migrated to Python 3.8+


# 🔥 Features

* An OpenOPC Gateway Service (a Windows service providing remote access 
to the OpenOPC library, which is useful to avoid DCOM issues).
* Command Line Interface (CLI)
* Enables you to use OPC Classic with any Platform
* CLI and Gateway are independent Executables that do not require Python
* A system check module (allows you to check the health of your system)
* A free OPC automation wrapper (required DLL file).
* General documentation with updated procedures (this file).

# 🐍 OpenOPC vs OpenOPC 2

Open OPC 2 is based on OpenOPC and should be seen as a successor. If you already have an application that is based on 
OpenOPC, you can migrate with a minimal effort. Our main motivation to build this new version was to improve the developer
experience and create a base for other developers that is easier to maintain, test and work with...

* Simpler installation
* Mostly the same api (but we take the freedom to not be compatible)
* No memory leak in the OpenOpcService 🎉
* Python 3.8+ (tested with 3.10)
* Typings 
* Pyro5, increased security
* We added tests 😎
* Refactoring for increased readablity
* Nicer CLI
* Pipy Package 



# 🚀 Getting started
##  Windows local installation

The quickest way to start is the cli application. Start your OPC server and use the openopc2.exe cli application for test (no python
installation required). 





Now you know that your OPC server is talking to OpenOPC 2. Then lets get started with python. If you use OpenOPC 2 with 
Python in windows directly you are **limited to a 32bit Python** installattion. This is because the ddls of OPC are 32bit.
If you prefere working with a 64bit Python version you can simply use the With OpenOPC Gateway. 

<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/WindowsSetup.png" alt="WindowsSetup" width="400"/>


```console
pip install openopc2
openopc2 --install
python -m openopc2 servers
```



## Multi plattform installation
One of the main benefits of OpenOPC 2 ist the OpenOPC gateway. This enables you to use any modern platform for 
developting your application. Start the OpenOPC service in the Windows environment where the OPC server is running. 
The Service starts a server (Pyro5) that lets you use the OpenOPC2 OpcDaClient on another machine. Due to the magic of
Pyro (Python Remote Objects) the developer experience and usage of the Library remains the same as if you worke int the 
local Windows setup. 



<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/LinuxSetup.png" alt="LinuxSetup" width="700"/>

On the Windows Machine open the console as administator. 

```shell
openopc --install
openopcservice install
openopcservice start
```

On your Linux machine
```
pip install openopc2
openopc2 --install`
```

python
```python
from openopc2.da_client import OpcDaClient



```

# ⚙️ Configuration 

The configuration of the OpenOpc 2 libray and the OpenOpcGateway is done via environment variables. To initiate them,
simply run:

```shell
OpenOPC install 
```

```
OPC_CLASS=Matrikon.OPC.Automation;Graybox.OPC.DAWrapper;HSCOPC.Automation;RSI.OPCAutomation;OPC.Automation
OPC_CLIENT=OpenOPC
OPC_GATE_HOST=192.168.1.96    # IMPORTANT: Replace with your IP address
OPC_GATE_PORT=7766
OPC_HOST=localhost
OPC_MODE=dcom
OPC_SERVER=Hci.TPNServer;HwHsc.OPCServer;opc.deltav.1;AIM.OPC.1;Yokogawa.ExaopcDAEXQ.1;OSI.DA.1;OPC.PHDServerDA.1;Aspen.Infoplus21_DA.1;National Instruments.OPCLabVIEW;RSLinx OPC Server;KEPware.KEPServerEx.V4;Matrikon.OPC.Simulation;Prosys.OPC.Simulation
```

* If they are not set, open a command prompt window to do that by 
typing:

```
C:\>set ENV_VAR=VALUE
C:\>set OPC_GATE_HOST=172.16.4.22    # this is an example
```

* Make sure the firewall is allowed to keep the port 7766 open. If in 
doubt, and you're doing a quick test, just turn off your firewall 
completely.

* For easy testing, make sure an OPC server is installed in your Windows 
box (i.e. Matrikon OPC Simulation Server).

* The work environment for testing these changes was a remote MacOs with Window10 64bit host and the Matrikon simulation
server. 

* Register the OPC automation wrapper ( `gbda_aut.dll` ) by typing this 
in the command line:

```shell
C:\openopc2\lib>regsvr32 gbda_aut.dll
```

* If, for any reason, you want to uninstall this file and remove it from 
your system registry later, type this in the command line:

```shell
C:\openopc2\lib>regsvr32 gbda_aut.dll -u
```


# CLI

The CLI (Command Line Interface) lets you use OpenOPC2 in the shell and offers you a quick way to explore your opc server
and the OpenOPC DA client without the need of writing Python code.

The documentation of the CLI can be found [here](CLI.md)

<p>
<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/cli_server-info.png" alt="WindowsSetup" width="400"/>
</p>

<p>
<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/cli_read.png" alt="WindowsSetup" width="400"/>
</p>


<p>
<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/cli_write.png" alt="WindowsSetup" width="400"/>
</p>


<p>
<img src="https://github.com/iterativ/openopc2/raw/develop/doc/assets/cli_properties.png" alt="WindowsSetup" width="400"/>
</p>



# OpenOPC Gateway

This task can be completed from one of two ways (make sure to have it 
installed first):

* By clicking the `Start` link on the "OpenOPC Gateway Service" from the 
"Services" window (Start -> Control Panel -> System and Security -> 
Administrative Tools).
* By running the `net start SERVICE` command like this:

```shell
C:\openopc2\bin> zzzOpenOPCService
```

* If you have problems starting the service, you can also try to start 
this in "debug" mode:

```shell
C:\openopc2\src>python OpenOPCService.py debug
```



```shell
C:\openopc2\>net stop zzzOpenOPCService
```

### Configure the way the OpenOPC Gateway Service starts

If you are going to use this service frequently, it would be better to 
configure it to start in "automatic" mode. To do this:

* Select the "OpenOPC Gateway Service" from the "Services" window 
(Start -> Control Panel -> System and Security -> Administrative Tools).
* Right-click and choose "Properties".
* Change the startup mode to "Automatic". Click "Apply" and "OK" 
buttons.
* Start the service (if not already started).




## 🙏 Credits

OpenOPC 2 is based on the OpenOPC python library that was originally created by Barry Barnleitner and its many Forks on
Github. Without the great work of all the contributors, this would not be possible. Contribution is open for everyone. 

The authors of the var package are:


| Years     |      | Name                | User |
|-----------|------|---------------------|------|
| 2008-2012 | 🇺🇸 | Barry Barnreiter    | barry_b@users.sourceforge.net |
| 2014      | 🇷🇺 | Anton D. Kachalov   | barry_b@users.sourceforge.net |
| 2017      | 🇻🇪 | José A. Maita       | jose.a.maita@gmail.com|
| 2022      | 🇨🇭 | Lorenz Padberg      | renzop |
| 2022      | 🇨🇭 | Elia Bieri          | eliabieri |




## 📜 License

This software is licensed under the terms of the GNU GPL v2 license plus 
a special linking exception for portions of the package. This license is 
available in the `LICENSE.txt` file.
