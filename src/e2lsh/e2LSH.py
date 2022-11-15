import random
import numpy as np


class TableNode(object):
    def __init__(self, index):
        self.val = index
        self.buckets = {}


def genPara(n, r):

    a = []
    for i in range(n):
        a.append(random.gauss(0, 1))
    b = random.uniform(0, r)

    return a, b


def gen_e2LSH_family(n, k, r):

    result = []
    for i in range(k):
        result.append(genPara(n, r))

    return result


def gen_HashVals(e2LSH_family, v, r):

    hashVals = []

    for hab in e2LSH_family:
        hashVal = (np.inner(hab[0], v) + hab[1]) // r
        hashVals.append(hashVal)

    # print(hashVals)
    return hashVals


def H2(hashVals, fpRand, k, C):
    return int(sum([(hashVals[i] * fpRand[i]) for i in range(k)]) % C)


def e2LSH(dataSet, k, L, r, tableSize):

    hashTable = [TableNode(i) for i in range(tableSize)]

    n = len(dataSet[0])
    m = len(dataSet)

    C = pow(2, 32) - 5
    hashFuncs = []
    fpRand = [random.randint(-10, 10) for i in range(k)]

    for times in range(L):

        e2LSH_family = gen_e2LSH_family(n, k, r)

        # hashFuncs: [[h1, ...hk], [h1, ..hk], ..., [h1, ...hk]]
        # hashFuncs include L hash functions group_report, and each group_report contain k hash functions
        hashFuncs.append(e2LSH_family)

        for dataIndex in range(m):

            # generate k hash values
            hashVals = gen_HashVals(e2LSH_family, dataSet[dataIndex], r)

            # generate fingerprint
            fp = H2(hashVals, fpRand, k, C)

            # generate index
            index = fp % tableSize

            # find the node of hash table
            node = hashTable[index]

            # node.buckets is a dictionary: {fp: vector_list}
            if fp in node.buckets:
                node.buckets[fp].append(dataIndex)

            else:
                node.buckets[fp] = [dataIndex]

    return hashTable, hashFuncs, fpRand


def nn_search(dataSet, query, k, L, r, tableSize):
    """

    :param dataSet:
    :param query:
    :param k:
    :param L:
    :param r:
    :param tableSize:
    :return: the data index that similar with query
    """

    result = set()

    temp = e2LSH(dataSet, k, L, r, tableSize)
    C = pow(2, 32) - 5

    hashTable = temp[0]
    hashFuncGroups = temp[1]
    fpRand = temp[2]

    for hashFuncGroup in hashFuncGroups:

        # get the fingerprint of query
        queryFp = H2(gen_HashVals(hashFuncGroup, query, r), fpRand, k, C)

        # get the index of query in hash table
        queryIndex = queryFp % tableSize

        # get the bucket in the dictionary
        if queryFp in hashTable[queryIndex].buckets:
            result.update(hashTable[queryIndex].buckets[queryFp])

    return result
