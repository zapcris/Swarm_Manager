import math
from queue import Queue, Empty
from threading import Thread
from time import sleep
#from write_opcua import write_opcua

#################################### Robot agent code ################################################

class Transfer_robot:

    def __init__(self, id, global_task, data_opcua, tqueue):
        self.id = id
        self.start_robot(tqueue)
        self.global_task = global_task
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua
        self.success_bid = None
        self.STN = None
        self.assigned_task = False




    def bid(self, auctioned_task):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        start_loc = auctioned_task["command"][0]
        end_loc = auctioned_task["command"][1]
        total_ws = len(self.data_opcua["machine_pos"])
        if start_loc == 11: ## if source node
            start_pos = [100, 100]
        else:
            start_pos = self.data_opcua["machine_pos"][start_loc-1]
        if end_loc == 12: ## if source node or sink node
            end_pos = [500, 500]
        else:
            end_pos = self.data_opcua["machine_pos"][end_loc-1]
        ### Euclidean distance for cost calculation ##########
        task_cost = math.sqrt(math.pow(end_pos[0] - start_pos[0], 2) + math.pow(
                    end_pos[1] - start_pos[1], 2) * 1.0)

        #if self.data_opcua["rob_busy"][self.id-1] == False :
        if self.assigned_task == False:
            marginal_cost = math.sqrt(math.pow(start_pos[0] - self.data_opcua["robot_pos"][self.id - 1][0], 2) + math.pow(
                    start_pos[1] - self.data_opcua["robot_pos"][self.id - 1][1], 2) * 1.0)
        else:
            marginal_cost = 999999999
        bid_value = task_cost + marginal_cost
        #print(bid_value)
        return bid_value

    def task_assigned(self):
        self.assigned_task = True
        return self

    def task_deassigned(self):
        self.assigned_task = False
        return self


    def node_function(self, tqueue):
       while True:
           try:
               taken_task = tqueue.get(False)
               self.sendtoOPCUA(taken_task)
               # Opt 1: Handle task here and call q.task_done()
           except Empty:
               # Handle empty queue here
               #print("Queue was empty")
               pass
            #####get first task######
            # taken_task = tqueue.get(False)
            # self.sendtoOPCUA(taken_task)
            # #tqueue.pop(0)

    def start_robot(self, tqueue):
        t = Thread(target=self.node_function, args=(tqueue,))
        t.start()
    def simulate(self,q_in: Queue):
        return None

    def sendtoOPCUA(self, task):
        cmd = ["" for _ in range(2)]
        print(f"Task {task} received from Swarm Manager for execution")
        sleep(0.5)
        c = str(task["command"][0]) + "," + str(task["command"][1])
        cmd.insert((int(self.id) - 1), c)
        if task["command"][0] == 11:
            #main.data_opcua["create_part"] = task["pV"]
            #write_opcua(task["pV"], "create_part", None)
            sleep(0.7)
            print("part created",task["pV"])
            #write_opcua(0, "create_part", None)
            #main.data_opcua["create_part"] = 0
            #write_opcua(0,"create_part")
            sleep(0.7)
            #write_opcua(None, "transfer", cmd)
            sleep(0.7)
            #write_opcua(None, "transfer", ["", "", ""])
            print("command sent to opcuaclient", cmd)

        else:
            #write_opcua(None, "transfer", cmd)
            sleep(0.7)
            #write_opcua(None, "transfer", ["", "", ""])








    def execute_typ1cmd(self, fromscheduler):
        self.data_opcua["mobile_manipulator"] = fromscheduler

    def execute_typ2cmd(self, fromscheduler):
        self.data_opcua["mobile_manipulator"] = fromscheduler

    def execute_typ4cmd(self, fromscheduler):
        self.data_opcua["mobile_manipulator"] = fromscheduler




class Workstation_robot:

    def __init__(self, name, process_times, data_opcua):
        self.name: name
        self.processtime = process_times
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua






