from concurrent.futures import ThreadPoolExecutor

from openopc2.utils import get_opc_da_client
from tests.test_config import test_config
import time

from rich.progress import (
    Progress,
    TextColumn,
    TimeElapsedColumn, BarColumn,
)


def read_tags_in_thread(tags: list, task_id,
                        progress, open_opc_config):

    tags = range(100)
    progress.update(task_id, total=len(tags), state="Connecting Server")

    # The easiest way to get multithreading to work is to create the opc client in the thread context

    opc_client = get_opc_da_client(open_opc_config)
    progress.update(task_id, total=len(tags), advance=1, state="Reading Tags")

    for n, tag in range(tags):
        time.sleep(0.1)
        progress.update(task_id, total=len(tags), advance=1, state=f"reading tag:{tag}")
        # read_result = opc_client.read(tag, sync=False)
        # print(f"Thread:{task_id}  Reading Tag: {tag} value: {read_result}")


def main():
    """
    This example show a few simple commands how to configure and connect an OPC server.
    for the ease of use print() is used extensively
    """



    # pylint: disable=import-outside-toplevel
    from rich import print as rprint
    __builtins__.print = rprint


    open_opc_config = test_config()
    open_opc_config.OPC_MODE = 'gateway'
    open_opc_config.OPC_GATEWAY_HOST = '192.168.0.123'
    open_opc_config.print_config()
    paths = "*"

    limit = 20

    opc_client = get_opc_da_client(open_opc_config)
    tags = opc_client.list(paths=paths, recursive=False, include_type=False, flat=True)

    tags = [tag for tag in tags if "@" not in tag and '#' not in tag]
    if limit:
        tags = tags[:limit]

    progress = Progress(
        TimeElapsedColumn(),
        BarColumn(bar_width=None),
        "•",
        "[progress.percentage]{task.percentage:>3.1f}%",
        TextColumn("[magenta]{task.fields[state]}", justify="left"),
    )
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for task in range(5):
                task_id = progress.add_task("Reading Tags", state='')
                pool.submit(read_tags_in_thread, tags, task_id, progress, open_opc_config)


if __name__ == '__main__':
    main()
