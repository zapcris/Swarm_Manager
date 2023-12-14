import asyncio
import sys
from datetime import datetime, timedelta
from time import sleep
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
from Reactive_10Robots.SM10_Product_Task import Sink, Transfer_time, Process_time, Source, Product, Waiting_time


async def production_time(Finished_products):
    labels = []
    product_times = []
    batch_stime = Finished_products[0].tracking[0].tstamp
    batch_etime = Finished_products[-1].tracking[-1].tstamp
    b_time = (batch_etime - batch_stime).total_seconds()
    batch_time = timedelta(seconds=b_time)
    production_legend = []
    product_sts = []

    file_time = dt.datetime.fromtimestamp(os.path.getmtime(__file__))
    curr_time = file_time.strftime("%d_%m_%Y_%H_%M")
    folder_name = "results/" + curr_time
    print("geneated folder name", folder_name)
    ### Create folder for saving plots###
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i, product in enumerate(Finished_products):
        #### Evaluate labels for pie chart #######
        # l = "P_variant:" + str(product.pv_Id) + "," + "P_instance:" + str(product.pi_Id)
        l = f"var_{product.pv_Id} and inst_{product.pi_Id}"
        labels.append(l)
        wait_time = 0
        travel_time = 0
        process_time = 0
        prod_stat = []

        for obj in product.tracking:
            if obj.sts == "Source":
                prod_stime = obj.tstamp

            elif obj.sts == "Transfer":
                travel_time += obj.dtime

            elif obj.sts == "Wait":
                wait_time += obj.dtime

            elif obj.sts == "Process":
                process_time += obj.dtime

            elif obj.sts == "Sink":
                prod_etime = obj.tstamp

        prod_stat.append(travel_time)
        prod_stat.append(wait_time)
        prod_stat.append(process_time)
        product_sts.append(prod_stat)
        tdiff = (prod_etime - prod_stime).total_seconds()
        product_times.append(tdiff)
    print(product_sts)

    ## Create pie chart for production overview###
    for l, p in zip(labels, product_times):
        d = f"{p} sec {l}"
        production_legend.append(d)
    main_title = f"Production Runtime for: {batch_time}"
    main_fname = "Main_Statistics"
    await pie_chart(elements=production_legend, f_name=main_fname, folder=folder_name)
    # pie_chart2(elements=production_legend, title=main_title)

    #### Create pie chart for product overview###
    for i, (status, label, times) in enumerate(zip(product_times, labels, product_sts)):
        product_legend = []
        title = f"Product {label} time for {status} seconds"
        print(title)
        d1 = f"{times[0]} Transfer"
        d2 = f"{times[1]} Wait"
        d3 = f"{times[2]} Process"
        product_legend = [d1, d2, d3]
        print(product_legend)
        await pie_chart(elements=product_legend, f_name=label, folder=folder_name)
        # pie_chart2(elements=production_legend, title=title)


##Function to plot stats##
async def pie_chart2(elements, title):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    data = [float(x.split()[0]) for x in elements]
    times = [x.split()[-1] for x in elements]

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, times,
              title="Legend",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize="x-small",
              )

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(title)
    plt.show()


##Function to save stats##
async def pie_chart(elements, f_name, folder):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    data = [float(x.split()[0]) for x in elements]
    times = [x.split()[-1] for x in elements]

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, times,
              title="Legend",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize="x-small",
              )

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(f_name)
    f_dir = f"{folder}/{f_name}.pdf"
    print("The filename", f_dir)
    plt.savefig(f_dir)


def func(pct, allvals):
    absolute = int(np.round(pct / 100. * np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} seconds)"


async def main():
    task = asyncio.create_task(production_time(finish_products))
    await asyncio.gather(task)


###### Dashboard Test ###############

if __name__ == "__main__":
    start_time = datetime.now()
    sleep(2)
    stop_time = datetime.now()
    diff = (stop_time - start_time).total_seconds()
    print(diff)

    #### Test Charts #######

    a = Transfer_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=0, drop=0, tr_no=1)
    b = Process_time(stime=datetime.now(), etime=datetime.now(), dtime=0, wk_no=1)
    c = Source(tstamp=datetime.now())
    w = Waiting_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=0, drop=0, tr_no=1)
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
    w.calc_time()
    p1.tracking.append(w)
    s1 = Sink(tstamp=datetime.now())
    p1.tracking.append(s1)
    sleep(2)
    s2 = Sink(tstamp=datetime.now())
    p2.tracking.append(s2)
    sleep(2)
    w.calc_time()
    p3.tracking.append(w)
    s3 = Sink(tstamp=datetime.now())
    p3.tracking.append(s3)
    sleep(2)
    s4 = Sink(tstamp=datetime.now())
    p4.tracking.append(s4)

    finish_products = [p1, p2, p3, p4]

    start = p1.tracking[0].tstamp

    stop = p4.tracking[-1].tstamp
    d = (stop - start).total_seconds()

    asyncio.run(main())

    # a.calc_time()
    # b.calc_time()

    # d = Sink(tstamp=datetime.now())
