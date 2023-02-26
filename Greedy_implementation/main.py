import sys

from Greedy_implementation.Scheduler import Joint_Scheduler, Product
from Greedy_implementation.Task_Planner import Task_PG, order
from Greedy_implementation.Robot_agent import Transfer_robot, Workstation_robot
from Greedy_implementation.Task_allocation import Task_Allocation




### instantiate order and generation of task list to that order
test_order = Task_PG(order)
generate_task = test_order.task_list()
Product_task = generate_task[0]
Global_task = generate_task[1]
Task_Queue = generate_task[2]

# for i in Task_Queue:
#     print(i)
# print(Product_task)
#print(Global_task)

#### initialize OPCUA client to communicate to Visual Components ###################

data_opcua = {
            "brand": "Ford",
            "mobile_manipulator": ["", "", ""],
            "rob_busy": [False, False, False],
            "machine_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ],
            "robot_pos": [[0, 0], [0, 0], [0, 0]],
            "create_part": 0,
            "mission": ["", "", "", "", "", "", "", "", "", ""]
    }
# x = threading.Thread(target=start_opcua, args=(data_opcua,))
# x.start()



#########Initialization of Workstation robots###############################

W_robot = []
for i, (type,pt) in enumerate(zip(order["Wk_type"], order["Process_times"])):
    if type==1 or type==2:
        #print("create wk", i, pt, type)
        wr = Workstation_robot(i, pt, data_opcua)
        W_robot.append(wr)


########## Initialization of Carrier robots######################################################
T_robot = []
for i , R in enumerate(data_opcua["rob_busy"]):
    #print(i+1, R)
    robot = Transfer_robot(i + 1, Global_task, data_opcua)
    T_robot.append(robot)


#sys.exit()

### Initialize Reactive Scheduler
#
GreedyScheduler = Joint_Scheduler(order, Global_task, Product_task, data_opcua, T_robot)

### Initialize the products and initial task for production
initial_task = GreedyScheduler.initialize_production()


###################### perform task allocation####################################

## Initialize Task Allocator
Greedy_Allocator = Task_Allocation(Global_task, data_opcua, T_robot)

Greedy_Allocator.step_allocation(initial_task)

### Trigger bids to transfer robots
#Greedy_Allocator.bid_counter()








############################## Test debug function###########################################
#broadcast_bid(task_list)

# for t in task_list:
#     if t["id"] == 1 or t["id"] == 2 :
#         t.assign(robot="one")
#         t.cstatus(status="Executing")
#         print(t)
#     else:
#         t.deassign(robot="None")
#         print(t)






