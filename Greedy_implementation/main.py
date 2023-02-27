import sys
from queue import Empty
from threading import Thread

from Greedy_implementation.Scheduler import Joint_Scheduler, Product
from Greedy_implementation.Task_Planner import Task_PG, order
from Greedy_implementation.Robot_agent import Transfer_robot, Workstation_robot
from Greedy_implementation.Task_allocation import Task_Allocation
import multiprocessing as mp


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





#########Initialization of Workstation robots###############################

W_robot = []
for i, (type,pt) in enumerate(zip(order["Wk_type"], order["Process_times"])):
    if type==1 or type==2:
        #print("create wk", i, pt, type)
        wr = Workstation_robot(i, pt, data_opcua)
        W_robot.append(wr)


########## Initialization of Carrier robots######################################################
T_robot = []
q_robot = []

for r in data_opcua["rob_busy"]:
    q = mp.Queue()
    q_robot.append(q)


for i , R in enumerate(data_opcua["rob_busy"]):
    #print(i+1, R)

    robot = Transfer_robot(id=i + 1, global_task=Global_task, data_opcua=data_opcua, tqueue=q_robot[i])
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

alloted_task = Greedy_Allocator.step_allocation(initial_task)

for aalt in alloted_task:
    print(aalt["id"],aalt["robot"])

######## Peform Task Execution###################
print("Task Execution Initiated")
#GreedyScheduler.execution_queue(alloted_task)


### Trigger bids to transfer robots
#Greedy_Allocator.bid_counter()




####### Task queue functions #############

#pool = mp.Pool()
#manager = mp.Manager()

q_main_to_releaser = mp.Queue()
#q_releaser_to_robot = manager.Queue()
for task in alloted_task:
    q_main_to_releaser.put_nowait(task)

print(q_main_to_releaser)
def assignment_function(allotment_queue):
        # asignee = allotment_queue["robot"]
        # #print(asignee)
        # robot_id = asignee-1
        # robots[robot_id].append(alloted_task)
        while True:

            try:
                asignee = allotment_queue.get(False)
                robot_id = asignee["robot"] - 1
                #robots[robot_id].append(alloted_task)
                print(asignee["robot"])
                q_robot[robot_id].put_nowait(asignee)
                print(q_robot)

                # Opt 1: Handle task here and call q.task_done()
            except Empty:
                # Handle empty queue here
                # print("Queue was empty")
                pass



##### Start Task releaser to Robot thread################

releaser_thread = Thread(target=assignment_function, args=(q_main_to_releaser,))

releaser_thread.start()





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






