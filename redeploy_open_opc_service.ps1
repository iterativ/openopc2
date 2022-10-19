

Stop-Service -Name "zzzOpenOpcService"
pyinstaller --paths ./venv/Lib/site-packages --paths ./openopc120 --hidden-import=json --hidden-import=win32timezone --hidden-import=pythoncom  ./openopc120/OpenOpcService.py

./dist/OpenOpcService/OpenOpcService.exe install
./dist/OpenOpcService/OpenOpcService.exe start debug
