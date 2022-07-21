def soft_instance_input(class_name, instance_num):
    """
    Read instance class -> input
    Read file text which represents the instance of the problem

    Args:
    :param class_name: Name of instance class
    :param instance_num:
    :return dict
    """

    f = open("../data_instances/Class {}/p{}.txt".format(class_name, instance_num), "r")
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


def get_copy_version(current_solution):
    """
    Get a copy version of the current solution which has type as a list of lists "[[], [], ...]"
    :param current_solution:
    :return: list of lists ("[[], [], ...]")
    """

    res = []
    n = len(current_solution)

    for i in range(0, n):
        tmp_val = current_solution[i]
        res.append(tmp_val)

    return res


def get_random_solution(size):
    """
    Generate a random solution
    :param size: size of one dimension of a solution
    :return: list of lists
    """
    import random
    pos = []
    for i in range(0, size):
        pos.append(random.randint(0, size - 1))

    return pos

