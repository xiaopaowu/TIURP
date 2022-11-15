import xlrd
import xlwt
from scipy import stats
from numpy import mean, std, sqrt


def Kruskal_Wallis(lst1, lst2):
    kruskal_pvalue = stats.kruskal(lst1, lst2)
    return round(kruskal_pvalue.pvalue, 4)


def Wilcoxon_test(lst1, lst2):
    wilcoxon_pvalue = stats.wilcoxon(lst1, lst2)
    return round(wilcoxon_pvalue.pvalue, 4)


def cohen_d(lst1, lst2):
    nx = len(lst1)
    ny = len(lst2)
    dof = nx + ny - 2
    numerator = mean(lst1) - mean(lst2)
    denominator = sqrt(((nx - 1) * std(lst1, ddof=1) ** 2 + (ny - 1) * std(lst2, ddof=1) ** 2) / dof)

    d = abs(numerator / denominator)
    r = d / sqrt(d ** 2 + 4)

    return r


if __name__ == '__main__':

    # projects = ['MyListening', '2048', 'HuaWei', 'HuJiang', 'TravelDiary', 'Wonderland']

    '''
        read data file.
    '''

    project = 'MyListening'
    ExcelPath = 'E:/result/MAE/' + project + '.xls'
    workbook = xlrd.open_workbook(ExcelPath)
    sheet1 = workbook.sheet_by_name(project)
    nrows = sheet1.nrows  # 30 rows
    ncolumns = 5  # 5 columns

    RANDOM = []
    BDDiv = []
    DMBD19 = []
    TSE20 = []
    CTRP = []

    for row in range(1, nrows):
        RANDOM.append(sheet1.cell_value(row, 0))
    for row in range(1, nrows):
        BDDiv.append(sheet1.cell_value(row, 1))
    for row in range(1, nrows):
        DMBD19.append(sheet1.cell_value(row, 2))
    for row in range(1, nrows):
        TSE20.append(sheet1.cell_value(row, 3))
    for row in range(1, nrows):
        CTRP.append(sheet1.cell_value(row, 4))

    print('DATA SIZE: ', len(RANDOM))
    print('RANDOM', RANDOM)
    print('BDDiv', BDDiv)
    print('DMBD19', DMBD19)
    print('TSE20', TSE20)
    print('CTRP', CTRP, '\n')

    '''
        start statistic test.
        
        central_method_name = 'CTRP'
        compare_method_name = ['RANDOM', 'BDDiv', 'DMBD19', 'TSE20']
        compare_metric = ['APFD', 'APFDS', 'MAE'] # it contains the key parameter setting.
        
    '''

    # print(Kruskal_Wallis(RANDOM, CTRP))
    # print(Kruskal_Wallis(BDDiv, CTRP))
    # print(Kruskal_Wallis(DMBD19, CTRP))
    # print(Kruskal_Wallis(TSE20, CTRP))

    # print(Wilcoxon_test(RANDOM, CTRP))
    # print(Wilcoxon_test(BDDiv, CTRP))
    # print(Wilcoxon_test(DMBD19, CTRP))
    # print(Wilcoxon_test(TSE20, CTRP))

    print(cohen_d(RANDOM, CTRP))
    print(cohen_d(BDDiv, CTRP))
    print(cohen_d(DMBD19, CTRP))
    print(cohen_d(TSE20, CTRP))
