# -*- coding: UTF-8 -*-
import os

import numpy as np

from read_data import load_caselist


def jaccard_of_text(reportA, reportB):
    setA = set(reportA.keyword)
    setB = set(reportB.keyword)
    intersection = len(setA.intersection(setB))
    union = len(setA.union(setB))

    if len(setA) == 0 and len(setB) == 0:
        return 1
    else:
        return 1 - float(intersection / union)


def read_SPDistanceMatrix(project):
    imagename_path = 'E:/data/feature_vector/ImageNames-' + project + '.txt'
    SPdistance_path = 'E:/data/distance_matrix/SPDistanceMatrix-' + project + '.txt'

    # get image name list
    f_namelist = open(imagename_path)
    namelistfile = f_namelist.read()
    namelistfile = namelistfile.replace(' ', '')
    namelistfile = namelistfile.replace('\n', ',')
    namelistfile = namelistfile.split(',')
    namelist = []
    imagecount = int(len(namelistfile) / 2)
    for imagename in range(imagecount, 2 * imagecount):
        namelist.append(namelistfile[imagename])

    # read SPM distance Matrix
    SPM_Matrix = np.loadtxt(SPdistance_path, delimiter=',')
    return namelist, SPM_Matrix


def build_text_distance_matrix(project):
    caselist = load_caselist(project)
    casecount = len(caselist)
    text_distance_matrix = np.zeros((casecount, casecount), dtype=np.float64)

    for i in range(casecount):
        for j in range(i, casecount):
            DT = jaccard_of_text(caselist[i], caselist[j])
            text_distance_matrix[i][j] = DT

    for i in range(casecount):
        for j in range(i + 1, casecount):
            text_distance_matrix[j, i] = text_distance_matrix[i, j]

    DT_filename = 'E:/data/distance_matrix/DTMatrix-' + project + '.txt'
    np.savetxt(DT_filename, text_distance_matrix, fmt='%.6f')
    print('Build Matrix of Text Distance Succeed!')

    return text_distance_matrix


def get_distance_of_shots(shotA, shotB, imagenamelist, SPM_Matrix):
    if shotA not in imagenamelist or shotB not in imagenamelist:
        return 10000
    shotA_index = imagenamelist.index(shotA)
    shotB_index = imagenamelist.index(shotB)
    distance = SPM_Matrix[shotA_index][shotB_index]

    return distance


def jaccard_of_shots(reportA, reportB, imagenamelist, SPM_Matrix, γ):
    intersection = 0
    shotlistA = reportA.shotlist
    shotlistB = [[0 for i in range(2)] for i in range(len(reportB.shotlist))]

    for index, shot in enumerate(shotlistA):
        file_suffix = os.path.splitext(shot)[1]
        shotlistA[index] = '{}{}{}{}'.format(reportA.case_id, '_', index, file_suffix)

    for i in range(len(reportB.shotlist)):
        shotlistB[i][0] = 0
        shotlistB[i][1] = reportB.shotlist[i]

    for index, shot in enumerate(shotlistB):
        file_suffix = os.path.splitext(shot[1])[1]
        shotlistB[index][1] = '{}{}{}{}'.format(reportB.case_id, '_', index, file_suffix)

    for shotA in shotlistA:
        for i in range(len(shotlistB)):
            if shotlistB[i][0] == 0 and get_distance_of_shots(shotA, shotlistB[i][1], imagenamelist, SPM_Matrix) <= γ:
                intersection += 1
                shotlistB[i][0] = 1
                break

    union = len(shotlistA) + len(shotlistB) - intersection
    if union == 0:
        return 0
    else:
        return 1 - float(intersection / union)


def build_shot_distance_matrix(project, γ):
    caselist = load_caselist(project)
    casecount = len(caselist)
    imagenamelist, SPM_Matrix = read_SPDistanceMatrix(project)
    shot_distance_matrix = np.zeros((casecount, casecount))

    for i in range(casecount):
        for j in range(i + 1, casecount):
            DS = jaccard_of_shots(caselist[i], caselist[j], imagenamelist, SPM_Matrix, γ)
            shot_distance_matrix[i][j] = DS

    for i in range(casecount):
        for j in range(i + 1, casecount):
            shot_distance_matrix[j, i] = shot_distance_matrix[i, j]

    DS_filename = 'E:/data/distance_matrix/DSMatrix-' + project + '.txt'
    np.savetxt(DS_filename, shot_distance_matrix, fmt='%.6f')
    print('Build Matrix of Shot Distance Succeed!')
    return shot_distance_matrix


# near 1:similar
def balanced_distance(β, DT, DS):
    distance = (1 + β * β) * DS * DT / (β * β * DS + DT)
    return distance


def build_balanced_distance_matrix(project, same_shot_distance, balanced_factor):
    caselist = load_caselist(project)
    casecount = len(caselist)
    imagenamelist, SPM_Matrix = read_SPDistanceMatrix(project)
    balanced_distance_matrix = np.zeros((casecount, casecount))

    for i in range(casecount):
        for j in range(i, casecount):
            DT = jaccard_of_text(caselist[i], caselist[j])
            DS = jaccard_of_shots(caselist[i], caselist[j], imagenamelist, SPM_Matrix, same_shot_distance)
            if DT == 0:
                BD = 0
            elif DS == 0:
                BD = 0.75 * DT
            elif DT != 0 and DS != 0:
                BD = balanced_distance(balanced_factor, DT, DS)
            balanced_distance_matrix[i][j] = BD

    for i in range(casecount):
        for j in range(i + 1, casecount):
            balanced_distance_matrix[j, i] = balanced_distance_matrix[i, j]

    BD_filename = 'E:/data/distance_matrix/BDMatrix-' + project + '.txt'
    np.savetxt(BD_filename, balanced_distance_matrix, fmt='%.6f')

    print('Build Matrix of Balanced Distance Succeed!')
    return balanced_distance_matrix
