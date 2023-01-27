import asyncio
import math
import time

import matplotlib
from asyncua import Client, Server
from opcua import ua, uamethod, Server
import logging
import os.path




if __name__ == "__main__":
    topology = {1: (9, 4), 2: (18, 13),
                3: (22, 8), 4: (18, 10),
                5: (13, 0), 6: (15, 4),
                7: (24, 22), 8: (12, 6),
                9: (10, 11), 10: (14, 16),
                11: (26, 15), 12: (30, 4),
                13: (17, 17), 14: (0, 2),
                15: (19, 24), 16: (22, 12),
                17: (26, 20), 19: (23, 33),
                20: (27, 28)}
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    #setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar1 = myobj.add_variable(idx, "topology", 6.7)
    myvar1.set_writable()    # Set MyVariable to be writable by clients

    # starting!
    server.start()

    try:

        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            myvar1.set_value(len(topology))
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()