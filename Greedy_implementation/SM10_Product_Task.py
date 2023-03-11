from dataclasses import dataclass


@dataclass
class Task:
    id: int
    type: int
    command: []
    pV: int
    pI: int
    allocation: bool
    status: str
    robot: int

    def __getitem__(self, id):
        return getattr(self, id)



    def assign(self, robot):
        object.__setattr__(self, 'allocation', True)
        object.__setattr__(self, 'robot', robot)

    def deassign(self, robot):
        object.__setattr__(self, 'allocation', False)
        object.__setattr__(self, 'robot', robot)

    def cstatus(self, status):
        object.__setattr__(self, 'status', status)





@dataclass
class Product:
    pv_Id: int
    pi_Id: int
    task_list: []
    #released : bool
    inProduction: False
    finished: False
    last_instance: int
    robot : int
    wk : int



    # current_position = []
    # start_time = time
    # finish_time = time


    # def __init__(self, pi_Id, pv_Id, task_list, inProduction, finished, last_instance):
    #     self.pi_ID = pi_Id
    #     self.pv_ID = pv_Id
    #     self.inProduction = inProduction
    #     self.produced = finished
    #     self.task_list = task_list
    #     self.last_instance = last_instance



    # def __str__(self):
    #     return f'The product instance is {self.pi}'
    #
    # def __repr__(self):
    #     return self

    def __getitem__(self, pv_Id):
        return getattr(self, pv_Id)

    def remove_from_production(self):
        object.__setattr__(self, 'inProduction', False)

    def to_robot(self, robot):
        object.__setattr__(self, 'wk', 0)
        object.__setattr__(self, 'robot', robot)

    def to_wk(self, wk):
        object.__setattr__(self, 'robot', 0)
        object.__setattr__(self, 'wk', wk)

    def pfinished(self):
        object.__setattr__(self, 'finished', True)
    #
    # def reset_Instance(self):
    #     object.__setattr__(self, 'last_instance', 0)

    def dequeue(self):
        if len(self.task_list) > 0 :
            self.task_list.pop(0)
        return (self)
