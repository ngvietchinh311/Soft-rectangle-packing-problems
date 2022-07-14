import sys
from pytube import YouTube, Channel
import itertools
import utils.utilities as utils


def get_copy_version(current_solution):
    res = []
    for k in range(0, n):
        tmp_res = []
        for i in range(0, n):
            tmp_res.append(current_solution[k][i])
        res.append(tmp_res)
    return res


n = 3
L1 = 10
L2 = 15
a = [26, 12, 8]
x = [0, 1, 1]
# x = [1, 2, 1, 1, 3]


def calculate_solution_value(current_sol):
    global n, L1, L2, a, x

    res = 0

    for k in range(0, n):
        # Variable hold the layer's area
        tmp_a = 0

        # Calculate the layer's area by adding the existing recs in that layer
        for i in range(0, n):
            if current_sol[k][i] == 1:
                tmp_a += a[i]
        # Variable hold lengths of recs that in layer 'k + 1'
        tmp_l = [res]
        k_height = L2 * tmp_a / (L1 * L2)

        for i in range(0, n):
            if current_sol[k][i] == 1:
                tmp_l.append(2 * (k_height + (a[i] / k_height)))

        res = max(tmp_l)
    return res


def change_layer_neighborhood(current_solution):
    """
    Find all 'neighbors' of current solution by changing position of 1 rectangle (from 1 layer to another layer)
    :return: list of objects typed 'x'
    """
    global n, L1, L2, a, x

    res = []

    for k in range(0, n):
        for i in range(0, n):
            if current_solution[k][i] == 1:
                for check in range(0, n):
                    if current_solution[check][i] == 1:
                        continue
                    tmp_x = get_copy_version(current_solution)
                    tmp_x[k][i] = 0
                    tmp_x[check][i] = 1
                    res.append(tmp_x)
    return res


def get_random_solution():
    """
    Generate a random solution
    :return: list of lists
    """
    import random
    global n, L1, L2, a, x
    pos = []
    res = []
    for i in range(0, 10):
        pos.append(random.randint(0, 9))

    for k in range(0, 10):
        tmp_res = []
        for i in range(0, 10):
            tmp_res.append(0)
        res.append(tmp_res)

    for i in range(0, 10):
        res[pos[i]][i] = 1

    return res

# def get_recs_layers(current_solution):
#     res = {}
#     for k in range(0, n):
#         for i in range(0, n):
#             if x[k][i] == 1:
#                 res.update({})


def swap_sol(current_solution):
    global n, L1, L2, a, x

    res = []

    layer = {}

    for k in range(0, n):
        for i in range(0, n):
            if current_solution[k][i] == 1:
                layer.update({i: k})

    res_d = {}

    for i in range(0, n):
        res_d.update({i: []})

    for i in range(0, n):
        tmp_list = list(range(0, n))
        tmp_list.remove(i)
        for j in tmp_list:
            if layer[j] == layer[i]:
                continue
            res_d[i].append(j)

    for i in range(0, n):
        for j in res_d[i]:
            tmp_x = get_copy_version(current_solution)
            tmp_x[layer[i]][i] = 0
            tmp_x[layer[j]][i] = 1

            tmp_x[layer[j]][j] = 0
            tmp_x[layer[i]][j] = 1

            res.append(tmp_x)

    print(res_d)

    return res


def split_layer(current_solution):
    global n

    layer_dict = {}
    res = []

    for k in range(0, n):
        layer_dict.update({k: []})

    for k in range(0, n):
        for i in range(0, n):
            if x[k][i] == 1:
                layer_dict[k].append(i)

    blank_layer = None
    for k in range(0, n):
        if sum(current_solution[k]) == 0:
            blank_layer = k
            break
    if blank_layer is None:
        return []

    for k in range(0, n):
        layer_length = len(layer_dict[k])
        if layer_length >= 2:
            for l in range(0, layer_length + 1):
                for sub_set in itertools.combinations(layer_dict[k], l):
                    if len(sub_set) > int(len(layer_dict[k]) / 2) or len(sub_set) == 0:
                        continue
                    for i in list(sub_set):
                        tmp_x = get_copy_version(current_solution)
                        tmp_x[k][i] = 0
                        tmp_x[blank_layer][i] = 1

                        res.append(tmp_x)

    return res


