import numpy as np

data = np.array(['a', 'b', 'c', 'd', 'a', 'b'])


def calc_elnt(x):
    x = np.array(x)
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        ent -= p * np.log2(p)
    return ent
