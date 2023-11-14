import sys

from scipy.interpolate import griddata
from sklearn.preprocessing import MinMaxScaler

selected_top = [[14, 0], [8, -2.8], [14, -8.399999999999999], [3, -2.8], [14, -2.8],
                [20, -2.8], [10, -5.6], [7, -11.2], [14, -14.0], [18, -5.6], [24, -5.6],
                [21, -11.2], [14, -16.8], [25, -2.8], [14, -19.6], None, [4, -5.6], None,
                [14, -22.400000000000002], [14, -25.200000000000003]]

scaled_top = []
min_x, max_x, min_y, max_y = 0, 0, 0, 0
for value in selected_top:
    if value != None:
        if value[0] < min_x :
            min_x = value[0]

        if value[0] > max_x :
            max_x = value[0]

        if value[1] < min_y :
            min_y = value[1]

        if value[1] > max_y :
            max_y = value[1]

    # print(f"min x {min_x} min y {min_y}")
    # print("position old data structure:", pos)
min_new_x = 0
max_new_x = 34000
min_new_y = -34000
max_new_y = 16000
scale = 1000
print("minimum x value", min_x)
print("maximum x value", max_x)
print("minimum y value", min_y)
print("maximum y value", max_y)
for value in selected_top:
    if value != None:
        scaled_top.append((scale * (value[0] + abs(min_x)), scale * (value[1] + abs(min_y))))

data = [[14, 0], [8, -2.8], [14, -8.399999999999999], [3, -2.8], [14, -2.8],
                [20, -2.8], [10, -5.6], [7, -11.2], [14, -14.0], [18, -5.6], [24, -5.6],
                [21, -11.2], [14, -16.8], [25, -2.8], [14, -19.6],[4, -5.6],
                [14, -22.400000000000002], [14, -25.200000000000003]]


scaler = MinMaxScaler(feature_range=(0,40000))
print(scaler.fit(data))
#print(scaler.data_max_)
print(scaler.transform(data))

print(scaler.transform([[10, 10]]))

pos_str = str(int(99.0)) + "," + str(int(99.0)) + "d"

print(pos_str)