"""
Title:          Server/Client Common Functions
Type:           Module
Engineer:       Michael Podsiadly

Command list:
- get_data_files:       Get the latest data files created for each AD
- get_logs:             Get the latest log files for the whole system
- compare_ads:          Get the list of AD files with dates and compare to list in server directory
"""

# ++++++++++++++++

"""
To-Do:
-Send/Receive commands:
    -https://dzone.com/articles/scaling-a-polling-python-application-with-asyncio
-Change all prints to logs
-Create central log file
-Fix comments
"""

import os, io, sys
import asyncio
import logging
from typing import IO

logging.basicConfig(
    filename="networkCommons.log",
    format="%(asctime)s :: %(levelname)s : %(name)s : %(message)s",
    level=logging.DEBUG,
    datefmt="%d-%b-%y %H:%M:%S",
)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ++++++++++++++++


class NC:
    """docstring for networkCommons."""

    def __init__(self, writer, reader):
        self.writer = writer
        self.reader = reader

    # TODO: Compare sent and recieved file sizes
    async def send_file(self, file):
        """Send file of a specified location.

        Keyword arguments:
        writer -- called when initializing connection
        file -- pathway, file name, and file extension
        """
        with open(file, "rb") as file_bytes:  # Opening file as readable in bytes
            print(f"Send: {file_bytes!r}")

            total_bytes = 0
            while True:
                chunk = file_bytes.read(1024)
                total_bytes += len(chunk)

                if not chunk:  # Error with write_eof(). Need a way to finish
                    print("Draining...")

                    check = "end"
                    self.writer.write(check.encode())
                    # Maybe writing at the end an empty list could work

                    await self.writer.drain()
                    break

                self.writer.write(chunk)
            print(f"Sent: {total_bytes!r} bytes")

    # TODO: Compare sent and recieved file sizes
    async def collect_file(self, file):
        """Collect file and save to specified location.

        Keyword arguments:
        reader -- called when initializing connection
        file -- pathway, file name, and file extension
        """
        with open(file, "wb") as f:  # Opening file as writable in bytes

            total_bytes = 0
            while True:
                self.reader._eof = False  # Force to read
                data = await self.reader.read(1024)

                # Get buffer using BytesIO
                chunk = io.BytesIO(data)

                total_bytes += chunk.getbuffer().nbytes

                # last_four = data[:-4].decode("utf-8")
                # last_four = chunk.getvalue()[-1:]
                last_four = chunk.getvalue()
                # print((last_four))

                check = "end"

                # print(check.encode())

                if last_four == check.encode():
                    print("Not Data")
                    break

                f.write(chunk.getvalue())
            print(f"Collected: {total_bytes!r} bytes")

    # os.path.join(__location__, "recieved.png")
    async def send_msg(self, msg):
        """Send message to connection which will initialize an action.

        Keyword arguments:
        writer -- called when initializing connection
        msg -- short command in string format specified at beginning of file
        """
        try:
            logging.info("Sending: %s", msg)
            self.writer.write(msg.encode())
            await self.writer.drain()

        except Exception as e:
            logging.error("Command could not be encoded; %s", e)

    async def get_msg(self):
        """Recieve message and return msg

        Keyword arguments:
        reader -- called when initializing connection
        """
        try:
            # 2^8 bytes at a time. I just like it, no special reason
            data = await self.reader.read(256)
            msg = data.decode()
            addr = writer.get_extra_info("peername")
            logging.info("Received %s from %s", (msg, addr))

        except Exception as e:
            logging.error("Command could not be decoded; %s", e)

        return msg
