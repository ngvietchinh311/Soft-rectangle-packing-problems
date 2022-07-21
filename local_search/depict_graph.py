import matplotlib.pyplot as plt
from local_search_v2 import LocalSearch
import utils.utilities as utils
import numpy as np


def get_correlation_between_number_of_iterations_and_the_results(class_name: str, class_num: str, n_iterations=50):
    ls = LocalSearch(class_name, class_num)

    n = ls.inp["n"]

    res = []
    y = []
    x = []

    start_pt = utils.get_random_solution(n)
    current_pt = start_pt
    best = ls.calculate_solution_value(start_pt)

    for i in range(0, n_iterations):
        tmp_best = best
        tmp_current_pt = current_pt
        best_tmp_current_pt = current_pt

        neighbours = ls.change_layer_neighborhood(tmp_current_pt)
        neighbours.extend(ls.swap_layer_neighborhood(tmp_current_pt))
        # neighbours.extend(ls.split_layer_neighbourhood(tmp_current_pt))
        neighbours.extend(ls.merge_layer_neighbourhood(tmp_current_pt))
        for neighbour in neighbours:
            value_check = ls.calculate_solution_value(neighbour)
            if value_check < tmp_best:
                tmp_best = value_check
                best_tmp_current_pt = neighbour
            else:
                continue

        x.append(i)
        y.append(tmp_best)

        if tmp_best < best:
            current_pt = best_tmp_current_pt
            best = tmp_best
        else:
            break

    res.append(best)

    return [x, y]


def get_correlation_between_number_of_restarts_and_the_results(class_name: str, class_num: str, n_iterations=3,
                                                               n_restarts=4):
    ls = LocalSearch(class_name, class_num)

    n = ls.inp["n"]

    res = []
    y = []
    x = []

    for turn in range(0, n_restarts):
        start_pt = utils.get_random_solution(n)
        current_pt = start_pt
        best = ls.calculate_solution_value(start_pt)

        for i in range(0, n_iterations):
            tmp_best = best
            tmp_current_pt = current_pt
            best_tmp_current_pt = current_pt

            neighbours = ls.change_layer_neighborhood(tmp_current_pt)
            neighbours.extend(ls.swap_layer_neighborhood(tmp_current_pt))
            # neighbours.extend(ls.split_layer_neighbourhood(tmp_current_pt))
            neighbours.extend(ls.merge_layer_neighbourhood(tmp_current_pt))
            for neighbour in neighbours:
                value_check = ls.calculate_solution_value(neighbour)
                if value_check < tmp_best:
                    tmp_best = value_check
                    best_tmp_current_pt = neighbour
                else:
                    continue

            if tmp_best < best:
                current_pt = best_tmp_current_pt
                best = tmp_best
            else:
                break

        x.append(turn)
        y.append(best)

        res.append(best)

    return [x, y]


def depict_correlation_between_number_of_restarts_and_the_results(class_name, class_num, n_restarts=8, n_ite=3,
                                                                  num_lines=3):
    for i in range(0, num_lines):
        data = get_correlation_between_number_of_restarts_and_the_results(class_name=class_name, class_num=class_num,
                                                                          n_restarts=n_restarts, n_iterations=n_ite)

        x = data[0]
        y = data[1]

        plt.plot(x, y)

    plt.title('Correlation between number of restarts and the results')
    plt.xlabel('Restart')
    plt.ylabel('Result')
    plt.show()


def depict_correlation_between_number_of_iteration_and_the_results(class_name, class_num, n_iterations=50, num_lines=3):
    figure, axis = plt.subplots(1, num_lines)

    for i in range(0, num_lines):
        data = get_correlation_between_number_of_iterations_and_the_results(class_name=class_name, class_num=class_num,
                                                                            n_iterations=n_iterations)

        x = data[0]
        y = data[1]

        print(x)
        print(y)
        print("----------------")

        axis[i].plot(x, y)

    plt.show()


depict_correlation_between_number_of_iteration_and_the_results('MN', '01', n_iterations=4000)
