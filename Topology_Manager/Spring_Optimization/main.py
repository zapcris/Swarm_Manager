import random
#from .utils import Get_Distance_Or_Flow
import sys
# from orderlist_db import database
from tkinter import *

import pandas as pd
from pymongo import MongoClient
from ttkbootstrap.constants import *

from Genetic_Algorithm import run_GA

random.seed(1314141)


# global dframe

def read_orderlist():
    orderlist = []
    sequencelist = []

    cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    db = client.swarm_production
    # cursor = db.productList.find({"name: 12"})
    mycol = db.orderlist.find()
    for x in mycol:
        orderlist.append(x['order_list'])
    # print(orderlist[1][0]['Sequence'])

    for i in range(len(orderlist)):
        for j in range(len(orderlist[i])):
            if i == 0:
                sequencelist.append(orderlist[i][j]['Sequence'])

    print("whole sequence list", sequencelist)
    natch_seq = []
    for i in range(len(sequencelist)):
        natch_seq.append(list(sequencelist[i]))
    print("old batch sequence", natch_seq)

    for i in range(0, len(natch_seq)):
        for j in range(0, len(natch_seq[i])):
            natch_seq[i][j] = int(natch_seq[i][j])
    print("modified batch sequence", natch_seq)


def close():
    # win.destroy()
    root.quit()


def clear():
    del dframe


######### Tkinter UI ###############
root = Tk()
root.geometry('800x600')

btn = Button(root, text='Open the batch sequence excel file', command=run_GA)
btn.pack(side='top')

btn2 = Button(root, text='Close the program', command=close)
btn2.pack(side='bottom')

btn3 = Button(root, text='test MongoDB', command=read_orderlist)
btn3.pack(side='right')

btn3 = Button(root, text='clear dataframe', command=clear)
btn3.pack(side='left')

# dates = pd.date_range('20210101', periods=8)
# dframe = pd.DataFrame(np.random.randn(8,4),index=dates,columns=list('ABCD'))
ini_string = 'SWARM TOPOLOGY MANAGER'
dframe = pd.DataFrame

txt = Text(root)
txt.pack()


class PrintToTXT(object):
    def write(self, s):
        txt.insert(END, s)


sys.stdout = PrintToTXT()

print("The Batch Sequence from the sheet")

print(dframe)

root.mainloop()
