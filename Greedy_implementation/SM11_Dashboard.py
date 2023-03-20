from datetime import datetime
from time import sleep

import matplotlib.pyplot as plt

from Greedy_implementation.SM10_Product_Task import Sink, Transfer_time, Process_time, Source, Product


def display_cycletime():
    return None


def production_time(Finished_products):
    labels = []
    product_times = []
    batch_stime = datetime
    batch_etime = datetime
    # batch_time = float
    for i, product in enumerate(Finished_products):
        #### Evaluate labels for pie chart #######
        # l = "P_variant:" + str(product.pv_Id) + "," + "P_instance:" + str(product.pi_Id)
        l = f"Product (variant):{product.pv_Id} (instance):{product.pi_Id}"
        labels.append(l)
        prod_etime = datetime
        prod_stime = datetime

        if i == 0:

            for obj in product.tracking:
                tdiff1 = float
                if obj.sts == "Source":
                    batch_stime = obj.tstamp
                    prod_stime = obj.tstamp
                elif obj.sts == "Sink":
                    prod_etime = obj.tstamp
            tdiff1 = (prod_etime - prod_stime).total_seconds()
            product_times.append(tdiff1)

        elif i != 0 and i != -1:
            tdiff2 = float
            for obj in product.tracking:
                if obj.sts == "Sink":
                    prod_stime = obj.tstamp
                elif obj.sts == "Sink":
                    prod_etime = obj.tstamp
            tdiff2 = (prod_etime - prod_stime).total_seconds()
            product_times.append(tdiff2)

        elif i == -1:
            tdiff3 = float
            for obj in product.tracking:
                if obj.sts == "Sink":
                    batch_etime = obj.tstamp
                    prod_stime = obj.tstamp
                elif obj.sts == "Sink":
                    prod_etime = obj.tstamp
            tdiff3 = (prod_etime - prod_stime).total_seconds()
            product_times.append(tdiff3)

    batch_time = (batch_etime - batch_stime).total_seconds()

    title = f"Total Batch product time {batch_time}"

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    # labels = ['Civil', 'Electrical', 'Mechanical', 'Chemical']
    # sizes = [15, 50, 45, 10]

    fig, ax = plt.subplots()
    ax.pie(product_times, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title(title)

    plt.show()


#### Test Charts #######

a = Transfer_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=0, drop=0, tr_no=1)
b = Process_time(stime=datetime.now(), etime=datetime.now(), dtime=0, wk_no=1)
c = Source(tstamp=datetime.now())
p1 = Product(pv_Id=1, pi_Id=1, task_list=[], inProduction=True, finished=False,
             last_instance=3, robot=0, wk=0, released=False, tracking=[])
p2 = Product(pv_Id=1, pi_Id=2, task_list=[], inProduction=True, finished=False,
             last_instance=3, robot=0, wk=0, released=False, tracking=[])
p3 = Product(pv_Id=2, pi_Id=1, task_list=[], inProduction=True, finished=False,
             last_instance=3, robot=0, wk=0, released=False, tracking=[])
p4 = Product(pv_Id=1, pi_Id=2, task_list=[], inProduction=True, finished=False,
             last_instance=3, robot=0, wk=0, released=False, tracking=[])

p1.tracking.append(c)
p1.tracking.append(a)
p1.tracking.append(b)
p2.tracking.append(c)
p2.tracking.append(a)
p2.tracking.append(b)
p3.tracking.append(c)
p4.tracking.append(c)
sleep(5)
s1 = Sink(tstamp=datetime.now())
p1.tracking.append(s1)
sleep(2)
s2 = Sink(tstamp=datetime.now())
p2.tracking.append(s2)
sleep(2)
s3 = Sink(tstamp=datetime.now())
p2.tracking.append(s3)
sleep(2)
s4 = Sink(tstamp=datetime.now())
p2.tracking.append(s4)

finish_products = [p1, p2, p3, p4]
production_time(finish_products)

# a.calc_time()
# b.calc_time()

# d = Sink(tstamp=datetime.now())
