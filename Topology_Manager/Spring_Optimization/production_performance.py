import math
import sys
import random
import numpy as np
import networkx as nx
import pylab as pl
from matplotlib import pyplot as plt
from shapely.geometry import MultiLineString, LineString
from itertools import combinations

Batch_process_times = [5, 8, 10, 12, 7, 9, 13, 10, 12, 10]
def euclidean_dist(x1, y1, x2, y2):
    dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)
    return round(dist)


random.seed(1033)


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def plot_throughput(num, prod_1_time, prod_normal_time, qty, num_cross):
    # Loop through each time step.
    # It is important to simulate each variant before scheduling a total batch
    n_steps = 1000  # number of unit time
    throughput = np.zeros(n_steps)
    loss = 0.0
    prd_cycle_time = prod_normal_time
    ideal_cycle_time = prod_normal_time
    cumulative_throuput = []
    cumulative_ideal_throughput = []
    ideal_throughput = np.zeros(n_steps)
    total_prod_time = 0
    ideal_prod_time = 0

    for i in range(1, n_steps):
        ###Every cycle time induce a random crossing congestion
        if i % prd_cycle_time == 0:
            loss = random.randint(0, num_cross) * 1  ### every crossing induces a single unit time loss
            prd_cycle_time = prod_normal_time + loss
            ideal_cycle_time = prod_normal_time + 0

        if 1 <= i <= prod_1_time:  ### Calculating throughput for the 1st production time.
            total_1st_time = prod_1_time + loss
            throughput[i] = 1 / total_1st_time
            ideal_throughput[i] = 1 / prod_1_time
            cumulative_throuput.append(throughput[i])
            cumulative_ideal_throughput.append(ideal_throughput[i])
        else:  ### calculating throughput for the normal prod time
            throughput[i] = 1 / prd_cycle_time
            ideal_throughput[i] = 1 / ideal_cycle_time
            cumulative_throuput.append(throughput[i])
            cumulative_ideal_throughput.append(ideal_throughput[i])

        if qty <= sum(cumulative_throuput) <= qty + 0.5:
            total_prod_time = i

        if qty <= sum(cumulative_ideal_throughput) <= qty + 0.5:
            ideal_prod_time = i

    snapped_throughput = throughput[:total_prod_time]

    steps = np.arange(0, n_steps, 1)
    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }
    # Plot it!
    plt.plot(steps, throughput)
    plt.title(f'Product variant {num + 1} throughput with total prod time : {total_prod_time} for {qty} qty')
    plt.xlabel('unit time', fontdict=font)
    plt.ylabel('Throughput', fontdict=font)
    plt.savefig(f'charts/throughput/perf_product variant {num + 1}')
    plt.pause(0.05)
    plt.clf()
    return total_prod_time, snapped_throughput, round(total_1st_time), ideal_prod_time


