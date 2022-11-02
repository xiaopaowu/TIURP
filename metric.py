# -*- coding: UTF-8 -*-
import numpy as np

import matplotlib.pyplot as plt
from collections import Counter

def pyplot(caselist, row_index):
    x_ = [float(i) / len(caselist) for i in range(len(caselist) + 1)]
    y_ = [0.0] * len(x_)
    row_index.sort()

    for i, value in enumerate(row_index):
        y_[value] = (i + 1) / len(row_index)

    for i, value in enumerate(y_):
        if value == 0:
            y_[i] = y_[i - 1]

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.plot(x_, y_)
    # plt.show()

    linear_interpolation = []
    for i in np.linspace(0.25, 1, 4):
        if i in y_:
            linear_interpolation.append(x_[y_.index(i)] * len(caselist))
        else:
            linear_interpolation.append(np.interp(i, y_, x_) * len(caselist))
    return linear_interpolation


def apfd(Q, caselist, n, M):
    fault_index = {}
    for index in Q:
        case = caselist[index]
        if len(fault_index) == M:
            break
        if case.bug_category not in fault_index and case.bug_category is not 'none':
            fault_index[case.bug_category] = Q.index(index) + 1
    print(len(fault_index), fault_index)

    apfd = 1 + float(0.5 / n)
    for key, value in fault_index.items():
        apfd -= float(value / (n * M))
    print('apfd:', apfd)

    linear_interpolation = pyplot(caselist, list(fault_index.values()))
    print('linear interpolation: ', linear_interpolation, '\n')

    return apfd, linear_interpolation
