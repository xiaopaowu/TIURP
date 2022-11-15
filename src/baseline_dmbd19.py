# -*- coding: UTF-8 -*-
import random
import numpy as np
from model import *


def clustering(project, thre):  # return cluster index
    filename = './distance_matrix/BDMatrix-' + project + '.txt'
    distance_matrix = np.loadtxt(filename, delimiter=' ', dtype=float)
    m, n = distance_matrix.shape

    R = [i for i in range(m)]
    Q = [-1] * m

    min, min_i, min_j = 2, -1, -1
    for i in range(m):
        for j in range(i + 1, n):
            if distance_matrix[i][j] < min:
                min = distance_matrix[i][j]
                min_i = i
                min_j = j
    Q[min_i], Q[min_j] = 0, 1
    R.remove(min_i)
    R.remove(min_j)
    random.shuffle(R)

    t = 1
    while len(R) != 0:
        i = R[0]
        max_dist, k = -1, -1
        for j, value in enumerate(Q):
            if value != -1 and distance_matrix[i][j] > max_dist:
                max_dist = distance_matrix[i][j]
                k = value
        if max_dist >= thre:  # add to cluster
            Q[i] = k
            R.remove(i)
        else:  # create a new cluster
            Q[i] = t + 1
            t += 1
            R.remove(i)
    return Q


def build_cluster_list(cluster_index):
    clusterlist = []
    cluster_num = len(np.unique(cluster_index))
    print('cluster num:', cluster_num)

    for i in range(0, cluster_num):
        newcase = cluster(i)
        clusterlist.append(newcase)

    for i in range(len(cluster_index)):
        for j in clusterlist:
            if cluster_index[i] == j.cluster_id:
                j.report_state.append(i)

    return clusterlist
