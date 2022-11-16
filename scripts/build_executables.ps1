
pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./openopc2 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcService `
            ../openopc2/gateway_service.py


pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./openopc2 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcCli `
            ../openopc2/cli.py