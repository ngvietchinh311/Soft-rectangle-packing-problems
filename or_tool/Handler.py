# class Handler:
#     def __init__(self, n, L1, L2, a):
#         self.n = n
#         self.L1 = L1
#         self.L2 = L2
#         self.a = a
#
#     def mip_guillotine_org(self):
def soft_instance_input(instance_class):
    f = open("../data_instances/Class {}/p{}.txt".format(instance_class[0], instance_class[1]), "r")
    res = {}
    basic_info = f.readline().split(' ')
    res['n'] = int(basic_info[1])
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

print(soft_instance_input(['U', '01']))