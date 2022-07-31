import matplotlib.pyplot as plt
import seaborn as sns
from local_search import LocalSearch
import utils.utilities as utils


def get_correlation_between_number_of_iterations_and_the_results(class_name: str, class_num: str, n_iterations=50,
                                                                 n_restarts=5):
    """
    Get the information needed to create a graph for ITERATED LOCAL SEARCH to depict the correlation between
    number of iterations and the result
    :param class_name: instance class
    :param class_num: number of instance equivalent to the class
    :param n_iterations: number of iterations you want to execute. Default value: 50
    :param n_restarts: Number of restarts
    :return: list of 2 lists (x_axis + y_axis list)
    """
    ls = LocalSearch(class_name, class_num)

    n = ls.inp["n"]

    res = []

    for start in range(0, n_restarts):
        start_pt = utils.get_random_solution(n)
        current_pt = start_pt
        best = ls.calculate_solution_value(start_pt)

        res.append(best)

        for i in range(0, n_iterations):
            tmp_best = best
            tmp_current_pt = current_pt
            best_tmp_current_pt = current_pt

            neighbours = ls.change_layer_neighborhood(tmp_current_pt)
            neighbours.extend(ls.swap_layer_neighborhood(tmp_current_pt))
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

            res.append(best)

    return res


def depict_correlation_between_number_of_iteration_and_the_results(class_name, class_num, n_iterations=50, num_lines=3,
                                                                   n_restarts=5):
    """
    Depict the information get from running the ITERATED LOCAL SEARCH method as a line graph
    :param class_name: instance class's name
    :param class_num: number of data instance equivalent to the class
    :param n_iterations: Number of iterations (DEFAULT VALUE: 1)
    :param num_lines: number of line graphs want to depict (DEFAULT VALUE: 3)
    :param n_restarts: number of restarts
    """

    # if num_lines == 1:
    #     pass
    # else:
    #     figure, axis = plt.subplots(1, num_lines)
    #     plt.subplots_adjust(left=0.1)
    #
    #     for i in range(0, num_lines):
    #         data = get_correlation_between_number_of_iterations_and_the_results(class_name=class_name,
    #                                                                             class_num=class_num,
    #                                                                             n_iterations=n_iterations,
    #                                                                             n_restarts=n_restarts)
    #
    #         x = data[0]
    #         y = data[1]
    #
    #         axis[i].plot(x, y)
    #
    #     plt.show()

    sns.set_theme(style="darkgrid")

    res = get_correlation_between_number_of_iterations_and_the_results(class_name=class_name,
                                                                       class_num=class_num,
                                                                       n_iterations=n_iterations,
                                                                       n_restarts=n_restarts)

    sns.lineplot(list(range(1, len(res) + 1)), res)
    plt.show()


