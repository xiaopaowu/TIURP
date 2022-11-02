import numpy as np
import scipy.io as scio


# def chi2_distance(histA, histB, eps=1e-10):
#     d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])
#     return d


def load_data():
    project_name = 'MyListening'
    path = '/TIURP_JSEP/feature_vector/' + project_name + '/pyramids_all_200_3.mat'

    data = scio.loadmat(path)
    feature_vector = np.array(data['pyramid_all'])
    print(np.shape(feature_vector))

    # text_filename = 'E:/data/feature_vector/image_feature_vector-' + project_name + '.txt'
    # np.savetxt(text_filename, feature_vector, fmt='%.6f', delimiter=' ', encoding='utf-8')


if __name__ == '__main__':
    load_data()
