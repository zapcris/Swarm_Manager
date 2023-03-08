import asyncio
import time
from asyncua import Client, Node, ua
import threading

async def main_function(data_opcua):
    full_path = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

    async with Client(url=full_path) as client:

        objects = await client.nodes.root.get_children()
        print(objects)
        for i in objects:
            object_name = await i.read_browse_name()
            if object_name.Name == 'Objects':
                print("Objects:", object_name.Name)
                folder_object = await i.get_children()

                for i2 in folder_object:
                    folder_name = await i2.read_browse_name()
                    print("folder_name",folder_name)
                    if(folder_name.Name == "create_part"):
                        create_part = await i2.get_children()
                    if(folder_name.Name == "machine_parts"):
                        machine_parts = await i2.get_children()
                    if(folder_name.Name == "Moble manipulator control"):
                        mobile_manipulator_control = await i2.get_children()
                    if(folder_name.Name == "Moble manipulator busy"):
                        Moble_manipulator_busy = await i2.get_children()
                    if(folder_name.Name == "Positions"):
                        Positions = await i2.get_children()

        for k in create_part:
            object_name = await k.read_browse_name()
            print(object_name)
            if object_name.Name == 'create_new_part':
                create_new_part = k

        for k in Moble_manipulator_busy:
            object_name = await k.read_browse_name()
            print(object_name)
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

        rob_busy = [rob1_busy,rob2_busy,rob3_busy,rob4_busy,rob5_busy]

        for k in Positions:
            object_name = await k.read_browse_name()
            print(object_name)
            if object_name.Name == 'machine_pos':
                machine_pos = k
            if object_name.Name == 'robot_pos':
                robot_pos = k

        for k in machine_parts:
            object_name = await k.read_browse_name()
            print(object_name)
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

        machine_part = [machine_1_part,machine_2_part,machine_3_part,
                              machine_4_part,machine_5_part,machine_6_part,
                              machine_7_part,machine_8_part,machine_9_part,
                              machine_10_part]

        for k in mobile_manipulator_control:
            object_name = await k.read_browse_name()
            print(object_name)
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

        mobile_manipulator = [mobile_manipulator_1,mobile_manipulator_2,mobile_manipulator_3,
                              mobile_manipulator_4,mobile_manipulator_5,mobile_manipulator_6,
                              mobile_manipulator_7,mobile_manipulator_8,mobile_manipulator_9,
                              mobile_manipulator_10]

        for k in range(len(mobile_manipulator)):
            await mobile_manipulator[k].write_value("")

        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################


        """
            data_opcua = {
        "brand": "Ford",
        "mobile_manipulator": ["", "", ""],
        "rob_busy": [False, False, False],
        "machine_pos": [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],],
        "robot_pos": [[0, 0], [0, 0], [0, 0]],
    }
        """


        # machine_pos robot_pos
        machine_positions = [0]*10
        rob_positions = [0]*3
        robot_busy = [0]*5
        while(True):

            # Read if mobile manipulator is busy
            for k in range(len(rob_busy)):
                robot_busy[k] = await rob_busy[k].read_value()
            data_opcua["rob_busy"] = robot_busy
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
                    machine_positions[k] = [x,y]
                except:
                    ok = 0
            data_opcua["machine_pos"] = machine_positions

            ##################################################
            values = await robot_pos.read_value()
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



            # print("create part ")
            await create_new_part.write_value(data_opcua["create_part"])


            mobile_manipulator_thread = data_opcua["mobile_manipulator"]
            for k in range(len(mobile_manipulator_thread)):
                mission = mobile_manipulator_thread[k]
                if (mission != ""):
                    await mobile_manipulator[k].write_value(mission)
                else:
                    await mobile_manipulator[k].write_value("")

            #print("rob_positions",rob_positions)
            #print("machine_positions", machine_positions)
            #print("robot_busy", robot_busy)
            #time.sleep(10)
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################





async def start_opcua(data_opcua):
    asyncio.run(main_function(data_opcua))

if __name__ == "__main__":

    data_opcua = {
        "brand": "Ford",
        "mobile_manipulator": ["", "", ""],
        "rob_busy": [False, False, False],
        "machine_pos": [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],],
        "robot_pos": [[0, 0], [0, 0], [0, 0]],
        "create_part": 0,
        "mission": ["","","","","","","","","",""]
    }

    x = threading.Thread(target=start_opcua, args=(data_opcua,))
    x.start()


    time.sleep(2)

    data_opcua["create_part"] = 9
    time.sleep(0.7)
    data_opcua["create_part"] = 0

    time.sleep(2)

    data_opcua["mobile_manipulator"] = ['4,7','','']
    #data_opcua["mobile_manipulator"] = ['m,0,-5000,0', '', '']
    #data_opcua["mobile_manipulator"] = ['', 's,7', '']
    time.sleep(0.7)
    data_opcua["mobile_manipulator"] = ['', '', '']

    while True:
        time.sleep(1)

        print(data_opcua["rob_busy"])

    print("all done!@!!!")


    """
    while(True):

        time.sleep(0.5)
        print(data_opcua["machine_pos"])
        print(data_opcua["robot_pos"])
        print("####################################")
    """
    # new code under:



