import math
import numpy as np
from dataclasses import dataclass


@dataclass
class workstation:
    num: int
    active: bool


@dataclass
class config:
    x: float
    y: float


class topology:
    def __init__(self, ws_list, config_list, top_num):
        self.ws_list = ws_list
        self.configs = config_list
        self.num = top_num

    # def display(self):
    #     # for ws, cfg in zip(self.ws_list, self.configs):
    #     #     print(f"Workstation number: {ws.num} Coordinates x={cfg.x:.2f} y={cfg.y:.2f} active={ws.active}")
    #     print(f"The topology for product variant in batch  number is {self.num}")

    def calculate_distance(self):
        total_ws = len(self.ws_list)  # 5
        dist = 0.0
        for i in range(total_ws - 1):
            dist += math.sqrt(math.pow(self.configs[i + 1].x - self.configs[i].x, 2) + math.pow(
                self.configs[i + 1].y - self.configs[i].y, 2) * 1.0)
        return round(dist)

    def enlist_postions(self):
        total_ws = len(self.ws_list)
        ws_pos_list = []
        ws_seq_list = []
        for ws, cfg in zip(self.ws_list, self.configs):
            # ws_arrays = [ws.num,[cfg.x, cfg.y]]
            ws_arrays = [cfg.x, cfg.y]
            ws_seq_list.append(ws_arrays)
        return ws_seq_list

    def overlap_ws(self):
        no_of_overlaps = 0
        total_ws = len(self.ws_list)  # 5
        for i in range(total_ws - 1):
            if (math.sqrt(math.pow(self.configs[i + 1].x - self.configs[i].x, 2) + math.pow(
                    self.configs[i + 1].y - self.configs[i].y, 2) * 1.0)) <= 3:
                no_of_overlaps += 1

        return no_of_overlaps

    def overlap_routes(self):
        no_of_overlaps = 0
        route_x = 0
        route_y = 0
        Grid = np.zeros((10, 10))
        total_ws = len(self.ws_list)  # 5
        for i in range(total_ws - 1):
            route_x = self.configs[i + 1].x - self.configs[i].x
            route_y = self.configs[i + 1].y - self.configs[i].y
            if route_x <= route_y:
                Grid[route_x:, route_y] = 1
                Grid[route_y, :route_x] = 1
            if route_y < route_x:
                Grid[0:route_x] = 1
                Grid[route_x:route_y] = 1

        return self.configs

    def fitness_calc(self):
        total_ws = len(self.ws_list)  # 5
        dist = 0.0
        fitness_val = 0
        no_of_overlaps = 0
        for i in range(total_ws - 1):
            dist += math.sqrt(math.pow(self.configs[i + 1].x - self.configs[i].x, 2) + math.pow(
                self.configs[i + 1].y - self.configs[i].y, 2) * 1.0)
            if (math.sqrt(math.pow(self.configs[i + 1].x - self.configs[i].x, 2) + math.pow(
                    self.configs[i + 1].y - self.configs[i].y, 2) * 1.0)) <= 3:
                no_of_overlaps += 1
        if no_of_overlaps >= 1:
            fitness_val = 0
        else:
            fitness_val = round(dist)
        return fitness_val
