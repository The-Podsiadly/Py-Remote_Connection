"""
Title:          TCP Server
Type:           Server
Engineer:       Michael Podsiadly

https://mender.io/

"""

import networkcommons
import os, io, sys
import asyncio
import logging
from typing import IO

logging.basicConfig(
    filename="system.log",
    format="%(asctime)s :: %(levelname)s : %(name)s : %(message)s",
    level=logging.DEBUG,
    datefmt="%d-%b-%y %H:%M:%S",
)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ++++++++++++++++
# TODO: Add command control
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


async def gettingShit(directory):
    """ Get message from client--either Empty_Dir or list--and then change the string list into an actual list, which then is used in a for loop to save each file with their respective file type and name in the directory/folder specified.

    Keyword arguments:
    directory -- String variable of folder to be saved in
    """
    data = await NC.get_msg()
    print(data)

    if data == "Empty_Dir":
        logging.info("Client contains empty directory")
        return
    else:
        logging.info("Recieved from client a String list of data files")
        list = data.strip("][").split(", ")  # Converting string into list
        list = [i.replace("'", "") for i in list]

        # Sooo what's going on with the location? Because of the Change_dir, is the os destination currently in that or do we have to change it back?
        for file in list:
            destination = os.path.join(directory, file)
            await NC.collect_file(destination)


# TODO: Finish command list
async def cmd_list(cmd):
    """ Check what command it is and request that event, all controlled by networkcommons

    Keyword arguments:
    cmd -- String variable
    """
    cmd = cmd.lower()

    if cmd == "getdf":  # Get Data Files
        with change_dir("server"):
            await gettingShit(os.getcwd())

        return
    elif cmd == "getlogs":  # Get Logs
        with change_dir("server"):
            await gettingShit(os.getcwd())

        return

    elif cmd == "getads":  # Get ADs
        with change_dir("ads"):
            await gettingShit(os.getcwd())

        return
    else:
        logging.info("Command does not exist; %s", cmd)
        return


async def handle_echo(reader, writer):
    """Control actions and requests for client

    Keyword arguments:
    writer -- called when initializing connection
    reader -- called when initializing connection
    """
    global addr
    global NC
    addr = writer.get_extra_info("peername")

    NC = networkcommons.NC(writer, reader)

    # The heart of the program. Once loop is broken, connection is closed
    OPEN = True
    while OPEN:
        cmd = input("Command: ")
        await NC.send_msg(cmd)

        if cmd == "close":  # Close connection
            OPEN = False
        else:  # Go through command list
            await cmd_list(cmd)

    # await collect_file(reader)
    # await send_file(file, writer)

    print("Close the connection")
    writer.close()


async def main():
    """Start connection for server and manage connection

    Keyword arguments:
    """
    # file = os.path.join(__location__, "server/recieved.png")

    # Change "127.0.0.1" to the IP address you are trying to connect to
    # Change "8888" to the Port your client is open on
    server = await asyncio.start_server(handle_echo, "127.0.0.1", 8888)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    # Serve requests until Ctrl+C is pressed
    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


asyncio.run(main())
