# -*- coding: UTF-8 -*-
import random

import numpy as np


def bddiv(caselist, project):
    filename = 'E:/data/distance_matrix/BDMatrix-' + project + '.txt'
    BD_Matrix = np.loadtxt(filename)

    R = [i for i in range(len(caselist))]
    Q = []

    rk = random.choice(R)  # index: case_id
    Q.append(rk)
    R.remove(rk)

    while len(R) != 0:
        max, rc = -1, -1
        for i in R:
            min = 2
            for j in Q:
                if BD_Matrix[i][j] < min:
                    min = BD_Matrix[i][j]
            if min > max:
                max = min
                rc = i
        Q.append(rc)
        R.remove(rc)
    return Q
