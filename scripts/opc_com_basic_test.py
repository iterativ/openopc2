
import pythoncom
import pywintypes
import win32com.client
import win32com.server.util


def main():
    opc_classes = ['Matrikon.OPC.Automation',
                   'Graybox.OPC.DAWrapper',
                   'HSCOPC.Automation',
                   'RSI.OPCAutomation',
                   'OPC.Automation']

    opc_class = "OPC.Automation"

    for opc_class in opc_classes:
        server = "Matrikon.OPC.Simulation"
        host = 'localhost'
        #program_name = "Matrikon.OPC.Simulation"
        server = "ABB.AC800MC_OpcDaServer"

        print(f"Trying to connect OPC server with {server}@{host} class {opc_class}")
        try:
            opc_client = win32com.client.gencache.EnsureDispatch(opc_class, 0)
            opc_client.Connect(server, host)


            info = f"""
            SERVER =  {server}
            HOST = {host}
            OPC_CLASS = {opc_class}
            
            client_name     {opc_client.ClientName}
            server_name =   {opc_client.ServerName}
            server_state =  {opc_client.ServerState}
            version =       {opc_client.MajorVersion}.{opc_client.MinorVersion} - {opc_client.BuildNumber}
            start_time =    {opc_client.StartTime}
            current_time =  {opc_client.CurrentTime}
            vendor_info =   {opc_client.VendorInfo}
            """
            print(info)
        except Exception as e:
            print(e.__dict__)


if __name__ == '__main__':
    main()