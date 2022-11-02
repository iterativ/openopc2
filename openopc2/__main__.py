from openopc2.cli import OpcCli

if __name__ == '__main__':
    opc_cli = OpcCli()
    print("*" * 100)
    opc_cli.parse_arguments()