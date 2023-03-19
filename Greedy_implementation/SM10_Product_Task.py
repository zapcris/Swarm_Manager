from dataclasses import dataclass
from datetime import datetime


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

    # def __getitem__(self, pv_Id):
    #     return getattr(self, pv_Id)

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


@dataclass
class Transfer_time:
    start_time: datetime
    stop_time: datetime
    start_point: int
    stop_point: int
    variant: int
    instance: int
    robot: int
    travel_time: float
    step: int

    def start_timer(self):
        self.start_time = datetime.now()

    def stop_timer(self):
        self.stop_time = datetime.now()

    def calc_time(self):
        self.travel_time = (self.stop_time - self.start_time).total_seconds()


@dataclass
class Process_time:
    start_time: datetime
    stop_time: datetime
    Workstation: int
    step: int
    variant: int
    instance: int
    process_time: float

    def start_timer(self):
        self.start_time = datetime.now()

    def stop_timer(self):
        self.stop_time = datetime.now()

    def calc_time(self):
        self.process_time = (self.stop_time - self.start_time).total_seconds()

@dataclass
class Waiting_time:
    variant: int
    instance: int
    step: int
    start_time: datetime
    stop_time: datetime
    wait_time: float
    robot: int


    def start_timer(self):
        self.start_time = datetime.now()

    def stop_timer(self):
        self.stop_time = datetime.now()

    def calc_time(self):
        self.wait_time = (self.stop_time - self.start_time).total_seconds()

@dataclass
class Source_Sink:
    variant: int
    instance: int
    start_time: datetime
    stop_time: datetime
    cycle_time: float

    def start_timer(self):
        self.start_time = datetime.now()

    def stop_timer(self):
        self.stop_time = datetime.now()

    def cycle_time(self):
        self.cycle_time = (self.stop_time - self.start_time).total_seconds()
