OpenOPC for Python 1.2.0
Copyright (c) 2008-2012 by Barry Barnreiter (barry_b@users.sourceforge.net)

http://openopc.sourceforge.net/


Post installation
-----------------

Please go through the following post installation steps and functional
checks to verify your installation of OpenOPC for Python is working
correctly.

1. Get a listing of the available OPC servers on your computer by
going to the command prompt and entering:

opc -q

2. Set your prefered OPC server as the default by setting the system
wide enviornment variable OPC_SERVER.  (On Windows you can do this
by going to Control Panel > System > Advanced > Environment Variables)

OPC_SERVER=Matrikon.OPC.Simulation

3. Test your Win32 COM connection to the OPC server by entering the
following at the command prompt:

opc -i

4. Test to see if the OpenOPC Gateway Service is functioning by
entering:

opc -m open -i

5. Test some of the other commands available using the OPC Command
Line Client.  To get started, try entering the opc command without
any arguments in order to see the help page:

opc

To read an item from your OPC server, just include the item name as
one of your arguments.  For example, if you're using Matrikon's
Simulation server you could do:

opc Random.Int4

To read items from a specific OPC server you have installed,
include the -s switch followed by the OPC server name.  For
example:

opc -s Matrikon.OPC.Simulation Random.Int4

If you experience any unexpected errors during these tests, please
check the FAQ on http://openopc.sourceforge.net for additional help.

If after reading through the FAQ you still require additional help,
then the author of this package would be happy to assist you via
e-mail.  Please see the project website for current contact
information.



Software Developers
-------------------

If you elected to install the OpenOPC Development library during the
installation process, then you'll need to also download and install
the following packages in order to develop your own Python programs
which use the OpenOPC library:

1. Python 2.7.x
   http://www.python.org/download/

2. Python for Windows Extensions (pywin32)
   http://sourceforge.net/projects/pywin32/

3. Pyro 3.15
   http://irmen.home.xs4all.nl/pyro3/

Of course, Python is necessary on all platforms.  However the other
packages may be optional depending on your configuration:

1. Win32 platform, using the OpenOPC Gateway Service

Pywin32:  optional
Pyro:     required

2. Win32 platform, talking to OPC Servers directly using COM/DCOM

Pywin32:  required
Pyro:     optional

3. Non-Windows platform (use of Gateway Service is manditory)

Pywin32:  not applicable
Pyro:     required

In order to get the most from the OpenOPC package, Windows developers
are encouraged to install both Pywin32 and Pyro.  Using Pyro to talk to
the Gateway Service provides a quick and easy method for bypassing the
DCOM security nightmares which are all too common when using OPC.


Documentation
-------------

A PDF manual for OpenOPC is included in this installation inside the
"doc" folder.   Users are encouraged to also look at the OpenOPC web
site for additional usage examples that may not be contained in the
manual.


Technical Support
-----------------

If you have any questions, bug reports, or suggestions for improvements
please feel free to contact the author at:

barry_b@users.sourceforge.net

While I cannot always guarantee a quick response, I eventually respond
to all e-mails and will do my best to slove any issues which are discovered.

Thanks for using OpenOPC for Python!
