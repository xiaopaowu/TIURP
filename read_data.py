# -*- coding: UTF-8 -*-

import jieba
import xlrd

from model import *


def reform_float_to_str(float_num):
    str_num = str(float_num)
    str_num = str_num.replace('.0', '')
    return str_num


def reform_description(description):
    description = description.strip()
    # description = description.replace('\n', '')
    return description


def reform_img_url(img_url):
    img_url = img_url.replace(' ', '')
    img_url = img_url.replace(';', '\n')
    img_url = img_url.split('\n')
    return img_url


def extract_keyword(report):
    f_stopwords = open('stopwords1893.txt', encoding='utf-8')
    stopwords = f_stopwords.read()
    stopwords = stopwords.split('\n')

    report.keyword = jieba.lcut(report.description, cut_all=False)
    keyword_1 = []
    for word in report.keyword:  # filter stopwords
        if word not in stopwords and word is not ' ':
            keyword_1.append(word)
    report.keyword = keyword_1


def load_caselist(project):
    ExcelPath = '/TIURP_JSEP/report/' + project + '.xls'
    workbook = xlrd.open_workbook(ExcelPath)
    sheet1 = workbook.sheet_by_name(project)
    nrows = sheet1.nrows

    caselist = []

    bug_id_col_index = 0
    report_id_col_index = 1
    bug_category_col_index = 3
    description_col_index = 4
    img_url_col_index = 5
    severity_col_index = 6
    recurrent_col_index = 7

    case_id = 0
    for row in range(1, nrows):
        newcase = case(case_id)
        newcase.bug_id = reform_float_to_str(sheet1.cell_value(row, bug_id_col_index))
        newcase.report_id = reform_float_to_str(sheet1.cell_value(row, report_id_col_index))
        newcase.bug_category = sheet1.cell_value(row, bug_category_col_index)
        newcase.description = reform_description(sheet1.cell_value(row, description_col_index))
        newcase.shotlist = sheet1.cell_value(row, img_url_col_index)
        newcase.severity = reform_float_to_str(sheet1.cell_value(row, severity_col_index))
        newcase.recurrent = reform_float_to_str(sheet1.cell_value(row, recurrent_col_index))

        if newcase.shotlist.strip() != '':
            newcase.shotlist = reform_img_url(newcase.shotlist)
        caselist.append(newcase)
        case_id += 1

    for report in caselist:
        extract_keyword(report)

    return caselist


def statistics_case(caselist):
    # |F|,|S|,|Rs|
    bug = []
    screenshot = 0
    report_img = 0

    for case in caselist:
        if case.bug_category == '其他':
            case.bug_category = 'none'
        if case.bug_category != 'none':
            bug.append(case.bug_category)

        if len(case.shotlist) > 0:
            screenshot += len(case.shotlist)
            report_img += 1

    bug_list = list(set(bug))
    print(len(bug_list), bug_list)
    for bug in bug_list:
        bug_severity = {}
        bug_severity[1] = 0
        bug_severity[2] = 0
        bug_severity[3] = 0
        bug_severity[4] = 0
        bug_severity[5] = 0

        for case in caselist:
            if case.bug_category == bug:
                bug_severity[int(case.severity)] += 1

        bug_sev_list = list(bug_severity.values())
        max_index = bug_sev_list.index(max(bug_sev_list)) + 1
        print(bug, ':', max_index)
    print('\n')

    sev_category = {}
    for index in range(1, 6):
        sev_category[index] = []

    for case in caselist:
        if int(case.severity) == 1 and case.bug_category not in sev_category[1]:
            sev_category[1].append(case.bug_category)
        elif int(case.severity) == 2 and case.bug_category not in sev_category[2]:
            sev_category[2].append(case.bug_category)
        elif int(case.severity) == 3 and case.bug_category not in sev_category[3]:
            sev_category[3].append(case.bug_category)
        elif int(case.severity) == 4 and case.bug_category not in sev_category[4]:
            sev_category[4].append(case.bug_category)
        elif int(case.severity) == 5 and case.bug_category not in sev_category[5]:
            sev_category[5].append(case.bug_category)

        if len(case.shotlist) > 0:
            screenshot += len(case.shotlist)
            report_img += 1

    n = len(caselist)
    
    for k, v in sev_category.items():
        print(k, ':', v)
    print('\n')

    return n, len(set(bug_list)), screenshot, report_img


if __name__ == '__main__':
    # MyListening,2048,HuaWei,HuJiang,TravelDiary,Wonderland

    project = 'MyListening'
    caselist = load_caselist(project)

    n, M, shot_num, report_num = statistics_case(caselist)
    print(n, M)
