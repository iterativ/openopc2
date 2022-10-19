pyinstaller --paths ./venv/Lib/site-packages --paths ./openopc120 --hidden-import=json --hidden-import=win32timezone --hidden-import=pythoncom  ./openopc120/OpenOpcService.py
pyinstaller --onefile --hidden-import=json --hidden-import=win32timezone --hidden-import=pythoncom ./openopc120/opc.py


