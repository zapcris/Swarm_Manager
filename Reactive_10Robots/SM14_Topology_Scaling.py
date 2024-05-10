import math
import numpy as np
import matplotlib.pyplot as plt


def scale_graph_uniformly(coordinates, desired_x_min, desired_x_max, desired_y_min, desired_y_max):
    # Extract x and y values from the coordinates
    x_values, y_values = coordinates[:, 0], coordinates[:, 1]

    # Calculate current range of x and y values
    x_range = np.max(x_values) - np.min(x_values)
    y_range = np.max(y_values) - np.min(y_values)

    # Calculate scaling factors for x and y
    scaling_factor_x = (desired_x_max - desired_x_min) / x_range
    scaling_factor_y = (desired_y_max - desired_y_min) / y_range

    # Scale the x and y values
    scaled_x_values = (x_values - np.min(x_values)) * scaling_factor_x + desired_x_min
    scaled_y_values = (y_values - np.min(y_values)) * scaling_factor_y + desired_y_min

    # Combine scaled x and y values back into coordinates
    scaled_coordinates = np.column_stack((scaled_x_values, scaled_y_values))
    list_scaled_coordinates = []
    for x, y in zip(scaled_x_values, scaled_y_values):
        cord = [x, y]
        list_scaled_coordinates.append(cord)

    print("The Scaling factors are", scaling_factor_x, scaling_factor_y)
    print("list cordinates", list_scaled_coordinates)
    return list_scaled_coordinates, scaled_coordinates



if __name__ == '__main__':

    # Create a sample set of coordinates
    coordinates = np.array(
        [[16, 14], [2, 21], [17, 21], [8, 20], [12, 22], [22, 13], [12, 16], [8, 12], [10, 7], [3, 2]])

    # Desired x and y axis limits
    desired_x_min, desired_x_max = -16000, 16000
    desired_y_min, desired_y_max = 13000, 40000

    # Scale the coordinates
    scaled_coordinates = scale_graph_uniformly(coordinates, desired_x_min, desired_x_max, desired_y_min, desired_y_max)

    # Plot the original and scaled graphs
    plt.plot(coordinates[:, 0], coordinates[:, 1], 'o', label='Original Coordinates')
    plt.plot(scaled_coordinates[:, 0], scaled_coordinates[:, 1], 'o', label='Scaled Coordinates')
    plt.title('Original and Scaled Coordinates')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.xlim(desired_x_min, desired_x_max)
    plt.ylim(desired_y_min, desired_y_max)
    plt.show()

