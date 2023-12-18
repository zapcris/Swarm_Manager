import tkinter as tk

class Robot:
    def __init__(self, id):
        self.id = id
        self.is_working = False
        self.is_moving = False
        self.is_error = False

class Workstation:
    def __init__(self, id):
        self.id = id
        self.is_running = False
        self.is_maintenance = False
        self.is_idle = True

class RobotStatusUI(tk.Toplevel):
    def __init__(self, master, robot):
        super().__init__(master)
        self.robot = robot
        self.title(f"Robot {self.robot.id} Status")
        self.create_widgets()

    def create_widgets(self):
        self.working_label = tk.Label(self, text="Working:")
        self.working_label.pack()

        self.moving_label = tk.Label(self, text="Moving:")
        self.moving_label.pack()

        self.error_label = tk.Label(self, text="Error:")
        self.error_label.pack()

        self.update_status()

    def update_status(self):
        self.working_label.config(text=f"Working: {self.robot.is_working}")
        self.moving_label.config(text=f"Moving: {self.robot.is_moving}")
        self.error_label.config(text=f"Error: {self.robot.is_error}")

class WorkstationStatusUI(tk.Toplevel):
    def __init__(self, master, workstation):
        super().__init__(master)
        self.workstation = workstation
        self.title(f"Workstation {self.workstation.id} Status")
        self.create_widgets()

    def create_widgets(self):
        self.running_label = tk.Label(self, text="Running:")
        self.running_label.pack()

        self.maintenance_label = tk.Label(self, text="Maintenance:")
        self.maintenance_label.pack()

        self.idle_label = tk.Label(self, text="Idle:")
        self.idle_label.pack()

        self.update_status()

    def update_status(self):
        self.running_label.config(text=f"Running: {self.workstation.is_running}")
        self.maintenance_label.config(text=f"Maintenance: {self.workstation.is_maintenance}")
        self.idle_label.config(text=f"Idle: {self.workstation.is_idle}")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot and Workstation Selector")
        self.robots = [Robot(i) for i in range(1, 11)]
        self.workstations = [Workstation(i) for i in range(1, 11)]
        self.create_widgets()

    def create_widgets(self):
        self.robot_buttons = []
        for robot in self.robots:
            button = tk.Button(self.root, text=f"Robot {robot.id}", command=lambda r=robot: self.show_robot_status(r))
            button.pack()
            self.robot_buttons.append(button)

        self.workstation_buttons = []
        for workstation in self.workstations:
            button = tk.Button(self.root, text=f"Workstation {workstation.id}", command=lambda w=workstation: self.show_workstation_status(w))
            button.pack()
            self.workstation_buttons.append(button)

    def show_robot_status(self, robot):
        status_ui = RobotStatusUI(self.root, robot)

    def show_workstation_status(self, workstation):
        status_ui = WorkstationStatusUI(self.root, workstation)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

