import re

import jieba
import numpy as np


def extract_keyword(bug_description):
    # it will remove the stopwords.
    f_stopwords = open('stopwords1893.txt', encoding='utf-8')
    stopwords = f_stopwords.read()
    stopwords = stopwords.split('\n')

    description = jieba.lcut(bug_description.strip(), cut_all=False)
    keyword_1 = []
    for word in description:  # filter stopwords
        # remove the numbers and the letters in this word
        word_ = re.sub(r"[A-Za-z0-9]+", "", word).strip()

        if word_ not in stopwords and word_ is not '':
            keyword_1.append(word_)

    return keyword_1


if __name__ == '__main__':
    project_list = ['MyListening', '2048', 'HuaWei', 'HuJiang', 'TravelDiary', 'Wonderland']

    for project in project_list:
        keywords = []

        filename = '/TIURP_JSEP/reduced_bug_description/' + project + '.txt'
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                keywords.append(extract_keyword(line))

        corpus = []
        for index, words in enumerate(keywords):
            # print(index, words)
            corpus.extend(words)

        corpus = list(set(corpus))  # P1: it has 781 words.
        print('Corpus size: ', len(corpus))
        print(corpus)

        text_feature_vector = np.zeros((len(keywords), len(corpus)), dtype=int)
        for index, keyword in enumerate(keywords):
            if len(keyword) != 0:
                for i in range(len(keyword)):
                    for j in range(len(corpus)):
                        if keyword[i] == corpus[j]:
                            text_feature_vector[index][j] += 1

        print('The shape of text vector: ', text_feature_vector.shape, '\n')

        text_filename = './fasttext_text_vector/' + project + '.txt'
        np.savetxt(text_filename, text_feature_vector, fmt='%d', delimiter=' ', encoding='utf-8')