def get_data_iter_res_tabu_search(class_name, class_num):
    def compare_solution(sol_1, sol_2):
        """
        Compare 2 solution and point out the difference between them (the positions of the first solution
        which have different value compared to the second one).
        This can be described as transition abstraction
        :return: list of integers (list of transition abstraction)
        """
        n_1 = len(sol_1)
        n_2 = len(sol_2)
        ret = []
        if n_1 != n_2:
            return ret

        for index in range(0, n_1):
            if sol_1[index] != sol_2[index]:
                ret.append(index)
        return ret

    ls = LocalSearch(class_name, class_num)

    n = ls.inp["n"]

    n_iterations = 300

    # Create a tabu list with fixed size
    tabu_size = int(n / 2)
    tabu_list = []
    res = []

    start_pt = utils.get_random_solution(n)
    current_pt = start_pt
    best = ls.calculate_solution_value(start_pt)
    stable = 0  # stable index
    stable_limit = 5  # limit of stable index
    for i in range(0, n_iterations):
        tmp_best = best
        tmp_current_pt = current_pt
        best_tmp_current_pt = current_pt

        """
        CHANGE LAYER NEIGHBOURS
        """
        neighbours_1 = ls.change_layer_neighborhood(tmp_current_pt)
        for neighbour in neighbours_1:
            value_check = ls.calculate_solution_value(neighbour)
            if value_check < best:
                transitions_abs = compare_solution(current_pt, neighbour)
                check_list = []
                check_list.extend(tabu_list)
                check_list.extend(transitions_abs)
                check_list = set(check_list)
                if len(check_list) < (len(transitions_abs) + len(tabu_list)):
                    continue

                tmp_best = value_check
                best_tmp_current_pt = neighbour
            else:
                continue

        if tmp_best < best:
            """
            UPDATE RESULT + TABU LIST
            """
            transitions_abs = compare_solution(current_pt, best_tmp_current_pt)
            tabu_list.extend(transitions_abs)
            for index in range(0, len(tabu_list) - tabu_size):
                tabu_list.pop(0)

            current_pt = best_tmp_current_pt
            best = tmp_best
            res.append(best)
        else:
            """
            SWAP LAYER NEIGHBOURS
            """
            neighbours_2 = ls.swap_layer_neighborhood(tmp_current_pt)
            for neighbour in neighbours_2:
                value_check = ls.calculate_solution_value(neighbour)
                if value_check < tmp_best:
                    transitions_abs = compare_solution(current_pt, neighbour)
                    check_list = []
                    check_list.extend(tabu_list)
                    check_list.extend(transitions_abs)
                    check_list = set(check_list)
                    if len(check_list) < (len(transitions_abs) + len(tabu_list)):
                        continue

                    tmp_best = value_check
                    best_tmp_current_pt = neighbour
                else:
                    continue

            if tmp_best < best:
                """
                UPDATE RESULT + TABU LIST
                """
                transitions_abs = compare_solution(current_pt, best_tmp_current_pt)
                tabu_list.extend(transitions_abs)
                for index in range(0, len(tabu_list) - tabu_size):
                    tabu_list.pop(0)

                current_pt = best_tmp_current_pt
                best = tmp_best
                res.append(best)
            else:
                """
                MERGE LAYER NEIGHBOURS
                """
                neighbours_3 = ls.merge_layer_neighbourhood(tmp_current_pt)
                for neighbour in neighbours_3:
                    value_check = ls.calculate_solution_value(neighbour)
                    if value_check < tmp_best:
                        transitions_abs = compare_solution(current_pt, neighbour)
                        if len(transitions_abs) > tabu_size:
                            trans_list = list(range(0, n))
                            for tmp_index in transitions_abs:
                                trans_list.remove(tmp_index)
                            transitions_abs = trans_list
                        check_list = []
                        check_list.extend(tabu_list)
                        check_list.extend(transitions_abs)
                        check_list = set(check_list)
                        if len(check_list) < (len(transitions_abs) + len(tabu_list)):
                            continue

                        tmp_best = value_check
                        best_tmp_current_pt = neighbour
                    else:
                        continue

                if tmp_best < best:
                    """
                    UPDATE RESULT + TABU LIST
                    """
                    transitions_abs = compare_solution(current_pt, best_tmp_current_pt)
                    if len(transitions_abs) > tabu_size:
                        trans_list = list(range(0, n))
                        for tmp_index in transitions_abs:
                            trans_list.remove(tmp_index)
                        transitions_abs = trans_list
                    tabu_list.extend(transitions_abs)
                    for index in range(0, len(tabu_list) - tabu_size):
                        tabu_list.pop(0)

                    current_pt = best_tmp_current_pt
                    best = tmp_best
                    res.append(best)
                else:
                    stable += 1

                    if stable < stable_limit:
                        tmp_neighbour = neighbours_1
                        tmp_neighbour.extend(neighbours_2)
                        tmp_neighbour.extend(neighbours_3)
                        aspiration_list = []
                        aspiration_list_value = []
                        for neighbour in tmp_neighbour:
                            value_check = ls.calculate_solution_value(neighbour)
                            if value_check > tmp_best:
                                aspiration_list_value.append(value_check)
                                aspiration_list.append(neighbour)

                        aspiration_criterion = aspiration_list[
                            aspiration_list_value.index(min(aspiration_list_value))]

                        current_pt = aspiration_criterion
                        best = min(aspiration_list_value)

                        """
                        SHOULD I UPDATE THE TABU_LIST ???
                        """

                        res.append(best)
                    else:
                        stable = 0
                        tabu_list = []

    return res


