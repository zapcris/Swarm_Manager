import math
from dataclasses import dataclass




@dataclass
class config:
    x: float
    y: float

class Transfer_robot:

    def __init__(self, name, global_task, data_opcua):
        self.name: name
        self.global_task = global_task
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua
        self.success_bid = None
        self.STN = None



    def bid(self, auctioned_task):
        total_ws = len(self.data_opcua["machine_pos"])
        dist = 0.0
        # for i in range(total_ws - 1):
        #     dist += math.sqrt(math.pow(auctioned_task[i + 1].x - auctioned_task[i].x, 2) + math.pow(
        #         auctioned_task[i + 1].y - auctioned_task[i].y, 2) * 1.0)
        print(auctioned_task)
        return auctioned_task


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







