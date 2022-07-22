import time
import itertools
import utils.utilities as utils


class LocalSearch:
    """
    Class for building local search's algorithm methods
    """
    def __init__(self, class_name, instance_num):
        self.class_name = class_name
        self.instance_num = instance_num
        self.inp = utils.soft_instance_input(class_name, instance_num)

    def get_number_of_layers(self, current_solution):
        """
        Return number of layers in current solution
        :param current_solution:
        :return: int (number of layers)
        """
        tmp_set = set()
        for i in current_solution:
            tmp_set.add(current_solution[i])

        print(tmp_set)

        return len(tmp_set)

    def calculate_solution_value(self, current_solution):
        """
        Calculate and return the value of the current solution
        :param current_solution:
        :return: float
        """
        n = self.inp["n"]
        a = self.inp["a"]
        L1 = self.inp["L1"]
        L2 = self.inp["L2"]

        # Variable hold the layer's area
        tmp_a = []
        for i in range(0, n):
            tmp_a.append(0)

        for i in range(0, n):
            tmp_a[current_solution[i]] += a[i]

        tmp_res = []
        for i in range(0, n):
            k_height = L2 * tmp_a[current_solution[i]] / (L1 * L2)
            tmp_res.append(2 * (k_height + (a[i] / k_height)))

        res = max(tmp_res)

        return res

    def print_solution(self, current_solution):
        """
        Function to print the current solution
        :param current_solution:
        :return:
        """
        n = self.inp["n"]
        for i in range(0, n):
            print(current_solution[i], end='    ')

    def change_layer_neighborhood(self, current_solution):
        """
        Find all 'neighbors' of current solution by changing position of 1 rectangle (from 1 layer to another layer)
        :param current_solution:
        :return: list of solution
        """
        n = self.inp["n"]

        res = []

        for i in range(0, n):
            tmp_layer_list = list(range(0, n))
            tmp_layer_list.remove(current_solution[i])
            for replace_layer in tmp_layer_list:
                tmp_x = utils.get_copy_version(current_solution)
                tmp_x[i] = replace_layer
                res.append(tmp_x)

        return res

    def swap_layer_neighborhood(self, current_solution):
        """
        Find all neighbors of current solution by swapping 2 rectangles in 2 different layers
        :param current_solution:
        :return: list of solution
        """
        n = self.inp['n']

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

    def split_layer_neighbourhood(self, current_solution):
        """
        Find all neighbors of current solution by splitting layer into 2 smaller layers
        :param current_solution:
        :return: list of solutions
        """
        n = self.inp['n']

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

    def merge_layer_neighbourhood(self, current_solution):
        """
        Find all neighbors of current solution by merging 2 layers
        :param current_solution:
        :return: list of solutions
        """
        n = self.inp['n']
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
                tmp_x = utils.get_copy_version(current_solution)
                for i in layer_dict[tmp_layer]:
                    tmp_x[i] = k
                res.append(tmp_x)

        return res

    def iterated_local_search(self):
        """
        Use iterated local search technique to calculate the best solution
        :return: integer which depict the best solution
        """
        n = self.inp["n"]

        n_restarts = 5
        n_iterations = 5000

        res = []
        res_best = 2 * (self.inp["L1"] + self.inp["L2"])
        for turn in range(0, n_restarts):
            start_pt = utils.get_random_solution(n)
            current_pt = start_pt
            best = self.calculate_solution_value(start_pt)
            for i in range(0, n_iterations):
                tmp_best = best
                tmp_current_pt = current_pt
                best_tmp_current_pt = current_pt

                neighbours = self.change_layer_neighborhood(tmp_current_pt)
                for neighbour in neighbours:
                    value_check = self.calculate_solution_value(neighbour)
                    if value_check < tmp_best:
                        tmp_best = value_check
                        best_tmp_current_pt = neighbour
                    else:
                        continue

                neighbours = self.swap_layer_neighborhood(tmp_current_pt)
                for neighbour in neighbours:
                    value_check = self.calculate_solution_value(neighbour)
                    if value_check < tmp_best:
                        tmp_best = value_check
                        best_tmp_current_pt = neighbour
                    else:
                        continue

                neighbours = self.merge_layer_neighbourhood(tmp_current_pt)
                for neighbour in neighbours:
                    value_check = self.calculate_solution_value(neighbour)
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

            if best < res_best:
                res_best = best
            res.append(best)

        return min(res)

    def iterated_local_search_VNS(self):
        """
        Use VNS(Variable Neighborhood Search) technique to calculate the best solution
        :return: integer which depict the best solution
        """
        n = self.inp["n"]

        n_restarts = 1
        n_iterations = 100

        res = []
        res_best = 2 * (self.inp["L1"] + self.inp["L2"])
        for turn in range(0, n_restarts):
            start_pt = utils.get_random_solution(n)
            current_pt = start_pt
            best = self.calculate_solution_value(start_pt)
            for i in range(0, n_iterations):
                tmp_best = best
                tmp_current_pt = current_pt
                best_tmp_current_pt = current_pt

                neighbours = self.change_layer_neighborhood(tmp_current_pt)
                neighbours.extend(self.swap_layer_neighborhood(tmp_current_pt))
                neighbours.extend(self.merge_layer_neighbourhood(tmp_current_pt))
                for neighbour in neighbours:
                    value_check = self.calculate_solution_value(neighbour)
                    if value_check < tmp_best:
                        tmp_best = value_check
                        best_tmp_current_pt = neighbour
                    else:
                        continue

                if tmp_best < best:
                    current_pt = best_tmp_current_pt
                    best = tmp_best
                else:
                    neighbours = self.split_layer_neighbourhood(tmp_current_pt)
                    for neighbour in neighbours:
                        value_check = self.calculate_solution_value(neighbour)
                        if value_check < tmp_best:
                            tmp_best = value_check
                            best_tmp_current_pt = neighbour
                        else:
                            continue

                    if tmp_best < best:
                        current_pt = best_tmp_current_pt
                        best = tmp_best

            if best < res_best:
                res_best = best
            res.append(best)

        return min(res)

    def tabu_search(self):
        """
        Use Tabu search technique to calculate the best solution.
        This version will update the tabu list when meet the first neighbour of current neighbour type which
        is better than the current best solution.
        :return: integer which depict the best solution
        """

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

        n = self.inp["n"]

        n_iterations = 300

        # Create a tabu list with fixed size
        tabu_size = int(n/2)
        tabu_list = []
        res = []

        start_pt = utils.get_random_solution(n)
        current_pt = start_pt
        best = self.calculate_solution_value(start_pt)
        stable = 0  # stable index
        stable_limit = 5    # limit of stable index
        for i in range(0, n_iterations):
            tmp_best = best
            tmp_current_pt = current_pt
            best_tmp_current_pt = current_pt

            """
            CHANGE LAYER NEIGHBOURS
            """
            neighbours_1 = self.change_layer_neighborhood(tmp_current_pt)
            for neighbour in neighbours_1:
                value_check = self.calculate_solution_value(neighbour)
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
                neighbours_2 = self.swap_layer_neighborhood(tmp_current_pt)
                for neighbour in neighbours_2:
                    value_check = self.calculate_solution_value(neighbour)
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
                    neighbours_3 = self.merge_layer_neighbourhood(tmp_current_pt)
                    # neighbours.extend(self.swap_layer_neighborhood(tmp_current_pt))
                    # neighbours.extend(self.merge_layer_neighbourhood(tmp_current_pt))
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
                            tmp_neighbour = neighbours_1
                            tmp_neighbour.extend(neighbours_2)
                            tmp_neighbour.extend(neighbours_3)
                            aspiration_list = []
                            aspiration_list_value = []
                            for neighbour in tmp_neighbour:
                                value_check = self.calculate_solution_value(neighbour)
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

        return min(res)

    def tabu_search_v2(self):
        """
            Use Tabu search technique to calculate the best solution.
            This version will update the tabu list when meet the first neighbour of current neighbour type which
            is better than the current best solution.
            :return: integer which depict the best solution
            """

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
            tmp_best = best
            tmp_current_pt = current_pt
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
                        if 20 >= value_check - tmp_best > 0:
                            aspiration_list_value.append(value_check)
                            aspiration_list.append(neighbour)

                    try:
                        aspiration_criterion = aspiration_list[
                            aspiration_list_value.index(min(aspiration_list_value))]

                        current_pt = aspiration_criterion
                        best = min(aspiration_list_value)
                    except:
                        pass

                    res.append(best)
                else:
                    stable = 0
                    tabu_list = []

        return min(res)


if __name__ == '__main__':
    ls = LocalSearch("U", "20")
    for i in range(0, 100):
        start_time = time.time()
        print("RES" + "%s: %.2f" % (str(i), ls.iterated_local_search()))
        end_time = time.time()
        print("End in %.2f" % (end_time - start_time))
        print("------------------------------------------")