def get_data_iter_res_tabu_search_v2(class_name, class_num):
    def compare_solution(sol_1, sol_2):
        """
        Compare 2 solution and point out the difference between them (the positions of the first solution
        which have different value compared to the second one).
        This can be described as transition abstraction
        :return: list of integers (list of transition abstraction)
        """
        n_1 = len(sol_1)
        n_2 = len(sol_2)
        ret = []
        if n_1 != n_2:
            return ret

        for index in range(0, n_1):
            if sol_1[index] != sol_2[index]:
                ret.append(index)
        return ret

    self = LocalSearch(class_name, class_num)

    n = self.inp["n"]

    n_iterations = 100

    # Create a tabu list with fixed size
    tabu_size = int(n / 2)
    tabu_list = []
    res = []

    start_pt = utils.get_random_solution(n)
    current_pt = start_pt
    best = self.calculate_solution_value(start_pt)
    stable = 0  # stable index
    stable_limit = 5  # limit of stable index
    for i in range(0, n_iterations):
        print(i, ": ")
        tmp_current_pt = current_pt
        tmp_best = self.calculate_solution_value(tmp_current_pt)
        best_tmp_current_pt = current_pt

        """
        NEIGHBOURS INI
        """
        neighbours_3 = self.change_layer_neighborhood(tmp_current_pt)
        neighbours_3.extend(self.swap_layer_neighborhood(tmp_current_pt))
        neighbours_3.extend(self.merge_layer_neighbourhood(tmp_current_pt))
        for neighbour in neighbours_3:
            value_check = self.calculate_solution_value(neighbour)
            if value_check < tmp_best:
                transitions_abs = compare_solution(current_pt, neighbour)
                if len(transitions_abs) > tabu_size:
                    # transitions_abs = list(range(0, n))
                    trans_list = list(range(0, n))
                    for tmp_index in transitions_abs:
                        trans_list.remove(tmp_index)
                    transitions_abs = trans_list
                check_list = []
                check_list.extend(tabu_list)
                check_list.extend(transitions_abs)
                check_list = set(check_list)
                if len(check_list) < (len(transitions_abs) + len(tabu_list)):
                    continue

                tmp_best = value_check
                best_tmp_current_pt = neighbour
            else:
                continue

        if tmp_best < best:
            """
            UPDATE RESULT + TABU LIST
            """
            transitions_abs = compare_solution(current_pt, best_tmp_current_pt)
            if len(transitions_abs) > tabu_size:
                # transitions_abs = list(range(0, n))
                trans_list = list(range(0, n))
                for tmp_index in transitions_abs:
                    trans_list.remove(tmp_index)
                transitions_abs = trans_list
            tabu_list.extend(transitions_abs)
            for index in range(0, len(tabu_list) - tabu_size):
                tabu_list.pop(0)

            current_pt = best_tmp_current_pt
            best = tmp_best
            res.append(best)
        else:
            stable += 1

            if stable < stable_limit:
                tmp_neighbour = neighbours_3
                aspiration_list = []
                aspiration_list_value = []

                for neighbour in tmp_neighbour:
                    value_check = self.calculate_solution_value(neighbour)
                    if 20 >= value_check - tmp_best > 1:
                        aspiration_list_value.append(value_check)
                        aspiration_list.append(neighbour)

                try:
                    aspiration_criterion = aspiration_list[
                        aspiration_list_value.index(min(aspiration_list_value))]

                    current_pt = aspiration_criterion
                    best = min(aspiration_list_value)

                    res.append(best)
                except:
                    pass
            else:
                stable = 0
                tabu_list = []

                res.append(best)

    return res


def depict_tabu_search(class_name, class_num):
    sns.set_theme(style="darkgrid")

    res = get_data_iter_res_tabu_search_v2(class_name, class_num)

    sns.lineplot(list(range(1, len(res) + 1)), res)
    plt.show()


depict_correlation_between_number_of_iteration_and_the_results('U', '14', n_iterations=50, num_lines=1, n_restarts=4)

# depict_tabu_search("MN", "15")
