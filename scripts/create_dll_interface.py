import sys
from win32com.client import makepy
import win32com.client



"""
This file shows a test how you can create a Python Class from a dll and therefore create a stub interface. 

"""
program_name = "OPC.Automation"
#program_name = "Matrikon.OPC.Simulation"
#program_name = "ABB.AC800MC_OpcDaServer"
obj = win32com.client.GetObject(Pathname="OPC.Automation")

w = win32com.client.Dispatch(program_name, 1)
print(w)


obj = win32com.client.GetObject("OPC.Automation")

outputFile = f"h{program_name}.interface.py"
comTypeLibraryOrDLL = r"C:\Users\ABB\Downloads\graybox_opc_automation_wrapper\x64\gbda_aut.dll"
sys.argv = ["makepy", "-o", outputFile, comTypeLibraryOrDLL]

makepy.main()
