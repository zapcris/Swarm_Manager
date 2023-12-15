import asyncio
import sys
import time
from asyncua import Client, Node, ua
import threading


async def main_function(data_opcua):
    full_path = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

    async with Client(url=full_path) as client:

        objects = await client.nodes.root.get_children()
        # print(objects)
        for i in objects:
            object_name = await i.read_browse_name()
            if object_name.Name == 'Objects':
                # print("Objects:", object_name.Name)
                folder_object = await i.get_children()

                for i2 in folder_object:
                    folder_name = await i2.read_browse_name()
                    # print("folder_name",folder_name)
                    if (folder_name.Name == "create_part"):
                        create_part = await i2.get_children()
                    if (folder_name.Name == "machine_parts"):
                        machine_parts = await i2.get_children()
                    if (folder_name.Name == "Moble manipulator control"):
                        mobile_manipulator_control = await i2.get_children()
                    if (folder_name.Name == "Moble manipulator busy"):
                        Moble_manipulator_busy = await i2.get_children()
                    if (folder_name.Name == "Positions"):
                        Positions = await i2.get_children()
                    if (folder_name.Name == "Time of task"):
                        task_time = await i2.get_children()
                    if (folder_name.Name == "reconfiguration"):
                        reconfiguration = await i2.get_children()

        for k in create_part:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'create_new_part':
                create_new_part = k
            if object_name.Name == 'recive_part':
                recive_part = k

        for k in Moble_manipulator_busy:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'rob1_busy':
                rob1_busy = k
            if object_name.Name == 'rob2_busy':
                rob2_busy = k
            if object_name.Name == 'rob3_busy':
                rob3_busy = k
            if object_name.Name == 'rob4_busy':
                rob4_busy = k
            if object_name.Name == 'rob5_busy':
                rob5_busy = k
            if object_name.Name == 'rob6_busy':
                rob6_busy = k
            if object_name.Name == 'rob7_busy':
                rob7_busy = k
            if object_name.Name == 'rob8_busy':
                rob8_busy = k
            if object_name.Name == 'rob9_busy':
                rob9_busy = k
            if object_name.Name == 'rob10_busy':
                rob10_busy = k

        rob_busy = [rob1_busy, rob2_busy, rob3_busy, rob4_busy, rob5_busy, rob6_busy, rob7_busy, rob8_busy, rob9_busy,
                    rob10_busy]

        for k in Positions:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'machine_pos':
                machine_pos = k
            if object_name.Name == 'robot_pos':
                robot_pos = k

        for k in reconfiguration:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'reconfiguration_machine_pos':
                reconfiguration_machine_pos = k
            if object_name.Name == 'do_reconfiguration':
                do_reconfiguration = k

        for k in machine_parts:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'create_machine1':
                create_machine1 = k
            if object_name.Name == 'machine_1_part':
                machine_1_part = k
            if object_name.Name == 'machine_2_part':
                machine_2_part = k
            if object_name.Name == 'machine_3_part':
                machine_3_part = k
            if object_name.Name == 'machine_4_part':
                machine_4_part = k
            if object_name.Name == 'machine_5_part':
                machine_5_part = k
            if object_name.Name == 'machine_6_part':
                machine_6_part = k
            if object_name.Name == 'machine_7_part':
                machine_7_part = k
            if object_name.Name == 'machine_8_part':
                machine_8_part = k
            if object_name.Name == 'machine_9_part':
                machine_9_part = k
            if object_name.Name == 'machine_10_part':
                machine_10_part = k

        create_machines = [create_machine1]

        machine_part = [machine_1_part, machine_2_part, machine_3_part,
                        machine_4_part, machine_5_part, machine_6_part,
                        machine_7_part, machine_8_part, machine_9_part,
                        machine_10_part]

        for k in mobile_manipulator_control:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'mobile_manipulator_1':
                mobile_manipulator_1 = k
            if object_name.Name == 'mobile_manipulator_2':
                mobile_manipulator_2 = k
            if object_name.Name == 'mobile_manipulator_3':
                mobile_manipulator_3 = k
            if object_name.Name == 'mobile_manipulator_4':
                mobile_manipulator_4 = k
            if object_name.Name == 'mobile_manipulator_5':
                mobile_manipulator_5 = k
            if object_name.Name == 'mobile_manipulator_6':
                mobile_manipulator_6 = k
            if object_name.Name == 'mobile_manipulator_7':
                mobile_manipulator_7 = k
            if object_name.Name == 'mobile_manipulator_8':
                mobile_manipulator_8 = k
            if object_name.Name == 'mobile_manipulator_9':
                mobile_manipulator_9 = k
            if object_name.Name == 'mobile_manipulator_10':
                mobile_manipulator_10 = k

        mobile_manipulator = [mobile_manipulator_1, mobile_manipulator_2, mobile_manipulator_3,
                              mobile_manipulator_4, mobile_manipulator_5, mobile_manipulator_6,
                              mobile_manipulator_7, mobile_manipulator_8, mobile_manipulator_9,
                              mobile_manipulator_10]

        for k in task_time:
            object_name = await k.read_browse_name()
            # print(object_name)
            if object_name.Name == 'task_time_rob1':
                mobile_manipulator_1 = k
            if object_name.Name == 'task_time_rob2':
                mobile_manipulator_2 = k
            if object_name.Name == 'task_time_rob3':
                mobile_manipulator_3 = k
            if object_name.Name == 'task_time_rob4':
                mobile_manipulator_4 = k
            if object_name.Name == 'task_time_rob5':
                mobile_manipulator_5 = k
            if object_name.Name == 'task_time_rob6':
                mobile_manipulator_6 = k
            if object_name.Name == 'task_time_rob7':
                mobile_manipulator_7 = k
            if object_name.Name == 'task_time_rob8':
                mobile_manipulator_8 = k
            if object_name.Name == 'task_time_rob9':
                mobile_manipulator_9 = k
            if object_name.Name == 'task_time_rob10':
                mobile_manipulator_10 = k

        all_task_time_opc = [mobile_manipulator_1, mobile_manipulator_2, mobile_manipulator_3,
                             mobile_manipulator_4, mobile_manipulator_5, mobile_manipulator_6,
                             mobile_manipulator_7, mobile_manipulator_8, mobile_manipulator_9,
                             mobile_manipulator_10]

        for k in range(len(mobile_manipulator)):
            await mobile_manipulator[k].write_value("")

        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################

        # machine_pos robot_pos
        machine_positions = [0] * 11
        rob_positions = [0] * 10
        robot_busy = [0] * 10
        robot_task_time = [0] * 10
        reconfig_positions = [0] * 10
        while (True):
            ##################################################
            # Read if mobile manipulator is busy
            for k in range(len(rob_busy)):
                robot_busy[k] = await rob_busy[k].read_value()

            data_opcua["rob_busy"] = robot_busy
            ##################################################
            # The driving time for the mobile robot:
            for k in range(len(all_task_time_opc)):
                robot_task_time[k] = await all_task_time_opc[k].read_value()
                if (robot_task_time[k] != ""):
                    robot_task_time[k] = float(robot_task_time[k])

            data_opcua["all_task_time"] = robot_task_time

            ##################################################
            # Read machine position data
            values = await machine_pos.read_value()
            split_all = values.split("d")
            for k in range(len(split_all)):

                divide = split_all[k]
                try:
                    x, y = divide.split(",")
                    x = float(x)
                    y = float(y)
                    machine_positions[k] = [x, y]
                except:
                    machine_positions[k] = [0, 0]
            data_opcua["machine_pos"] = machine_positions
            ##################################################
            # Write reconfiguration data and send it to the simulation:
            await do_reconfiguration.write_value(data_opcua["do_reconfiguration"])

            await reconfiguration_machine_pos.write_value(data_opcua["reconfiguration_machine_pos"])
            ##################################################
            values = await robot_pos.read_value()
            # print("values",values)
            split_all = values.split("d")
            for k in range(len(split_all)):
                divide = split_all[k]
                try:
                    x, y = divide.split(",")
                    x = float(x)
                    y = float(y)
                    rob_positions[k] = [x, y]
                except:
                    ok = 0
            data_opcua["robot_pos"] = rob_positions
            ##################################################

            ##################################################
            # Create parts code !!!
            await create_new_part.write_value(data_opcua["create_part"])  # What part to create

            data_opcua[
                "recive_part"] = await recive_part.read_value()  # To confirm that Visual Components has created the part

            ##################################################
            mobile_manipulator_thread = data_opcua["mobile_manipulator"]
            for k in range(len(mobile_manipulator_thread)):
                mission = mobile_manipulator_thread[k]
                if (mission != ""):
                    await mobile_manipulator[k].write_value(mission)
                else:
                    await mobile_manipulator[k].write_value("")

            # print("rob_positions",rob_positions)
            # print("machine_positions", machine_positions)
            # print("robot_busy", robot_busy)
            # time.sleep(10)
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################


