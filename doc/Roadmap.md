Version 1.5

Goals:

- Create a maintainable repository
  - Integration tests coverage 80 %
  - Python 3.8, 3.9
  - Create executables for OpenOPCService and OPC cli
  - Create pypy package
  - remain compatible to 1.3 and 1.2

Known Issues:

- Return Values sometimes List of tuples and sometimes tuple... causes trouble complex code
- write(tag, include_error=True) returns list of tuples (which should be tuple)
- too many except: pass this is a very dangerous pattern

Future Goals:

- Proper Logging
- code  refactoring, reduce complexity increase readablility
- replace response tuples with named tuples / dataclasses whatever is suitable
- improve error handling
- introduce encrypted protocol for gateway
- write unittests
- consolidate repositories and forks on github
- test on multiple python versions and platforms

Far away Goals:

- OPC UA Gateway
- OPC AE support
- Rest API
