
Stop-Service -Name "zzzOpenOpcService"
./build_executables.ps1
./dist/OpenOpcService.exe install
./dist/OpenOpcService.exe start debug
