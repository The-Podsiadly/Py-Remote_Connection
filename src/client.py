"""
Title:          TCP Client
Type:           Client
Engineer:       Michael Podsiadly

https://mender.io/


# NOTE: NOT SECURE! NOT USING TLS, SSL, OR SSH

"""

import networkcommons
import os, io, sys
import asyncio
import logging
from typing import IO
from contextlib import contextmanager


logging.basicConfig(
    filename="system.log",
    format="%(asctime)s :: %(levelname)s : %(name)s : %(message)s",
    level=logging.DEBUG,
    datefmt="%d-%b-%y %H:%M:%S",
)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ++++++++++++++++
# TODO: Add comments
# TODO: Clean up by organizing into multiple files/classes
# TODO: Turn into an app using electronjs
# TODO: Add auto update command (future)
# TODO: Simplify logging
# TODO: Fix __location__ and whenever calling directory to be local
# TODO: Add comments throughout code to understand what is going on
# TODO: Add todo's wherever necessary


@contextmanager
def change_dir(destination):
    """Context Manager decorator that changes directory when called again automatically.

    Keyword arguments:
    destination -- Location (directory) that you want to access
    """
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)


async def sendingShit(folder):
    """ Open directory specified, check for files, make list of files with extensions, send to server, and finally send each file.

    Keyword arguments:
    folder -- String variable of folder name to be sent
    """
    logging.info("Checking for data files")
    with change_dir(folder):
        list = os.listdir()

        if not list:
            logging.info("Directory is empty")
            await NC.send_msg("Empty_Dir")
            return
        else:
            str_list = str(list)[1:-1]  # Convert list to string list
            await NC.send_msg(str_list)
            logging.info("Sent to server String list of data files")

            # Sooo what's going on with the location? Because of the Change_dir, is the os destination currently in that or do we have to change it back?
            for file in list:
                await NC.send_file(file)


# TODO: Finish command list
async def cmd_list(cmd):
    """ Check what command it is and request that event, all controlled by networkcommons

    Keyword arguments:
    cmd -- String variable
    """
    cmd = cmd.lower()

    if cmd == "getdf":  # Get Data Files
        # EDIT FOR ACTUAL DATA FILES
        await sendingShit("client")

        return
    elif cmd == "getlogs":  # Get Logs
        # EDIT FOR ACTUAL LOG FILE
        await sendingShit("client")

        return
    elif cmd == "getads":  # Get ADs
        await sendingShit("client")

        return
    else:
        logging.info("Command does not exist; %s", cmd)
        return


async def tcp_echo_client():
    # Change "127.0.0.1" to the IP address you are trying to connect to
    # Change "8888" to the Port your client is open on
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    global NC
    NC = networkcommons.NC(writer, reader)

    addr = writer.get_extra_info("peername")
    print(f"Connected to {addr}")

    OPEN = True

    while OPEN:
        print("Awaiting command from server")
        cmd = await NC.get_msg()
        print(f"Command from server: {cmd}")

        if cmd == "close":  # Close connection
            OPEN = False
        else:  # Go through command list
            await cmd_list(cmd)

    # await nc.send_file(writer, file)
    # await nc.collect_file(reader)

    print("Close the connection")
    writer.close()


asyncio.run(tcp_echo_client())
