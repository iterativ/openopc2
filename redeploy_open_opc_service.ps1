
Stop-Service -Name "zzzOpenOpcService"
pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./venv/Lib/site-packages `
            --paths ./openopc120 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcService `
            ./openopc120/opc_gateway_service.py

./dist/OpenOpcService.exe install
./dist/OpenOpcService.exe start debug
