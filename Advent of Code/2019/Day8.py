from aocscrapper import get_AoC_input
import numpy as np
import matplotlib.pyplot as plt

days_input = np.array([int(char) for char in get_AoC_input(2019, 8).strip()])

height = 6
width = 25
num_pixels = height * width
layer_arrays = days_input.reshape((-1, num_pixels))  # since we don't know how many layers there are, we use -1 for the first dimension

layer_digit_count = list()
for layer in layer_arrays:
    # layer == ? returns a boolean with Trues (which count as 1s, i.e.non-zeros) in the positions where ? was present in the layer.
    # Python assigns True a value of 1, so summing these Trues gives the total count of ?
    layer_digit_count.append({0: sum(layer == 0), 1: sum(layer == 1), 2: sum(layer == 2)})

zeros_per_layer = [layer[0] for layer in layer_digit_count]
least_zeros_layer_digit_counts = layer_digit_count[zeros_per_layer.index(min(zeros_per_layer))]
print("Part 1:", least_zeros_layer_digit_counts[1] * least_zeros_layer_digit_counts[2])

final_decoded_image = list()
for i in range(num_pixels):
    pixel_value_undetermined = True
    layer_depth = 0
    while pixel_value_undetermined:
        layer_pixel_data = layer_arrays[layer_depth][i]
        if layer_pixel_data != 2:  # i.e. pixel's value is 0 or 1
            final_decoded_image.append(layer_pixel_data)
            pixel_value_undetermined = False
        else:
            layer_depth += 1

final_decoded_image = np.array(final_decoded_image).reshape(height, width)
plt.imshow(final_decoded_image, cmap="binary")
print("Part 2: (see matplotlib window)")
plt.show()
