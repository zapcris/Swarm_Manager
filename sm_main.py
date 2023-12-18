import numpy as np

prod_span = 3000

cumulative_throughput = np.zeros(prod_span)

arr = [100,200,300,400,500,600,700,800,900,1000,1200,1300,1400,1500,1600]


offset = 1

for i in range(3):
    cumulative_throughput[offset:arr[i] + offset] = 10
    print(cumulative_throughput)
