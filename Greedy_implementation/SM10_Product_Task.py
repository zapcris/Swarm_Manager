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
    inProduction: False
    finished: False
    last_instance: int
    robot: int
    wk: int
    released: bool

    # def __str__(self):
    #     return f'The product instance is {self.pi}'
    #
    # def __repr__(self):
    #     return self

    def __getitem__(self, pv_Id):
        return getattr(self, pv_Id)

    def remove_from_production(self):
        object.__setattr__(self, 'inProduction', False)

    def set_Release(self):
        object.__setattr__(self, 'released', True)

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

    def remove_task(self):
        if len(self.task_list) > 0:
            print(f"Task {self.task_list[0]} removed from the product {self.pv_Id, self.pi_Id}")
            self.task_list.pop(0)

        return self
