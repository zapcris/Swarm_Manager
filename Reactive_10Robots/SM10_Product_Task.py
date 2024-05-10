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
    step: int

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
    priority: int
    mission_list: []
    current_mission: []
    task: []
    inProduction: False
    finished: False
    last_instance: int
    robot: int
    wk: int
    released: bool
    tracking: []

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

    # def to_wk(self, wk):
    #     object.__setattr__(self, 'robot', 0)
    #     object.__setattr__(self, 'wk', wk)

    def pfinished(self):
        object.__setattr__(self, 'finished', True)

    #
    # def reset_Instance(self):
    #     object.__setattr__(self, 'last_instance', 0)

    # def remove_task(self):
    #     if len(self.task_list) > 0:
    #         #print(f"Task {self.task_list[0]} removed from the product {self.pv_Id, self.pi_Id}")
    #         self.task_list.pop(0)
    #
    #     return self

    def process_done(self, wk_id):
        self.wk = wk_id
        if self.mission_list:
            self.mission_list.pop(0)
            print(f"workstation {self.wk} mission list generated {self.mission_list}")
            self.current_mission = self.mission_list[0]
            print(f"Current mission updated for product {self.pv_Id} {self.current_mission}")
        else:
            raise Exception(f"Product{self.pv_Id}{self.pi_Id} has no missions left on workstation{self.wk}")
        self.task = [99, 99]



@dataclass
class Base1:
    stime: datetime
    etime: datetime
    dtime: float

    def start_timer(self):
        self.stime = datetime.now()

    def stop_timer(self):
        self.etime = datetime.now()

    def calc_time(self):
        self.etime = datetime.now()
        self.dtime = (self.etime - self.stime).total_seconds()


@dataclass
class Base2:
    tr_no: int
    pickup: int
    drop: int


@dataclass
class Transfer_time(Base1, Base2):
    sts: str = "Transfer"


@dataclass
class Process_time(Base1):
    wk_no: int
    sts: str = "Process"


@dataclass
class Waiting_time(Base1, Base2):
    sts: str = "Wait"


@dataclass
class Source:
    tstamp: datetime
    sts: str = "Source"


@dataclass
class Sink:
    tstamp: datetime
    sts: str = "Sink"