def prod_efficiency(Batch_sequence, pos, Qty, len_graph):
    # print(Batch_sequence)
    edge_list = []
    edge_pos_list = []
    for i in range(len(Batch_sequence)):
        edges = []
        edges_pos = []
        for j in range(len(Batch_sequence[i]) - 1):
            edge = [Batch_sequence[i][j], Batch_sequence[i][j + 1]]
            edge_pos = [pos[Batch_sequence[i][j]], pos[Batch_sequence[i][j + 1]]]
            edges.append(edge)
            edges_pos.append(edge_pos)
        edge_list.append(edges)
        edge_pos_list.append(edges_pos)

    # print(edge_list)
    # print(edge_pos_list)

    multi_strng_list = []

    for pos_seq in edge_pos_list:
        e = MultiLineString(pos_seq)
        multi_strng_list.append(e.geoms)

    # for i in multi_strng_list:
    #     print(i)
    # # crossing is always zero in heirarchial tree graph
    num_crossings = []
    for multi_strng in multi_strng_list:
        c = 0
        for line1, line2 in combinations([line for line in multi_strng], 2):
            if line1.crosses(line2):
                # print(line1.intersection(line2))
                c += 1
                d = 0
        num_crossings.append(c)
    print("no of crossings", num_crossings)
    vel_transport = 2  # speed of the transport robot
    #process_time = 5  ## uniform process time required by workstations

    PI_arr_pt = []
    PI_arr_thr = []
    PI_arr_1sTime = []
    PI_arr_idealT = []
    throughput = []
    ## Find throughput for individual product variants
    for i, (seq, gLen, qty, cross,process_time) in enumerate(zip(Batch_sequence, len_graph, Qty, num_crossings,Batch_process_times)):
        num_workstations = len(seq)
        dist_lastedge = euclidean_dist(pos[seq[-2]][0], pos[seq[-2]][1], pos[seq[-1]][0], pos[seq[-1]][1])
        ct_1st_ptime = (num_workstations * process_time) + (
                gLen / vel_transport)  ## first product doesnot experience congestion
        ct_normal_time = process_time  ## (dist_lastedge / vel_transport)
        PI_prod_time = plot_throughput(i, ct_1st_ptime, ct_normal_time, qty, cross)
        # random_loss = cross * (random.randint(0, qty) * ct_normal_time)
        # print(random_loss)
        ###PI_prod_time = ct_1st_ptime + ((qty - 1) * ct_normal_time) + random_loss - old measurement of stocashtic loss
        PI_arr_pt.append(PI_prod_time[0])
        PI_arr_thr.append(PI_prod_time[1])
        PI_arr_1sTime.append(PI_prod_time[2])
        PI_arr_idealT.append(PI_prod_time[3])

    Batch_prod_time = sum(PI_arr_pt)
    print("production time required array", PI_arr_pt)
    print("production throughput array", len(PI_arr_thr[1]))
    print("production 1st prod time required array", PI_arr_1sTime)
    print("production ideal time array", PI_arr_idealT)

    ### Plot the cumulative graph with coinciding the
    prod_span = 5000

    # for i in range(len(cumulative_throughput)):
    #     cumulative_throughput[i] = random.randint(1,35)

    prod_steps = np.arange(0, prod_span, 1)
    plt.figure()
    # cmap = get_cmap(len(data))
    colors = pl.cm.jet(np.linspace(0, 1, len(Batch_sequence)))
    # Plotting both the curves simultaneously
    offset = 1
    for i in range(len(Batch_sequence)):
        print(f"The troubleshoot is {i}")
        cumulative_throughput = np.zeros(prod_span)
        process_time = Batch_process_times
        if i == 0:
            offset += 0
        else:
            coeff_pTime = PI_arr_idealT[i - 1] / process_time[i-1]
            #print("the calculated coeff prodcut", i+1, coeff_pTime)
            actual_processtime = float(PI_arr_pt[i - 1]) / coeff_pTime
            #print("debug here", float(PI_arr_pt[i - 1]), coeff_pTime)
            #print(f'previous process time is {process_time[i-1]}')
            print(f"the actual process time of product {i+1} is {coeff_pTime}")
            offset += round(Qty[i - 1] * actual_processtime)
            # print(f"Start time of previous product was {PI_arr_pt[i-1]} product and time to produce 1st sample of current product {PI_arr_1sTime[i]}")

        if i == len(Batch_sequence)-1:
            finish_time = PI_arr_pt[i] + offset
        #print(f"product {i + 1} with start {offset} and stop {PI_arr_pt[i] + offset} index")

        #print("ARR", PI_arr_thr[i])
        #print("PT",PI_arr_pt[i])
        'Increase the production span if array dimension error occurs'
        #cumulative_throughput[offset:PI_arr_pt[i] + offset] = PI_arr_thr[i]  # [1:PI_arr_pt[i]]
        #plt.plot(prod_steps, cumulative_throughput, color=colors[i], label=f'P{i + 1} for qty-{Qty[i]} CT-{process_time[i]} time')
        plt.pause(2)

    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Unit Time")
    plt.ylabel("Throughput")
    plt.title(f"Batch Production finished in {finish_time} time")

    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()

    # To load the display window
    plt.savefig(f'charts/throughput/Cumulative production')

    return Batch_prod_time, PI_arr_pt

