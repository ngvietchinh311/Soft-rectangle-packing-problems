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
        res = 0
        n = self.inp['n']
        for k in range(0, n):
            if sum(current_solution[k]) >= 1:
                res += 1
        return res

    def calculate_solution_value(self, current_solution):
        """
        Calculate and return the value of the current solution
        :param current_solution:
        :return: float
        """
        res = 0
        n = self.inp["n"]
        a = self.inp["a"]
        L1 = self.inp["L1"]
        L2 = self.inp["L2"]

        for k in range(0, n):
            # Variable hold the layer's area
            tmp_a = 0

            # Calculate the layer's area by adding the existing recs in that layer
            for i in range(0, n):
                if current_solution[k][i] == 1:
                    tmp_a += a[i]
            # Variable hold lengths of recs that in layer 'k + 1'
            tmp_l = [res]
            k_height = L2 * tmp_a / (L1 * L2)

            for i in range(0, n):
                if current_solution[k][i] == 1:
                    tmp_l.append(2 * (k_height + (a[i] / k_height)))

            res = max(tmp_l)

        return res

    def print_solution(self, current_solution):
        """
        Function to print the current solution
        :param current_solution:
        :return:
        """
        n = self.inp["n"]
        for i in range(0, n):
            for k in range(0, n):
                print(current_solution[i][k], end='    ')
            print()

    def change_layer_neighborhood(self, current_solution):
        """
        Find all 'neighbors' of current solution by changing position of 1 rectangle (from 1 layer to another layer)
        :param current_solution:
        :return: list of solution
        """
        n = self.inp["n"]

        res = []

        for k in range(0, n):
            for i in range(0, n):
                if current_solution[k][i] == 1:
                    for check in range(0, n):
                        if current_solution[check][i] == 1:
                            continue
                        tmp_x = utils.get_copy_version(current_solution)
                        tmp_x[k][i] = 0
                        tmp_x[check][i] = 1
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
                tmp_x = utils.get_copy_version(current_solution)
                tmp_x[layer[i]][i] = 0
                tmp_x[layer[j]][i] = 1

                tmp_x[layer[j]][j] = 0
                tmp_x[layer[i]][j] = 1

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

        for k in range(0, n):
            for i in range(0, n):
                if current_solution[k][i] == 1:
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
                            tmp_x = utils.get_copy_version(current_solution)
                            tmp_x[k][i] = 0
                            tmp_x[blank_layer][i] = 1

                            res.append(tmp_x)

        return res

    def merge_layer_neighbourhood(self, current_solution):
        n = self.inp['n']
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
                tmp_x = utils.get_copy_version(current_solution)
                tmp_x[k] = merge_layer
                tmp_x[tmp_layer] = blank_layer

                res.append(tmp_x)

        return res

    def iterated_local_search(self):
        """
        Use iterated local search technique to calculate the best solution
        :return: integer which depict the best solution
        """
        n = self.inp["n"]

        n_restarts = 20
        n_iterations = 10

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
                # neighbours.extend(self.swap_layer_neighborhood(tmp_current_pt))
                # neighbours.extend(self.split_layer_neighbourhood(tmp_current_pt))
                # neighbours.extend(self.merge_layer_neighbourhood(tmp_current_pt))
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

                neighbours = self.split_layer_neighbourhood(tmp_current_pt)
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
                print("RE ", turn, ": ", best)
                res_best = best
            res.append(best)

        return min(res)


if __name__ == '__main__':
    ls = LocalSearch("U", "21")
    start_time = time.time()
    print(ls.iterated_local_search())
    end_time = time.time()
    print("End in ", end_time - start_time)

    # ls = LocalSearch("U", "18")
    # sol = utils.get_random_solution(size=ls.inp["n"])
    # print(len(ls.merge_layer_neighbourhood(sol)))
