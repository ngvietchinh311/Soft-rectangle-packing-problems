def soft_instance_input(instance_class):
    """
        Read instance class -> input
        Read file text which represents the instance of the problem

        Args:
            instance_class (list): contains 2 values. One represents class of the instance,
                                 the other is equivalent to number of the class instances.
    """

    f = open("../data_instances/Class {}/p{}.txt".format(instance_class[0], instance_class[1]), "r")
    res = {}
    basic_info = f.readline().split(' ')
    res['n'] = int(basic_info[0])
    res['L1'] = int(basic_info[1])
    res['L2'] = int(basic_info[2])
    a = []
    for i in f:
        try:
            a.append(int(i))
        except:
            continue
    res['a'] = a

    return res


'''
    Input get from instance
'''
inp = soft_instance_input(['U', '01'])

n = inp['n']
L1 = inp['L1']
L2 = inp['L2']
a = inp['a']

'''
    Vars:
        x: list of lists which contains binary value (0, 1).
            x[k][i] = 0 means that rectangle 'i+1' is not in layer 'k+1', 1 means otherwise.
'''
x = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def get_copy_version(current_solution):
    res = []
    for k in range(0, n):
        tmp_res = []
        for i in range(0, n):
            tmp_res.append(current_solution[k][i])
        res.append(tmp_res)
    return res


def get_current_number_of_layers():
    global n, L1, L2, a, x

    res = 0
    for k in range(0, n):
        if sum(x[k]) >= 1:
            res += 1
    return res


def calculate_solution_value(current_sol):
    global n, L1, L2, a

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


def print_solution():
    global n, L1, L2, a, x

    for i in range(0, n):
        for k in range(0, n):
            print(x[i][k], end='    ')
        print()


"""
Set up neiborhood functions
"""


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


def iterated_local_search():
    n_iterations = 10
    start_pt = x
    current_pt = start_pt
    best = calculate_solution_value(start_pt)
    for i in range(0, n_iterations):
        # x : start solution
        tmp_best = best
        tmp_current_pt = current_pt
        neighbours = change_layer_neighborhood(tmp_current_pt)
        for neighbour in neighbours:
            value_check = calculate_solution_value(neighbour)
            if value_check < tmp_best:
                tmp_best = value_check
                tmp_current_pt = neighbour
            else:
                continue
        if tmp_best < best:
            current_pt = tmp_current_pt
            best = tmp_best
            print("{}: {}".format(str(i), best))

    pass


# current_pt = x
# print(calculate_solution_value(x))
# neighbors = change_layer_neighborhood(current_pt)
# val = []
# for neighbor in neighbors:
#     tmp_var = calculate_solution_value(neighbor)
#     val.append(tmp_var)
#
# print(min(val))

iterated_local_search()


# for j in x:
#     print(j)
# print("-------------------------------------------------")
# tmp_exe = change_layer_neighborhood()
# for i in tmp_exe:
#     for j in i:
#         print(j)
#     break
# print("-------------------------------------------------")
# for j in x:
#     print(j)
# print(len(tmp_exe))
