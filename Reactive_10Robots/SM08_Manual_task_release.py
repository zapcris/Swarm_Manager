import threading
import time
from tkinter import *
import queue
from Reactive_majorversion3.SM02_opcua_client_2_7 import start_opcua


q1 = queue.Queue(maxsize=100)



class MyWindow:



    def __init__(self, win, data_opcua):
        self.lbl1=Label(win, text='Enter Part Name')
        self.lbl2=Label(win, text='Robot No.')
        self.data_opcua = data_opcua
        self.lbl3 = Label(win, text='start workstation')
        self.lbl4 = Label(win, text='End workstation')


        self.t1=Entry(bd=3)
        self.t2=Entry()
        self.t3=Entry()
        self.t4=Entry()
        self.btn1 = Button(win, text='Create')

        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=20, y=100)
        self.t2.place(x=100, y=100)
        self.lbl3.place(x=20, y=150)
        self.lbl4.place(x=300, y=150)
        self.t3.place(x=150, y=150)
        self.t4.place(x=450, y=150)
        self.b1=Button(win, text='Create Part', command=self.create)
        self.b3 = Button(win, text='QueueTask', command=self.queue)
        self.b4 = Button(win, text='ReleaseTask', command=self.release)
        self.b5 = Button(win, text='List Queue', command=self.enlist_q)
        self.b6 = Button(win, text='Get positions', command=self.get_pos)
        self.b7 = Button(win, text='Enter product in queue', command=self.enque_prod)
        self.b1.place(x=300, y=50)



        self.b3.place(x=150, y=250)
        self.b4.place(x=250, y=250)
        self.b5.place(x=350, y=250)
        self.b6.place(x=430, y=250)
        self.b6.place(x=430, y=250)
        self.b7.place(x=430, y=280)

    def create(self):
        #self.t3.delete(0, 'end')
        txt1=str(self.t1.get())
        txt2=str(self.t2.get())


        self.data_opcua["create_part"] = int(self.t1.get())
        time.sleep(0.7)
        self.data_opcua["create_part"] = 0
        print("Part Created!!!")



    def queue(self):
        task_list = ["" for _ in range(2)]
        task = str(self.t3.get()) + "," + str(self.t4.get())
        task_list.insert((int(self.t2.get()) - 1), task)
        q1.put_nowait(task_list)

    def enque_prod(self):
        #q_product_done.put_nowait(p1)
        pass


    def enlist_q(self):
        print(list(q1.queue))

    def get_pos(self):
        print(data_opcua["machine_pos"])
        print(data_opcua["robot_pos"])
        print(data_opcua["rob_busy"])

    def release(self):
        global tqueue
        #task_list = ["" for _ in range(2)]
        print(list(q1.queue))

        try:
            tqueue = q1.get(False)
            # Opt 1: Handle task here and call q.task_done()
        except queue.Empty:
            # Handle empty queue here
            pass



        #task_list.insert((int(self.t2.get())-1),tqueue)
        self.data_opcua["mobile_manipulator"] = tqueue
        time.sleep(0.7)
        self.data_opcua["mobile_manipulator"] = ['', '', '']

        # data_opcua["mobile_manipulator"] = ['4,7','','']
        # # data_opcua["mobile_manipulator"] = ['m,0,-5000,0', '', '']
        # # data_opcua["mobile_manipulator"] = ['', 's,7', '']
        # time.sleep(0.7)
        # data_opcua["mobile_manipulator"] = ['', '', '']
        print(f"Task relased!!!, {tqueue}")




        #asyncio.run(opcua_client.main(tqueue))





###########################################################

data_opcua = {
            "brand": "Ford",
            "mobile_manipulator": ["", "", ""],
            "rob_busy": [False, False, False],
            "machine_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ],
            "robot_pos": [[0, 0], [0, 0], [0, 0]],
            "create_part": 0,
            "mission": ["", "", "", "", "", "", "", "", "", ""]
    }

x = threading.Thread(target=start_opcua, args=(data_opcua,))
x.start()

window=Tk()
mywin=MyWindow(window, data_opcua)
window.title('Task Release')
window.geometry("600x300+10+10")
window.mainloop()