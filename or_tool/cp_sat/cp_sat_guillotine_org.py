import time

from ortools.sat.python import cp_model

def soft_instance_input(instance_class):
    f = open("../../data_instances/Class {}/p{}.txt".format(instance_class[0], instance_class[1]), "r")
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


# Create the mip model with the SCIP backend.
model = cp_model.CpModel()

inp = soft_instance_input(['MN', '03'])

n = inp['n']
L1 = inp['L1']
L2 = inp['L2']
a = inp['a']

for i in range(0, n):
    a[i] = a[i]

# Declare objective variable
objective = model.NewIntVar(0, 2 * (L1 + L2), 'obj')

# Variables Declaration
'''
x[i][k]: Represents presence of the rectangle 'i' in layer 'k'
    + 1 if the rec 'i' is in layer 'k'
    + 0 if the rec 'i' is not in layer 'k'
'''
x = []
for i in range(0, n):
    tmp_l = []
    for k in range(0, n):
        tmp = model.NewIntVar(0, 1, 'x{}{}'.format(str(i + 1), str(k + 1)))
        tmp_l.append(tmp)
    x.append(tmp_l)

'''
w[i][k]: Represents the 'L1' of the rectangle 'i' in layer 'k'
'''
w = []
for i in range(0, n):
    tmp_l = []
    for k in range(0, n):
        tmp = model.NewIntVar(0, L1, 'w{}{}'.format(str(i + 1), str(k + 1)))
        tmp_l.append(tmp)
    w.append(tmp_l)

'''
y[k]: Take value 1 if there's at least 1 rec in layer 'k', 0 if there's no rec in layer 'k'
'''
y = []
for k in range(0, n):
    tmp = model.NewIntVar(0, 1, 'y{}'.format(str(k + 1)))
    y.append(tmp)

# Constraints Declaration (The constraints obey to the original formulation)
'''
Constraint (7)
'''
for i in range(0, n):
    sum_x = x[i][0] + x[i][1]
    layers = list(range(2, n))
    for k in layers:
        sum_x += x[i][k]
    model.Add(sum_x == 1)

'''
Constraints (8) + (9)
'''
for k in range(0, n):
    sum_i = x[0][k] + x[1][k]

    recs = list(range(2, n))
    model.Add(x[0][k] <= y[k])
    model.Add(x[1][k] <= y[k])

    for i in recs:
        sum_i += x[i][k]
        model.Add(x[i][k] <= y[k])
    model.Add(sum_i >= y[k])

'''
Constraints (10) + (11) + (12)
'''
for k in range(0, n):
    sum_i = w[0][k] + w[1][k]

    recs = list(range(2, n))

    model.Add(w[0][k] <= L1 * x[0][k])
    model.Add(w[1][k] <= L1 * x[1][k])

    model.Add(w[0][k] * L2 >= a[0] * x[0][k])
    model.Add(w[1][k] * L2 >= a[1] * x[1][k])

    for i in recs:
        sum_i += w[i][k]
        model.Add(w[i][k] <= L1 * x[i][k])
        model.Add(w[i][k] * L2 >= a[i] * x[i][k])

    model.Add(sum_i == L1 * y[k])

'''
Constraint (13)
'''
for k in range(0, n):
    for i in range(0, n):
        for j in range(0, n):
            if j != i:
                model.Add(a[i] * w[j][k] - a[j] * w[i][k] <= a[i] * L1 * (2 - x[i][k] - x[j][k]))

'''
Constraint (14)
'''
for k in range(0, n):
    for i in range(0, n):
        for j in range(0, n):
            if j != i:
                model.Add(a[j] * w[i][k] - a[i] * w[j][k] <= a[j] * L1 * (2 - x[i][k] - x[j][k]))

'''
added Constraint
'''
# for k in range(0, n - 1):
#     model.Add(y[k] >= y[k + 1])

'''
Objectives Constraint
'''
for k in range(0, n):
    for i in range(0, n):
        tmp_l2 = a[0] * x[0][k]
        for j in range(1, n):
            tmp_l2 += a[j] * x[j][k]
        model.Add(objective * L1 >= 2 * (L1 * w[i][k] + tmp_l2) + 2 * L1 * (L1 + L2) * (x[i][k] - 1))

start_time = time.time()

model.Minimize(objective)

solver = cp_model.CpSolver()
status = solver.Solve(model)

end_time = time.time()

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print('Solution:')
    print('Objective value =', solver.ObjectiveValue())
    print("Total time run: %.2f s" % (end_time - start_time))
    print()
    for k in range(0, n):
        for i in range(0, n):
            print(solver.Value(w[i][k]), end=' ')
        print()
else:
    print('The problem does not have an optimal solution.')
