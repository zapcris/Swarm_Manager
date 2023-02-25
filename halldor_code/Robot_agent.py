import math
from dataclasses import dataclass




@dataclass
class config:
    x: float
    y: float

class Transfer_robot:

    def __init__(self, num, global_task, data_opcua):
        self.num = num
        self.global_task = global_task
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua
        self.success_bid = None
        self.STN = None




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

        task_cost = math.sqrt(math.pow(end_pos[0] - start_pos[0], 2) + math.pow(
                    end_pos[1] - start_pos[1], 2) * 1.0)

        marginal_cost = math.sqrt(math.pow(start_pos[0] - self.data_opcua["robot_pos"][self.num-1][0], 2) + math.pow(
                    start_pos[1] - self.data_opcua["robot_pos"][self.num-1][1], 2) * 1.0)
        bid_value = task_cost + marginal_cost
        #print(bid_value)
        return bid_value


    # def build_STN(self, success_bid):
    #
    #
    #
    #
    #
    # def update_STN(self, success_bid):


class Workstation_robot:

    def __init__(self, name, process_times, data_opcua):
        self.name: name
        self.processtime = process_times
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua







