import queue
import sys
from queue import Empty
from threading import Thread
from Greedy_implementation.Robot_agent import Transfer_robot, Workstation_robot, data_opcua
from Greedy_implementation.Scheduler import Joint_Scheduler
from Greedy_implementation.Task_Planner import Task_PG, order
from Greedy_implementation.Task_allocation import Task_Allocation
from Greedy_implementation.client_2 import start_opcua

#### initialize OPCUA client to communicate to Visual Components ###################


# x = Thread(target=start_opcua, args=(data_opcua,))
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
    q = queue.Queue()
    q_robot.append(q)


for i , R in enumerate(data_opcua["rob_busy"]):
    #print(i+1, R)

    robot = Transfer_robot(id=i + 1, global_task=Global_task, data_opcua=data_opcua, tqueue=q_robot[i])
    T_robot.append(robot)


#sys.exit()

### Initialize Reactive Scheduler
GreedyScheduler = Joint_Scheduler(order, Global_task, Product_task, data_opcua, T_robot)

## Initialize Task Allocator
Greedy_Allocator = Task_Allocation(Global_task, data_opcua, T_robot)


Sim_step = 0
### Perform task creation and allocation process
initial_task = GreedyScheduler.initialize_production()

alloted_task = Greedy_Allocator.step_allocation(initial_task)

for aalt in alloted_task:
    #print(aalt["id"],aalt["robot"])
    print(aalt)



####### Task queue functions #############

#pool = mp.Pool()
#manager = mp.Manager()

q_main_to_releaser = queue.Queue()
#q_releaser_to_robot = manager.Queue()
for task in alloted_task:
    q_main_to_releaser.put_nowait(task)

print(q_main_to_releaser)
def release_function():
        # asignee = allotment_queue["robot"]
        # #print(asignee)
        # robot_id = asignee-1
        # robots[robot_id].append(alloted_task)
        while True:

            try:
                task_opcua = q_main_to_releaser.get(False)
                robot_id = task_opcua["robot"] - 1
                print(task_opcua["robot"])
                status = T_robot[robot_id].sendtoOPCUA(task_opcua)
                #scheduling_queue.done()
                if task is None:
                    q_main_to_releaser.task_done()
                    break
                q_main_to_releaser.task_done()
                Sim_step = 1
                print("All task completed", Sim_step)

                # Opt 1: Handle task here and call q.task_done()
            except Empty:
                # Handle empty queue here
                # print("Queue was empty")

                #print("No task to release")

                pass



##### Start Task releaser to Robot thread################

releaser_thread = Thread(target=release_function, args=())

releaser_thread.start()

# q_main_to_releaser.join()
# print('All work completed')



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






