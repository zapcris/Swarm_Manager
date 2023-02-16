import asyncio
from tkinter import *
import queue
import opcua_client
q1 = queue.Queue()
class MyWindow:

    def __init__(self, win):
        self.lbl1=Label(win, text='Robot Name')
        self.lbl2=Label(win, text='Start position')
        self.lbl4 = Label(win, text='End Position')
        self.lbl3=Label(win, text='Result')
        self.t1=Entry(bd=3)
        self.t2=Entry()
        self.t3=Entry()
        self.t4= Entry()
        self.btn1 = Button(win, text='Add')
        self.btn2=Button(win, text='Subtract')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=20, y=100)
        self.t2.place(x=100, y=100)
        self.lbl4.place(x=250, y=100)
        self.t4.place(x=350, y=100)
        self.b1=Button(win, text='Create', command=self.add)
        self.b3 = Button(win, text='AppendTask', command=self.insert)
        self.b4 = Button(win, text='ReleaseTask', command=self.release)
        self.b2=Button(win, text='Clear ')
        self.b2.bind('<Button-1>', self.sub)
        self.b1.place(x=100, y=150)
        self.b2.place(x=200, y=150)
        self.lbl3.place(x=100, y=200)
        self.t3.place(x=200, y=200)
        self.b3.place(x=150, y=250)
        self.b4.place(x=250, y=250)

    def add(self):
        self.t3.delete(0, 'end')
        txt1=str(self.t1.get())
        txt2=str(self.t2.get())
        txt3=str(self.t4.get())
        result=txt1+","+txt2+","+txt3
        self.t3.insert(END, str(result))
    def sub(self, event):
        self.t3.delete(0, 'end')
        self.t3.clear()
        self.t3.insert(END, str(self.t3))

    def insert(self):
        task = str(self.t3.get())
        q1.put(task)

    def release(self):
        while not q1.empty():
            tqueue = q1.get()
            print("The value is ", tqueue)

        asyncio.run(opcua_client.main(tqueue))

window=Tk()
mywin=MyWindow(window)
window.title('Task Release')
window.geometry("600x300+10+10")
window.mainloop()