import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA

project_list = ['MyListening', '2048', 'HuaWei', 'HuJiang', 'TravelDiary', 'Wonderland']
project_size = []  # [396, 206, 294, 252, 166, 116]

X = np.array([[0] * 4200])
for project in project_list:
    filename = 'E:/data/feature_vector/image_feature_vector-' + project + '.txt'
    tmp = np.loadtxt(filename)

    X = np.append(X, tmp, axis=0)
    project_size.append(tmp.shape[0])
    # print(X, '\n')

X = X[1:]
print(X.shape)

pca = PCA(500)  # int: 300（300个特征）, float: 0.95（保留95%的信息）, str: 'mle'（自动选择特征个数）
pca.fit(X)


X_new = pca.transform(X)
print('The image feature after pca processing: ', X_new.shape)
print(X_new)
print(max(X_new.reshape(X_new.shape[0] * X_new.shape[1], 1)), '\n')


for i in range(1, 6):
    project_size[i] += project_size[i - 1]
print('The size of each project: ', project_size, '\n')

m, n = X_new.shape
X_new = preprocessing.minmax_scale(X_new.flatten(), feature_range=(0, 1)).reshape(m, n)
print('The image feature after minmax scaling: ', X_new.shape)

img = [[] for i in range(6)]
img[0] = X_new[:project_size[0]]
img[1] = X_new[project_size[0]:project_size[1]]
img[2] = X_new[project_size[1]:project_size[2]]
img[3] = X_new[project_size[2]:project_size[3]]
img[4] = X_new[project_size[3]:project_size[4]]
img[5] = X_new[project_size[4]:]

print(X_new)

for index, project in enumerate(project_list):
    path = 'image_vector/' + project + '.txt'

    img_vector = np.array(img[index])
    np.savetxt(path, img_vector, fmt="%.6f", delimiter=" ")
