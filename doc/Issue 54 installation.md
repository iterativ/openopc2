## 64 bit installation
1. install OPC Core Components Redistributable (x64) 3.00.107
2. Restart windows server
3. Delete previous installed OpenOPCService and uninstall gbda_aut.dll
4. Download OpenOPCService from https://github.com/iterativ/openopc2/releases/tag/0.1.11 and put it to Program Files
5. Install and start service OpenOPCService
6. Copy 64 bit version of gbda_aut.dll to System32
7. Got to System32 and run regsvr32 gbda_aut.dll
8. Setup env variables
9. OPC_CLASS=OPC.Automation
10. OPC_CLIENT=OpenOPC
11. OPC_GATE_HOST={server-ip}
12. OPC_GATE_PORT=7766
13. OPC_HOST=localhost
14. OPC_MODE=dcom
15. OPC_SERVER=Matrikon.OPC.Simulation
16. Create inbound outbound rule for port 7766 (tried with turned off firewall as well)
17. Download OpenOPCCli from https://github.com/iterativ/openopc2/releases/tag/0.1.11 and put it to Program Files
18. Run openopcCLI server-info
19. Got
20. OPCError: (OPCError(...), 'Dispatch: (-2147221164, 'Class not registered', None, None) opc_class:"OPC.Automation"') [13832] Failed to execute script 'cli' due to unhandled exception!