def start_opcua(data_opcua):
    asyncio.run(main_function(data_opcua))


if __name__ == "__main__":

    data_opcua = {
        "brand": "Ford",
        "mobile_manipulator": ["", "", "", "", "", "", "", "", "", ""],
        "rob_busy": [False, False, False, False, False, False, False, False, False, False],
        "machine_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ],
        "robot_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],

        "create_part": 0,
        "recive_part": False,
        "done_createing_part": False,

        "mission": ["", "", "", "", "", "", "", "", "", ""],
        "all_task_time": ["", "", "", "", "", "", "", "", "", ""],
        "do_reconfiguration": False,
        "reconfiguration_machine_pos": "",

    }

    x = threading.Thread(target=start_opcua, args=(data_opcua,))
    x.start()

    time.sleep(1)


    def wait_create_parrt(data_opcua):
        # Wait until the part has been created
        run1 = 1
        # time.sleep(0.5)
        t1 = time.time()
        while (run1 == 1):
            time.sleep(0.1)
            if (data_opcua["recive_part"] == True):  # Wait until a part har been created
                data_opcua["create_part"] = 0
                run1 = 0

        # wait until Visual Components is ready to create a new part
        run2 = 1
        while (run2 == 1):
            time.sleep(0.1)
            if (data_opcua["recive_part"] == False):
                run2 = 0
        print("Required time for part creation second:", (time.time() - t1))

    while True:
        print(data_opcua["robot_pos"])
        print(data_opcua["rob_busy"])
        print(data_opcua["mobile_manipulator"])

        time.sleep(2)


    data_opcua["create_part"] = 1
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 2
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 3
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 4
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 5
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 6
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 7
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 8
    wait_create_parrt(data_opcua)

    data_opcua["create_part"] = 9
    wait_create_parrt(data_opcua)

    #################################################

    print("all done")
    time.sleep(100)

    # reconfig = "-5947.8017408,1345.07016512d-5891.42134789,3066.44623999d-5801.59637732,4823.26974015d"
    # reconfig = "0,0d10000,6000d0,12000d0,18000d20000,24000d0,30000d30000,36000d0,42000d0,48000d0,54000d0,60000d"

    # data_opcua["reconfiguration_machine_pos"] = reconfig

    # time.sleep(0.5)

    # data_opcua["do_reconfiguration"] = True
    # time.sleep(1)
    # data_opcua["do_reconfiguration"] = False

    # time.sleep(3)
    #
    # # time.sleep(2)
    # #

    #
    # time.sleep(3)
    #
    #
    # data_opcua["mobile_manipulator"] = ['a,10','','']
    # #data_opcua["mobile_manipulator"] = ['n,23', '', '']
    # #data_opcua["mobile_manipulator"] = ['b,1','','']
    # #data_opcua["mobile_manipulator"] = ['m,4000,15000,0', '', '']
    # #data_opcua["mobile_manipulator"] = ['s,7', '', '']
    # time.sleep(0.7)
    # data_opcua["mobile_manipulator"] = ['', '', '']
    #
    # time.sleep(45)
    #
    # data_opcua["mobile_manipulator"] = ['b,0','','']
    # #data_opcua["mobile_manipulator"] = ['n,39', '', '']
    # #data_opcua["mobile_manipulator"] = ['m,0,9000,-5000', '', '']
    # #data_opcua["mobile_manipulator"] = [' ', '', '']
    # time.sleep(0.7)
    # data_opcua["mobile_manipulator"] = ['', '', '']
    #
    # print(data_opcua["machine_pos"])

    while (True):
        time.sleep(2)
        print(data_opcua["machine_pos"])
        print(data_opcua["robot_pos"])
        print("####################################")
