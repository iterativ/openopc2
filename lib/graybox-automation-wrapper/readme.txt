OPC DATA ACCESS AUTO
--------------------

The fundamental design goal is that this interface is intended to work as a
'wrapper' for existing OPC Data Access Custom Interface Servers providing an
automation friendly mechanism to the functionality provided by the custom
interface.

The automation interface provides nearly all of the functionality of the
required and optional Interfaces in the OPC Data Access Custom Interface.
If the OPC Data Access Custom server supports the interface, the functions and
properties at the automation level will work. Automation interfaces generally
do not support optional capabilities in the same way that the custom interface
does. If the underlying custom interface omits some optional functionality
then the corresponding automation functions and properties will exhibit some
reasonable default behavior.


AUTOMATION WRAPPER
------------------

Graybox OPC Automation Wrapper is a DLL-module, in which all of the needed
OLE-objects are implemented. After registering this module, you will be able
to use any OPC Data Access Server with almost any OLE enabled programming
language (Visual Basic, VBA, etc).


USAGE
-----

Do the following steps to install the Wrapper.
- copy gbda_aut.dll to Windows\System32 folder;
- register this module - enter regsvr32 gbda_aut.dll in the command line.

To remove Graybox OPC Automation Wrapper from your system's registry enter
regsvr32 gbda_aut.dll -u.


LICENSE
-------

Graybox OPC Automation Wrapper is freeware. You can use it and redistibute it
freely. There are no limitation for this product.

No warranties. Graybox Software expressly disclaims any warranty for this
software. To the maximum extent permitted by applicable law, the software and
any related documentation is provided "as is" without warranties or conditions
of any kind, either express or implied, including, without limitation, the
implied warranties or conditions of merchantability, fitness for a particular
purpose, or noninfringement. The entire risk arising out of use or performance
of this software remains with you.


CONTACTS
--------

Check out a newer version of this product and our other products on
http:\\gray-box.net
