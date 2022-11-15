import numpy as np
from sklearn import preprocessing

from e2lsh import e2LSH


def gen_image_fp(k, L, r, tableSize, project):
    C = pow(2, 32) - 5
    filename = 'E:/data/feature_vector/image_feature_vector-' + project + '.txt'
    dataSet = np.loadtxt(filename)

    m, n = dataSet.shape
    dataSet = preprocessing.minmax_scale(dataSet.flatten()).reshape(m, n)

    hashTable, hashFuncs, fpRand = e2LSH.e2LSH(dataSet, k, L, r, tableSize)

    for index in range(tableSize):
        # find the node of hash table

        node = hashTable[index]
        print('table index:%d, bucket size:%d' % (index, len(node.buckets)))
        print(node.buckets)

    return hashTable


if __name__ == '__main__':
    project = '2048'
    hashTable = gen_image_fp(k=20, L=1, r=1, tableSize=1, project=project)
    all_buckets = hashTable[0].buckets
    num = []
    for key, value in all_buckets.items():
        num.extend(value)
    print(len(set(num)))
