# -*- coding: UTF-8 -*-
import random
import time

import numpy as np
import xlwt

from lsh_approach import get_all_buckets
from metric import apfd_s5
from other.information_entropy import calc_elnt
from read_data import load_caselist, statistics_case


def prioritization(caselist, project):
    filename = './group_report/all_buckets-' + project + '.txt'
    all_buckets = np.loadtxt(filename, dtype=int)
    m, n = all_buckets.shape

    R = [i for i in range(len(caselist))]
    random.shuffle(R)
    Q = []
    R1 = [i for i in range(m)]
    Q1 = []  # record all-buckets

    info_ent, index = 0, -1
    for i in R:
        if calc_elnt(caselist[i].keyword) > info_ent:
            info_ent = calc_elnt(caselist[i].keyword)
            index = i

    fp = 0
    for i in range(m):
        if all_buckets[i][index] > 0:
            all_buckets[i][index] = 0
            fp = i
            break

    if all_buckets[fp].sum() == 0:
        R1.remove(fp)
    else:
        Q1.append(fp)
        R1.remove(fp)

    Q.append(index)
    R.remove(index)

    while len(R) != 0:
        fp = random.choice(R1)
        index_ = np.where(all_buckets[fp] != 0)[0]

        info_ent, max_index = 0, -1
        for index in index_.tolist():
            if calc_elnt(caselist[index].keyword) > info_ent:
                info_ent = calc_elnt(caselist[index].keyword)
                max_index = index
        if info_ent == 0 or max_index == -1:
            max_index = random.choice(index_)
        max_index = random.choice(index_)

        Q.append(max_index)
        R.remove(max_index)

        all_buckets[fp][max_index] = 0
        if all_buckets[fp].sum() == 0:
            R1.remove(fp)
        else:
            Q1.append(fp)
            R1.remove(fp)

        if len(R1) == 0:
            R1, Q1 = Q1, R1
    return Q


if __name__ == '__main__':
    # MyListening,2048,HuaWei,HuJiang,TravelDiary,Wonderland

    project = 'TravelDiary'
    caselist = load_caselist(project)
    n, M, screenshot, report_img = statistics_case(caselist)

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(project)

    for i in range(30):
        get_all_buckets(caselist, project, k=23, L=1, r=0.7, tableSize=1)
        begin = time.time()
        Q = prioritization(caselist, project)
        end = time.time()
        run_time = end - begin

        apfd, linear_interpolation = apfd_s5(Q, caselist, n, M)

        sheet.write(i, 0, apfd)
        sheet.write(i, 2, linear_interpolation[0])
        sheet.write(i, 3, linear_interpolation[1])
        sheet.write(i, 4, linear_interpolation[2])
        sheet.write(i, 5, linear_interpolation[3])

    filename = 'E:/result/apfds_num/hash/' + project + '.xls'
    workbook.save(filename)
