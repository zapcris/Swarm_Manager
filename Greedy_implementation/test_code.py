from dataclasses import dataclass
from typing import Any


@dataclass
class Product:
    pv_Id: int
    pi_Id: int
    task_list: []
    inProduction: False
    finished: False
    last_instance: int

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

    def dequeue(self):
        if len(self.task_list) > 0:
            self.task_list.pop(0)
        return (self)


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


#product = Product(1,1,[0,0],True,False,1)
product = Product(pv_Id=1,pi_Id=1,task_list=[0,0],inProduction=True,finished=False,last_instance=1)
#task = Task(id=1,type=1,)

print (product["inProduction"])
