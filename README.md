# Py-Remote_Connection
Connect "Server" with "Client" remotely using WebSocket. Uses AsyncIO to open up a connection on localhost.

The point of this program is to created a simple way to connect 2 devices using the same package through a simple, secure interface.

Currenlty, this program simply opens up a connection between a server and a client over localhost and sends data back and forth with verification. It uses a central script `networkcommons.py` that creates a simple AsyncIO connection and verifies the file that was received and prepares a file to be sent. *Headers are examines.*

[Contributions are welcome.](#contributions) **Currently, there is no layout for contributions.**

## Setup
Good luck for now...

## Benchamrks
Not existent right now..
<!-- Decision to use `threading` is based off of [previous benchmarks](https://edmundmartin.com/beautiful-soup-vs-lxml-speed/), we want this program to scale with performance. Yet, I have added support for `synchronous`. *`AsyncIO` currently doesn't not work* -->

## Future Additions
Current list of future additions:
* Add log
* Create unit tests
* Add SSH, SSL, TLS capabilities
* Create unique IP address for product (or use the hardware's IP)
* Turn into a Python package
* Turn into a CLI

If you have any additions you'd like to see, let me know. Contributions is encouraged!

## Contributions
Currently do not have a template for posting contributions..
