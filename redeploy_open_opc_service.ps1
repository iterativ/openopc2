
Stop-Service -Name "zzzOpenOpcService"
pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./venv/Lib/site-packages `
            --paths ./openopc120 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            ./openopc120/opc_gateway_service.py

./dist/opc_gateway_service.exe install
./dist/opc_gateway_service.exe start debug
