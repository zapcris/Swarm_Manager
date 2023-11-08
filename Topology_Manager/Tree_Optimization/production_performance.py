import math
import sys
import random
import numpy as np
import networkx as nx
import pylab as pl
from matplotlib import pyplot as plt
from shapely.geometry import MultiLineString, LineString
from itertools import combinations

Batch_process_times = [5, 8, 10, 12, 7, 9, 13]
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
        num_crossings.append(0)
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
    prod_span = 3000

    # for i in range(len(cumulative_throughput)):
    #     cumulative_throughput[i] = random.randint(1,35)

    prod_steps = np.arange(0, prod_span, 1)
    plt.figure()
    # cmap = get_cmap(len(data))
    colors = pl.cm.jet(np.linspace(0, 1, len(Batch_sequence)))
    # Plotting both the curves simultaneously
    offset = 1
    for i in range(len(Batch_sequence)):
        cumulative_throughput = np.zeros(prod_span)
        process_time = Batch_process_times
        if i == 0:
            offset += 0
        else:

            coeff_pTime = PI_arr_idealT[i - 1] / process_time[i-1]
            #print("the calculated coeff prodcut", i+1, coeff_pTime)
            #actual_processtime = float(PI_arr_pt[i - 1]) / coeff_pTime
            actual_processtime = process_time[i-1] ## for tree topology
            print(f"the actual process time of product {i+1} is {coeff_pTime}")
            offset += round(Qty[i - 1] * actual_processtime) ## for tree topology its is original process time
            # print(f"Start time of previous product was {PI_arr_pt[i-1]} product and time to produce 1st sample of current product {PI_arr_1sTime[i]}")
        if i == len(Batch_sequence)-1:
            finish_time = PI_arr_pt[i] + offset
        print("product with start and stop index", i + 1, offset, PI_arr_pt[i] + offset)
        cumulative_throughput[offset:PI_arr_pt[i] + offset] = PI_arr_thr[i]  # [1:PI_arr_pt[i]]
        plt.plot(prod_steps, cumulative_throughput, color=colors[i], label=f'P{i + 1} for qty-{Qty[i]} CT-{process_time[i]}')
        # plt.pause(0.05)

    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Unit Time")
    plt.ylabel("Throughput")
    plt.title(f"Batch Production finished in {finish_time} time")

    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()

    # To load the display window
    plt.savefig(f'charts/throughput/Cumulative production')
    plt.clf()

    return Batch_prod_time, PI_arr_pt

# print(stochastic_throughput(Batch, G_pos, Qty_order, fitness_len))

#
# "Calculate the throughput of the system"
# seq = [1, 5, 9, 10, 2, 11, 13, 15, 7, 20]
# len_graph = 2000  # length of the traversal in the graph
# vel_transport = 2  # speed of the transport robot
# process_time = 5  ## uniform process time required by workstations
# num_workstations = 10
# dist_lastedge = euclidean_dist(G_pos[seq[-2]][0], G_pos[seq[-2]][1], G_pos[seq[-1]][0], G_pos[seq[-1]][1])
# qty = 50
# ct_1st_prod = (num_workstations * process_time) + (
#             len_graph / vel_transport)  ## first product doesnot experience congestion
# ct_normal_product = process_time + (dist_lastedge / vel_transport)
# random_loss = (random.randint(0, qty) * ct_normal_product)
# total_cycle_time = ct_1st_prod + ((qty - 1) * ct_normal_product) + random_loss
# print(ct_1st_prod)
# print(ct_normal_product)
# print(random_loss)
# print(total_cycle_time)
#
# sys.exit()
# "Draw graph of the subject"
#
# G = nx.MultiGraph()
# G.add_nodes_from(Batch_sequence)
# G.add_edges_from(edge_list)
# plt.figure()
# plt.title(f"The plot belongs to initial population {i + 1} ")
# nx.draw(G, G_pos, with_labels=True)
# plt.grid(True)
# plt.pause(0.05)
# plt.show()

# multiline = MultiLineString([[(614633.1598889811, 6614684.232110311), (614585.0239559432, 6615176.69973293),
#                               (614244.3696605981, 6615210.024609649), (614174.0171430812, 6615058.211282375)],
#                              [(614849.2836035677, 6614574.273030049), (615163.3363697577, 6614591.624011607),
#                               (615477.7302093033, 6614608.993836996), (615475.8039105758, 6614892.159749944),
#                               (615474.6318041045, 6615064.459401229), (614967.3343471865, 6615119.389699113)],
#                              [(615054.1363645532, 6614185.399992246), (615163.3363697577, 6614591.624011607),
#                               (615227.7403992868, 6614831.207001455), (615475.8039105758, 6614892.159749944),
#                               (615835.3545208545, 6614980.506471327), (615867.958614701, 6615021.869873968),
#                               (615474.6318041045, 6615064.459401229), (615474.2581286087, 6615119.389699113),
#                               (615286.7657710963, 6615227.024200648)],
#                              [(616057.5676853136, 6615001.338955494), (615867.958614701, 6615021.869873968),
#                               (616067.9839273975, 6615275.633330373)]])
#
# for line1, line2 in combinations([line for line in multiline], 2):
#     if line1.intersects(line2):
#         print(line1.intersection(line2))
#
# line1 = LineString([(0, 0), (5, 5)])
#
# line2 = LineString([(5, 0), (0, 5)])
#
# line3 = LineString([(1, 0), (5, 4)])
#
# line4 = LineString([(4, 0), (0, 4)])
#
# # print(line1.intersection(line4))
# if line1.intersects(line3):
#     print("done")
#
# "Testing the edges "
#
# total_edges = MultiLineString([[(0, 0), (5, 5)],
#                                [(5, 0), (0, 5)],
#                                [(1, 0), (5, 4)],
#                                [(4, 0), (0, 4)],
#                                ])
# count = 0
# for line1, line2 in combinations([line for line in total_edges], 2):
#
#     if line1.crosses(line2):
#         print(line1.intersection(line2))
#         count += 1
# print(count)


## graph plot
# n_steps = 100
# prd_cycle_time = PI_arr_pt[0] / Qty[0]
# throughput = np.zeros(n_steps)
#
# # Loop through each time step.
# flip = []
# for i in range(8):
# #     # Flip a coin.
#     f= np.random.rand()
#     flip.append(f)
# print(sum(flip))
#
#
# font = {'family': 'serif',
#         'color': 'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# for i in range(1, n_steps):
#     if i >=1 and i <= 35:
#         throughput[i] = 1 / 35
#     else:
#         throughput[i] = 1 / prd_cycle_time
# steps = np.arange(0, n_steps, 1)
# # Plot it!
# plt.plot(steps, throughput)
# plt.title('product instance 1 throughput')
# plt.xlabel('unit time', fontdict=font)
# plt.ylabel('Throughput', fontdict=font)
#
# plt.show()
