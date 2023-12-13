

class Transfer_robot:

    def __init__(self, id, global_task, product, tqueue, machine_pos):
        self.id = id
        self.free = True
        # self.start_robot(tqueue)
        self.global_task = global_task
        # self.auctioned_task = auctioned_task
        self.success_bid = None
        self.STN = None
        self.assigned_task = False
        self.assigned_product = False
        self.executing = False
        self.event = asyncio.Event()
        self.task = Task(id=0, type=0, command=[], pI=0, pV=0, allocation=False, status="null", robot=1, step=0)
        self.product = product
        self.finished_product = Product
        self.exec_cmd = False
        self.path_clear = False
        self.wk_loc = 99  ### 99 - arbitrary position #####
        self.base_move = False
        self.wait = False
        self.task_initiated = False
        # self.task_step = int
        self.opcua_cmd = []
        self.new_prod = int
        self.machine_pos = machine_pos
        self.base = False
        self.q1 = False
        self.q2 = False
        # print("The values of workstation positions are", self.machine_pos)
