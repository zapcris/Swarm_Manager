import asyncio
import logging

from asyncua import Server, ua
from asyncua.common.methods import uamethod


@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
    namespace = "http://examples.freeopcua.github.io"
    # server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_endpoint(url)

    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    create_part = await server.nodes.objects.add_object(idx, "create_part")
    create_new_part = await create_part.add_variable(idx, "create_new_part", 0)
    await create_new_part.set_writable()

    machine_parts = await server.nodes.objects.add_object(idx, "machine_parts")
    create_machine1 = await machine_parts.add_variable(idx, "create_machine1", "")
    machine_1_part = await machine_parts.add_variable(idx, "machine_1_part", "")
    machine_2_part = await machine_parts.add_variable(idx, "machine_2_part", "")
    machine_3_part = await machine_parts.add_variable(idx, "machine_3_part", "")
    machine_4_part = await machine_parts.add_variable(idx, "machine_4_part", "")
    machine_5_part = await machine_parts.add_variable(idx, "machine_5_part", "")
    machine_6_part = await machine_parts.add_variable(idx, "machine_6_part", "")
    machine_7_part = await machine_parts.add_variable(idx, "machine_7_part", "")
    machine_8_part = await machine_parts.add_variable(idx, "machine_8_part", "")
    machine_9_part = await machine_parts.add_variable(idx, "machine_9_part", "")
    machine_10_part = await machine_parts.add_variable(idx, "machine_10_part", "")
    sink_machine = await machine_parts.add_variable(idx, "sink_machine", "")

    # Set MyVariable to be writable by clients
    await create_machine1.set_writable()
    await machine_1_part.set_writable()
    await machine_2_part.set_writable()
    await machine_3_part.set_writable()
    await machine_4_part.set_writable()
    await machine_5_part.set_writable()
    await machine_6_part.set_writable()
    await machine_7_part.set_writable()
    await machine_8_part.set_writable()
    await machine_9_part.set_writable()
    await machine_10_part.set_writable()
    await sink_machine.set_writable()

    ###################################################################
    control_mobile_manipulator = await server.nodes.objects.add_object(idx, "Moble manipulator control")
    mobile_manipulator_1 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_1", "")
    mobile_manipulator_2 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_2", "")
    mobile_manipulator_3 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_3", "")
    mobile_manipulator_4 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_4", "")
    mobile_manipulator_5 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_5", "")
    mobile_manipulator_6 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_6", "")
    mobile_manipulator_7 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_7", "")
    mobile_manipulator_8 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_8", "")
    mobile_manipulator_9 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_9", "")
    mobile_manipulator_10 = await control_mobile_manipulator.add_variable(idx, "mobile_manipulator_10", "")

    # Set MyVariable to be writable by clients
    await mobile_manipulator_1.set_writable()
    await mobile_manipulator_2.set_writable()
    await mobile_manipulator_3.set_writable()
    await mobile_manipulator_4.set_writable()
    await mobile_manipulator_5.set_writable()
    await mobile_manipulator_6.set_writable()
    await mobile_manipulator_7.set_writable()
    await mobile_manipulator_8.set_writable()
    await mobile_manipulator_9.set_writable()
    await mobile_manipulator_10.set_writable()

    ###################################################################
    Moble_manipulator_busy = await server.nodes.objects.add_object(idx, "Moble manipulator busy")
    rob1_busy = await Moble_manipulator_busy.add_variable(idx, "rob1_busy", False)
    rob2_busy = await Moble_manipulator_busy.add_variable(idx, "rob2_busy", False)
    rob3_busy = await Moble_manipulator_busy.add_variable(idx, "rob3_busy", False)
    rob4_busy = await Moble_manipulator_busy.add_variable(idx, "rob4_busy", False)
    rob5_busy = await Moble_manipulator_busy.add_variable(idx, "rob5_busy", False)
    rob6_busy = await Moble_manipulator_busy.add_variable(idx, "rob6_busy", False)
    rob7_busy = await Moble_manipulator_busy.add_variable(idx, "rob7_busy", False)
    rob8_busy = await Moble_manipulator_busy.add_variable(idx, "rob8_busy", False)
    rob9_busy = await Moble_manipulator_busy.add_variable(idx, "rob9_busy", False)
    rob10_busy = await Moble_manipulator_busy.add_variable(idx, "rob10_busy", False)

    # Set MyVariable to be writable by clients
    await rob1_busy.set_writable()
    await rob2_busy.set_writable()
    await rob3_busy.set_writable()
    await rob4_busy.set_writable()
    await rob5_busy.set_writable()
    await rob6_busy.set_writable()
    await rob7_busy.set_writable()
    await rob8_busy.set_writable()
    await rob9_busy.set_writable()
    await rob10_busy.set_writable()

    ###################################################################

    task_time = await server.nodes.objects.add_object(idx, "Time of task")
    task_time_rob1 = await task_time.add_variable(idx, "task_time_rob1", "")
    task_time_rob2 = await task_time.add_variable(idx, "task_time_rob2", "")
    task_time_rob3 = await task_time.add_variable(idx, "task_time_rob3", "")
    task_time_rob4 = await task_time.add_variable(idx, "task_time_rob4", "")
    task_time_rob5 = await task_time.add_variable(idx, "task_time_rob5", "")
    task_time_rob6 = await task_time.add_variable(idx, "task_time_rob6", "")
    task_time_rob7 = await task_time.add_variable(idx, "task_time_rob7", "")
    task_time_rob8 = await task_time.add_variable(idx, "task_time_rob8", "")
    task_time_rob9 = await task_time.add_variable(idx, "task_time_rob9", "")
    task_time_rob10 = await task_time.add_variable(idx, "task_time_rob10", "")

    # Set MyVariable to be writable by clients
    await task_time_rob1.set_writable()
    await task_time_rob2.set_writable()
    await task_time_rob3.set_writable()
    await task_time_rob4.set_writable()
    await task_time_rob5.set_writable()
    await task_time_rob6.set_writable()
    await task_time_rob7.set_writable()
    await task_time_rob8.set_writable()
    await task_time_rob9.set_writable()
    await task_time_rob10.set_writable()

    ###################################################################
    positions = await server.nodes.objects.add_object(idx, "Positions")
    machine_pos = await positions.add_variable(idx, "machine_pos", "")
    robot_pos = await positions.add_variable(idx, "robot_pos", "")

    # Set MyVariable to be writable by clients
    await machine_pos.set_writable()
    await robot_pos.set_writable()

    ###################################################################
    reconfiguration = await server.nodes.objects.add_object(idx, "reconfiguration")
    reconfiguration_machine_pos = await reconfiguration.add_variable(idx, "reconfiguration_machine_pos", "")
    do_reconfiguration = await reconfiguration.add_variable(idx, "do_reconfiguration", False)

    # Set MyVariable to be writable by clients
    await reconfiguration_machine_pos.set_writable()
    await do_reconfiguration.set_writable()

    # Variable to inform that create a new part has been recived
    recive_part = await create_part.add_variable(idx, "recive_part", False)
    await recive_part.set_writable()

    async with server:
        while True:
            await asyncio.sleep(1)
            # new_val = await myvar.get_value() + 0.1
            # _logger.info("Set value of %s to %.1f", myvar, new_val)
            # await myvar.write_value(new_val)


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
