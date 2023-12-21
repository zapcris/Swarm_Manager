import time
import tkinter as tk


def serialise_robot(T_robot):
    robot = {}
    robot["id"] = T_robot.id
    robot["Free"] = T_robot.free
    robot["base"] = T_robot.base
    robot["q1"] = T_robot.q1
    robot["q2"] = T_robot.q2
    robot["wk_loc"] = T_robot.wk_loc
    robot["executing"] = T_robot.executing

    return robot


def serialise_workstation(W_robot):
    workstation = {}
    workstation["id"] = W_robot.id
    workstation["processing"] = W_robot.free
    workstation["product_free"] = W_robot.product_free
    workstation["robot_fre"] = W_robot.robot_free
    workstation["booked"] = W_robot.booked
    workstation["q1_empty"] = W_robot.q1_empty
    workstation["q2_empty"] = W_robot.q2_empty

    return workstation


class Robot:
    def __init__(self, id):
        self.id = id
        self.free = True
        self.base = False
        self.q1 = False
        self.q2 = False
        self.wk_loc = 99
        self.executing = False

        # self.is_working = False
        # self.is_moving = False
        # self.is_error = False


class Workstation:
    def __init__(self, id):
        self.id = id
        self.processing = False
        self.product_free = True
        self.robot_free = True
        self.booked = False
        self.q1_empty = True
        self.q2_empty = True

        # self.is_running = False
        # self.is_maintenance = False
        # self.is_idle = True


class RobotStatusUI(tk.Toplevel):
    def __init__(self, master, robot):
        super().__init__(master)
        self.robot = robot
        self.title(f"Robot {self.robot.id} Status")
        self.create_widgets()

    def create_widgets(self):
        self.id_label = tk.Label(self, text="ID:")
        self.id_label.pack()

        self.free_label = tk.Label(self, text="Free:")
        self.free_label.pack()

        self.base_label = tk.Label(self, text="Base:")
        self.base_label.pack()

        self.q1_label = tk.Label(self, text="Q1:")
        self.q1_label.pack()

        self.q2_label = tk.Label(self, text="Q2:")
        self.q2_label.pack()

        self.executing_label = tk.Label(self, text="Working:")
        self.executing_label.pack()

        self.wkloc_label = tk.Label(self, text="Workstation:")
        self.wkloc_label.pack()

        # self.moving_label = tk.Label(self, text="Moving:")
        # self.moving_label.pack()
        #
        # self.error_label = tk.Label(self, text="Error:")
        # self.error_label.pack()

        self.update_status()

    def update_status(self):
        self.id_label.config(text=f"ID: {self.robot.id}")
        self.free_label.config(text=f"Free: {self.robot.free}")
        self.executing_label.config(text=f"Working: {self.robot.executing}")
        self.base_label.config(text=f"Base: {self.robot.base}")
        self.q1_label.config(text=f"Q1: {self.robot.q1}")
        self.q2_label.config(text=f"Q2: {self.robot.q2}")
        self.wkloc_label.config(text=f"Workstation: {self.robot.wk_loc}")
        # self.moving_label.config(text=f"Moving: {self.robot.is_moving}")
        # self.error_label.config(text=f"Error: {self.robot.is_error}")


class WorkstationStatusUI(tk.Toplevel):
    def __init__(self, master, workstation):
        super().__init__(master)
        self.workstation = workstation
        self.title(f"Workstation {self.workstation.id} Status")
        self.create_widgets()

    def create_widgets(self):
        self.id_label = tk.Label(self, text="WK_no:")
        self.id_label.pack()

        self.processing_label = tk.Label(self, text="Processing:")
        self.processing_label.pack()

        self.productfree_label = tk.Label(self, text="Product Free:")
        self.productfree_label.pack()

        self.robotfree_label = tk.Label(self, text="Robot Free:")
        self.robotfree_label.pack()

        self.booked_label = tk.Label(self, text="Booked:")
        self.booked_label.pack()

        self.q1empty_label = tk.Label(self, text="Q1 Empty:")
        self.q1empty_label.pack()

        self.q2empty_label = tk.Label(self, text="Q2 Empty:")
        self.q2empty_label.pack()

        #
        # self.maintenance_label = tk.Label(self, text="Maintenance:")
        # self.maintenance_label.pack()
        #
        # self.idle_label = tk.Label(self, text="Idle:")
        # self.idle_label.pack()

        self.update_status()

    def update_status(self):
        self.id_label.config(text=f"WK_no: {self.workstation.id}")
        self.processing_label.config(text=f"Processing: {self.workstation.processing}")
        self.productfree_label.config(text=f"Product Free:: {self.workstation.product_free}")
        self.robotfree_label.config(text=f"Robot Free:: {self.workstation.robot_free}")
        self.booked_label.config(text=f"Booked: {self.workstation.booked}")
        self.q1empty_label.config(text=f"Q1 Empty: {self.workstation.q1_empty}")
        self.q2empty_label.config(text=f"Q2 Empty: {self.workstation.q2_empty}")

        # self.maintenance_label.config(text=f"Maintenance: {self.workstation.is_maintenance}")
        # self.idle_label.config(text=f"Idle: {self.workstation.is_idle}")


class MainApp:
    def __init__(self, root, T_robots, W_robots):
        self.root = root
        self.root.title("Robot and Workstation Selector")
        # self.robots = [Robot(i) for i in range(1, 11)]
        self.robots = T_robots
        # self.workstations = [Workstation(i) for i in range(1, 11)]
        self.workstations = W_robots
        self.create_widgets()

    def create_widgets(self):
        self.robot_buttons = []
        for robot in self.robots:
            button = tk.Button(self.root, text=f"Robot {robot.id}", command=lambda r=robot: self.show_robot_status(r))
            button.pack()
            self.robot_buttons.append(button)

        self.workstation_buttons = []
        for workstation in self.workstations:
            button = tk.Button(self.root, text=f"Workstation {workstation.id}",
                               command=lambda w=workstation: self.show_workstation_status(w))
            button.pack()
            self.workstation_buttons.append(button)

    def show_robot_status(self, robot):
        status_ui = RobotStatusUI(self.root, robot)

    def show_workstation_status(self, workstation):
        status_ui = WorkstationStatusUI(self.root, workstation)


def update(T_robot):
    time.sleep(10)
    T_robot[1].wk_loc = 15


if __name__ == "__main__":
    T_robot = []
    W_robot = []
    for i in range(10):
        r = Robot(i + 1)
        T_robot.append(r)
        w = Workstation(i + 1)
        W_robot.append(w)
    root = tk.Tk()
    app = MainApp(root, T_robots=T_robot, W_robots=W_robot)
    T_robot[1].wk_loc = 15
    root.mainloop()
