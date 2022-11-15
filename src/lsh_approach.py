# -*- coding: UTF-8 -*-

import numpy as np
from e2lsh.gen_fp import gen_image_fp


def jaccard_of_text(reportA, reportB):
    setA = set(reportA.keyword)
    setB = set(reportB.keyword)
    intersection = len(setA.intersection(setB))
    union = len(setA.union(setB))

    if len(setA) == 0 and len(setB) == 0:
        return 1
    else:
        return 1 - float(intersection / union)


def get_mindist(SPM_Matrix, i):
    min, min_arg = 2, -1
    for j in range(len(SPM_Matrix)):
        if SPM_Matrix[i][j] > 0 and SPM_Matrix[i][j] < min:
            min = SPM_Matrix[i][j]
            min_arg = j
    return min, min_arg


def get_img_num(all_buckets, j):
    num = 0
    m, n = all_buckets.shape
    for i in range(m):
        if all_buckets[i][j] != 0:
            num += 1
    return num


def convert_to_array(buckets, caselist, project):
    imagename_path = 'E:/data/feature_vector/ImageNames-' + project + '.txt'
    SPdistance_path = 'E:/data/distance_matrix/SPDistanceMatrix-' + project + '.txt'
    SPM_Matrix = np.loadtxt(SPdistance_path, delimiter=',')

    all_buckets = np.zeros((len(buckets), len(caselist)), dtype=int)
    m, n = all_buckets.shape

    # get image name list
    fopen = open(imagename_path)
    namelistfile = fopen.read()
    namelist = namelistfile.split('\n')[1].split(',')

    for index, value in enumerate(buckets.values()):
        for i in value:
            all_buckets[index][int(namelist[i].split('_')[0])] += 1

    for i, case in enumerate(caselist):
        if get_img_num(all_buckets, i) >= 2:
            min, min_idx = 2, -1
            for j, name in enumerate(namelist):
                if int(name.split('_')[0]) == i:
                    # find the smallest distance
                    min_dist, min_img_idx = get_mindist(SPM_Matrix, j)
                    if min > min_dist:
                        min = min_dist
                        min_idx = min_img_idx
            for index, value in enumerate(buckets.values()):
                if min_idx in value:
                    for v in range(m):
                        all_buckets[v][i] = 0
                    all_buckets[index][i] = 1
                    break

    delete_index = []
    for i in range(m):
        if all_buckets[i].sum() == 0:
            delete_index.append(i)
    delete_index.reverse()
    if len(delete_index) != 0:
        for i in delete_index:
            all_buckets = np.delete(all_buckets, i, 0)
    return all_buckets


def add_to_buckets(all_buckets, caselist):
    buckets = np.sum(all_buckets, axis=0)
    index_list = np.where(buckets == 0)[0]  # index:case_id

    for i in index_list:
        min, min_row, min_column = 1, -1, -1
        for row, value in enumerate(all_buckets):
            column_list = np.where(value != 0)[0]
            for column in column_list:
                if jaccard_of_text(caselist[column], caselist[i]) < min:
                    min = jaccard_of_text(caselist[column], caselist[i])
                    min_row = row

        all_buckets[min_row][i] += 1
    return all_buckets


def get_all_buckets(caselist, project, k=20, L=1, r=1, tableSize=1):
    hashTable = gen_image_fp(k, L, r, tableSize, project=project)  # dic

    all_buckets = hashTable[0].buckets
    all_buckets = convert_to_array(all_buckets, caselist, project)

    # add to buckets
    all_buckets = add_to_buckets(all_buckets, caselist)

    filename = './group_report/all_buckets-' + project + '.txt'
    # np.savetxt(filename, all_buckets, fmt='%d')
