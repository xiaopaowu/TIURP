# -*- coding: UTF-8 -*-

import csv
import jieba


def extract_keyword(description):
    f_stopwords = open('stopwords1893.txt', encoding='utf-8')
    stopwords = f_stopwords.read()
    stopwords = stopwords.split('\n')

    keywords = jieba.lcut(description, cut_all=False)
    keyword_1 = []
    for word in keywords:  # filter stopwords
        if word not in stopwords and word is not ' ':
            keyword_1.append(word)
    return keyword_1


def load_data():
    CsvPath = '/TIURP_JSEP/bugdata_textcnn.csv'

    csv_title = []
    csv_description = []
    with open(CsvPath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            keywords_0 = extract_keyword(row[2])
            keywords_1 = extract_keyword(row[3])
            if len(keywords_0) > 1 and len(keywords_1) > 1:
                csv_title.append(row[7])
                csv_description.append(row[8])

    print(len(csv_title), len(csv_description))

    for index, title in enumerate(csv_title):
        a = title.split('\n')
        csv_title[index] = ' '.join(a)

    for index, title in enumerate(csv_description):
        a = title.split('\n')
        csv_description[index] = ' '.join(a)

    with open('./data/rt-polarity.pos', 'w', encoding='utf-8') as f:
        for i in csv_title:
            f.write(i + '\n')

    with open('./data/rt-polarity.neg', 'w', encoding='utf-8') as f:
        for i in csv_description:
            f.write(i + '\n')


if __name__ == '__main__':
    load_data()