def merge_layer_neighbourhood(current_solution):
    global n
    res = []

    for k in range(0, n):
        if sum(current_solution[k]) == n:
            return []

    blank_layer = [0] * n

    for k in range(0, n):
        layer_list = list(range(0, n))
        layer_list.remove(k)
        for tmp_layer in layer_list:
            merge_layer = [i + j for i, j in zip(current_solution[k], current_solution[tmp_layer])]
            tmp_x = get_copy_version(current_solution)
            tmp_x[k] = merge_layer
            tmp_x[tmp_layer] = blank_layer

            res.append(tmp_x)

    return res


def swap_layer_neighborhood_v2(current_solution):
    """
    Find all neighbors of current solution by swapping 2 rectangles in 2 different layers
    :param current_solution:
    :return: list of solution
    """
    global n

    res = []

    recs = {}

    for i in range(0, n):
        recs.update({i: []})

    for i in range(0, n):
        tmp_list = list(range(0, n))
        tmp_list.remove(i)
        for j in tmp_list:
            if current_solution[j] == current_solution[i]:
                continue
            recs[i].append(j)

    for i in range(0, n):
        for j in recs[i]:
            tmp_x = utils.get_copy_version(current_solution)
            tmp_x[i] = current_solution[j]
            tmp_x[j] = current_solution[i]
            res.append(tmp_x)

    return res


def split_layer_neighbourhood(current_solution):
        """
        Find all neighbors of current solution by splitting layer into 2 smaller layers
        :param current_solution:
        :return: list of solutions
        """
        global n

        layer_dict = {}
        res = []

        for k in range(0, n):
            layer_dict.update({k: []})

        for i in range(0, n):
            layer_dict[current_solution[i]].append(i)

        blank_layer = None
        for k in range(0, n):
            if len(layer_dict[k]) == 0:
                blank_layer = k
                break
        if blank_layer is None:
            return []

        for k in range(0, n):
            if len(layer_dict[k]) < 2:
                continue
            else:
                for L in range(0, len(layer_dict[k]) + 1):
                    for subset in itertools.combinations(layer_dict[k], L):
                        if len(subset) > len(layer_dict[k]) / 2 or len(subset) == 0:
                            continue

                        replaced_list = list(subset)
                        tmp_x = utils.get_copy_version(current_solution)
                        for tmp_var in replaced_list:
                            tmp_x[tmp_var] = blank_layer
                        res.append(tmp_x)

        return res


def merge_layer_neighbourhood_v2(current_solution):
        global n
        res = []

        layer_dict = {}

        for k in range(0, n):
            layer_dict.update({k: []})

        for i in range(0, n):
            layer_dict[current_solution[i]].append(i)

        for k in range(0, n):
            if len(layer_dict[k]) == 0:
                continue
            merge_layers = list(range(0, n))
            merge_layers.remove(k)
            for tmp_layer in merge_layers:
                if len(layer_dict[tmp_layer]) == 0:
                    continue
                print(tmp_layer)
                tmp_x = utils.get_copy_version(current_solution)
                for i in layer_dict[tmp_layer]:
                    tmp_x[i] = k
                res.append(tmp_x)

        return res


# res = merge_layer_neighbourhood_v2(x)
# for i in res:
#     print(i)

# stuff = [1, 2, 3, 4]
#
# count = 0
# for L in range(0, len(stuff)+1):
#     for subset in itertools.combinations(stuff, L):
#         if len(subset) > len(stuff) / 2 or len(subset) == 0:
#             continue
#         print(list(subset))
#         count += 1

# get_random_solution()

tmp_list = list(range(1, 11))

print(tmp_list)
tmp_list.pop(0)
print(tmp_list)
