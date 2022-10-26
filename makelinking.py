import sys
from win32com.client import makepy
import win32com.client

w=win32com.client.Dispatch("OPC.Automation", 1)
#w.Visible=1
print(w)


from comtypes.client import CreateObject
obj = CreateObject("OPC.Automation")


files = "dbghelp.dll"
outputFile = r"httpwatch_automation.py"
comTypeLibraryOrDLL = r"C:\Users\ABB\Downloads\graybox_opc_automation_wrapper\x64\gbda_aut.dll"
sys.argv = ["makepy", "-o", outputFile, comTypeLibraryOrDLL]

makepy.main ()