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

inp = soft_instance_input(['MN', '21'])

n = inp['n']
L1 = inp['L1']
L2 = inp['L2']
a = inp['a']

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
w[i]: Represents the 'L2' of the layer 'k'
'''
w = []
for k in range(0, n):
    tmp = model.NewIntVar(0, L2, 'w{}'.format(str(k + 1)))
    w.append(tmp)

'''
y[k]: Take value 1 if there's at least 1 rec in layer 'k', 0 if there's no rec in layer 'k'
'''
y = []
for k in range(0, n):
    tmp = model.NewIntVar(0, 1, 'y{}'.format(str(k + 1)))
    y.append(tmp)

# Constraints Declaration

# Constraint (1)
for i in range(0, n):
    sum_x = x[i][0] + x[i][1]
    layers = list(range(2, n))
    for k in layers:
        sum_x += x[i][k]
    model.Add(sum_x == 1)

# Constraint (2) + (3)
for k in range(0, n):
    sum_i = x[0][k] + x[1][k]

    recs = list(range(2, n))
    model.Add(x[0][k] <= y[k])
    model.Add(x[1][k] <= y[k])

    for i in recs:
        sum_i += x[i][k]
        model.Add(x[i][k] <= y[k])
    model.Add(sum_i >= y[k])

# Constraint (4)
tmp_sum = w[0]
for i in range(1, n):
    tmp_sum += w[i]
model.Add(tmp_sum == L2)

# Constraint (5)
for k in range(0, n):
    area_k = a[0] * x[0][k] + a[1] * x[1][k]
    for i in range(2, n):
        area_k += (a[i] * x[i][k])
    model.Add(area_k == w[k] * L1)

# Objective Constraints
'''
Use a loop to calculate the 'L1' of each rectangle
'''
s_l2 = [model.NewIntVar(0, L2 * L2, 's{}'.format(str(k + 1))) for k in range(0, n)]
s_p_l2 = [model.NewIntVar(0, 2 * (L1 + L2) * L2, 's_l2{}'.format(str(k + 1))) for k in range(0, n)]
for k in range(0, n):
    tmp_l = [w[k], w[k]]
    model.AddMultiplicationEquality(s_l2[k], tmp_l)

    tmp_l = [w[k], objective]
    model.AddMultiplicationEquality(s_p_l2[k], tmp_l)
    for i in range(0, n):
        model.Add(2 * a[i] * x[i][k] + 2 * s_l2[k] <= s_p_l2[k])

model.Minimize(objective)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.ObjectiveValue())
    for k in range(0, n):
        for i in range(0, n):
            print(solver.Value(x[i][k]), end='  ')
        print()
else:
    print('The problem does not have an optimal solution.')
    print(status)






