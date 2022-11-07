pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./venv/Lib/site-packages `
            --paths ./openopc2 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcService `
            ../openopc2/gateway_service.py
