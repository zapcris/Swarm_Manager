

import asyncio
import time
from asyncua import Client, Node, ua


async def main_function():
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

        for k in create_part:
            object_name = await k.read_browse_name()
            print(object_name)
            if object_name.Name == 'create_new_part':
                create_new_part = k

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

        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################
        ###########################################################


        #-----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------
        print("create part ")
        await create_new_part.write_value(9)
        time.sleep(0.7)
        await create_new_part.write_value(0)

        print("Mobile manipultors transports part from")
        message = str(11)+","+str(9)
        await mobile_manipulator[0].write_value(message)
        time.sleep(0.7)
        await mobile_manipulator[0].write_value("")

        time.sleep(7)


        print("create part ")
        await create_new_part.write_value(2)
        time.sleep(0.7)
        await create_new_part.write_value(0)

        print("Mobile manipultors transports part from")
        message = str(11)+","+str(2)
        await mobile_manipulator[1].write_value(message)
        time.sleep(0.7)
        await mobile_manipulator[1].write_value("")

        time.sleep(7)

        print("create part ")
        await create_new_part.write_value(2)
        time.sleep(0.7)
        await create_new_part.write_value(0)

        print("Mobile manipultors transports part from")
        message = str(11)+","+str(3)
        await mobile_manipulator[2].write_value(message)
        time.sleep(0.7)
        await mobile_manipulator[2].write_value("")

        # -----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------
        """
        print("Mobile manipultors transports part")
        message = str(4)+","+str(7)
        await mobile_manipulator[0].write_value(message)
        time.sleep(0.4)
        await mobile_manipulator[0].write_value("")
        """
        # -----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------
        """
        print("Mobile manipultors transports part")
        message = "m"+","+str(0)+","+str(-5000)+","+str(0)
        await mobile_manipulator[0].write_value(message)
        time.sleep(0.4)
        await mobile_manipulator[0].write_value("")
        """

        """
        print("Mobile manipultors transports part")
        message = "s"+","+str(7)
        await mobile_manipulator[0].write_value(message)
        time.sleep(0.4)
        await mobile_manipulator[0].write_value("")
        """






asyncio.run(main_function())


