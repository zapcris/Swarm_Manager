import datetime

data_snapshot = []
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def collect_data():
    now = datetime.datetime.now()
    products = [[1,1],[2,2]]
    data = [now, products]
    print(data_snapshot)
    for ele in a:
        data_snapshot.append(data)
        #data_snapshot[1].append(curr_time)
        #data_snapshot[1].append(ele)
    print(data_snapshot)
    for i in range(len(data_snapshot)):
        print(data_snapshot[i][0], data_snapshot[i][1])

    new_data = [0 for o in data_snapshot]
    for i, (snap, data) in enumerate(zip(data_snapshot, new_data)):
        d = [snap, a[i]]
        new_data[i] = d

    print(new_data)
    numbers = []
    test_string = "PV-1_PI-1"
    for char in test_string:
        if char.isdigit():
            numbers.append(int(char))

    print(numbers)
    data2 = [["PV-1_PI-1", 100], ["PV-2_PI-2", 200]]
    throughput_data = [0 for o in data_snapshot]
    for i, (snap, thr_data) in enumerate(zip(data_snapshot, throughput_data)):
        throughput = 0
        for x in data2:
            p = []
            for char in x[0]:
                if char.isdigit():
                    p.append(int(char))
                if p in snap[1]:
                    throughput += 10 / x[1]
        d = [snap, throughput]
        print(d)
        throughput_data[i] = d

    for thr in throughput_data:
        print(thr)

collect_data()
