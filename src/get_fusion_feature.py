import numpy as np


def get_fusion_feature(project):
    file1 = '/TIURP_JSEP/text_vector/' + project + '.txt'
    file2 = '/TIURP_JSEP/image_vector/' + project + '.txt'

    text_vector = np.loadtxt(file1, delimiter=' ')
    image_vector = np.loadtxt(file2, delimiter=' ')

    print(text_vector.shape, image_vector.shape)

    # ==========================================================

    imagename_path = '/TIURP_JSEP/feature_vector/ImageNames-' + project + '.txt'

    # get image name list
    f_namelist = open(imagename_path)
    namelistfile = f_namelist.read()
    namelistfile = namelistfile.replace(' ', '')
    namelistfile = namelistfile.replace('\n', ',')
    namelistfile = namelistfile.split(',')
    namelist = []
    imagecount = int(len(namelistfile) / 2)
    for imagename in range(imagecount, 2 * imagecount):
        namelist.append(namelistfile[imagename])

    print(namelist)

    extended_image_vector = [[0] * 500] * len(text_vector)
    for j, name in enumerate(namelist):
        index = int(name.split('_')[0])
        # it selects the image that first occurs in the filename variable.
        if extended_image_vector[index][0] == 0:
            extended_image_vector[index] = image_vector[j]
    # print(np.array(extended_image_vector).shape)

    # np.hstack将参数元组的元素数组按水平方向进行叠加
    fusion_vector = np.hstack((text_vector, extended_image_vector))
    print('The shape of fusion vector: ', fusion_vector.shape, '\n')
    path = '/TIURP_JSEP/fusion_vector/' + project + '.txt'
    np.savetxt(path, fusion_vector, fmt='%.6f', delimiter=' ')
    return extended_image_vector

if __name__ == '__main__':
    project_list = ['MyListening', '2048', 'HuaWei', 'HuJiang', 'TravelDiary', 'Wonderland']

    for project in project_list:
        get_fusion_feature(project)
