# -*- coding: UTF-8 -*-
import copy
import numpy as np
import scipy.cluster.hierarchy as sch

from model import *


def read_Matrix(project, matrix_type):  # matrix type are: DS, DT, BD
    if matrix_type == 'DT':
        DT_path = 'E:/data/clustering/DTMatrix-' + project + '.txt'
        Matrix = np.loadtxt(DT_path)
    elif matrix_type == 'DS':
        DS_path = 'E:/data/clustering/DSMatrix-' + project + '.txt'
        Matrix = np.loadtxt(DS_path)
    elif matrix_type == 'BD':
        BD_path = 'E:/data/clustering/BDMatrix-' + project + '.txt'
        Matrix = np.loadtxt(BD_path)
    return Matrix


def hierarchy_clustering(project, matrix_type, θ):  # return cluster index
    Matrix = read_Matrix(project, matrix_type)
    instance = []
    for row_index in range(len(Matrix)):
        tmp = copy.deepcopy(Matrix[row_index])
        tmp = np.insert(tmp, 0, row_index)
        instance.append(tmp)
    # determine the threshold
    row_max = map(max, Matrix)
    longest_dist = max(row_max)
    clustering_threshold = θ * longest_dist

    # customized distance function
    def distance_fuc(X1, X2):
        distance_values1 = X1[1:]
        distance_values2 = X2[1:]
        X1_index = int(X1[0])
        X2_index = int(X2[0])

        return distance_values1[X2_index]

    Z = sch.linkage(instance, method='average', metric=distance_fuc)
    P = sch.dendrogram(Z)
    # plt.show()

    cluster_index = sch.fcluster(Z, t=clustering_threshold, criterion='distance')

    # print("==============================================================================")
    # print("DISTANCE TYPE:" + str(matrix_type))
    # print("farthest distance = " + str(longest_dist))
    # print("threshold = " + str(θ))
    # print("report num = " + str(len(cluster_index)))
    print("cluster num = " + str(max(cluster_index)))
    # print("cluster index:\n", cluster_index)
    # print("==============================================================================")

    return cluster_index


def build_cluster_list(cluster_index):
    clusterlist = []
    cluster_num = max(cluster_index)

    for i in range(1, cluster_num + 1):
        newcase = cluster(i)
        clusterlist.append(newcase)

    for i in range(len(cluster_index)):
        for j in clusterlist:
            if cluster_index[i] == j.cluster_id:
                report_state = np.array([i, 0])
                j.report_state.append(report_state)

    return clusterlist
