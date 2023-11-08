import math


def euclidean_dist(x1, y1, x2, y2):
    dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)
    return round(dist)


class Fitness():
    def __init__(self, graph):
        fitness_value = 0

        return fitness_value

    def display(self):
        for ws, cfg in zip(self.ws_list, self.configs):
            print(f"Workstation number: {ws.num} Coordinates x={cfg.x} y={cfg.y} active={ws.active}")
        print(f"The topology number is {self.num}")