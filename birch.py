import copy
import random

import numpy as np
import xlwt as xlwt
from sklearn.cluster import Birch

from get_fusion_feature import get_fusion_feature
from metric import apfd
from read_data import load_caselist, statistics_case

'''
    loading data...
    fusion_vector: it stores the feature representation of all reports.
'''

# MyListening,2048,HuaWei,HuJiang,TravelDiary,Wonderland

project = 'Wonderland'
file1 = '/TIURP_JSEP/fusion_vector/' + project + '.txt'

caselist = load_caselist(project)
n, M, shot_num, report_num = statistics_case(caselist)

fusion_vector = get_fusion_feature(project)


'''
    clustering analysis...
    clusterlist_[]: the index is the label, and the list is the case_id.
'''



'''
    start prioritizing process...
    Q: it is the result sequence.
'''

workbook = xlwt.Workbook()  # 新建一个工作簿
sheet = workbook.add_sheet(project)  # 在工作簿中新建一个表格

for i in range(30):
    R = [i for i in range(n)]
    Q = []

    cluster_num = i + 30  # 29： it ranges from 30 to 60.
    # cluster_num = 34
    print('cluster number:', cluster_num)
    y_pred = Birch(n_clusters=cluster_num).fit_predict(fusion_vector)

    clusterlist_ = {}

    for index, label in enumerate(y_pred):
        if label not in clusterlist_:
            clusterlist_[label] = [index]
        else:
            clusterlist_[label].append(index)

    clusterlist = copy.deepcopy(list(clusterlist_.values()))


    random_sample_ratio = 0.05 # 0.01,0.05,0.1
    while len(R) != 0:
        for index, cluster in enumerate(clusterlist):
            cluster_size = len(cluster)
            for count in range(int(random_sample_ratio*cluster_size)+1):
                
                if len(cluster) == 0 or len(R) == 0:
                    del clusterlist[index]
                    break
                case_id = random.choice(cluster)
                Q.append(case_id)
                R.remove(case_id)

                clusterlist[index].remove(case_id)

    print(len(Q), Q)
    apfd_, linear_interpolation = apfd(Q, caselist, n, M)
    
    
    sheet.write(i, 0, apfd_)
    sheet.write(i, 2, linear_interpolation[0])
    sheet.write(i, 3, linear_interpolation[1])
    sheet.write(i, 4, linear_interpolation[2])
    sheet.write(i, 5, linear_interpolation[3])

filename = '/TIURP_JSEP/result2/' + project +'_'+ str(random_sample_ratio) +'.xls'
workbook.save(filename)