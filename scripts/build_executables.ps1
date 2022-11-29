
poetry run pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./openopc2 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcService `
            openopc2/gateway_service.py


poetry run pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./openopc2 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcCli `
            openopc2/cli.py

poetry run pyinstaller --onefile `
            --clean `
            --noconfirm `
            --paths ./openopc2 `
            --hidden-import=json `
            --hidden-import=win32timezone `
            --hidden-import=pythoncom  `
            --name OpenOpcServer `
            openopc2/gateway_server.py