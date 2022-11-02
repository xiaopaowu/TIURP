from read_data import load_caselist
import csv
import re


def get_short_description(text):
    text = text.strip('。!?\n')
    split_list = re.split(r'[。!?\n]', text)

    bug_context = ''.join(split_list[:-1])
    bug_description = split_list[-1]

    return bug_context, bug_description


if __name__ == '__main__':
    project_list = ['MyListening', '2048', 'HuaWei', 'HuJiang', 'TravelDiary', 'Wonderland']

    for project in project_list:
        caselist = load_caselist(project)

        """
        read textcnn results:
        1: system behavior---> [0,1], positive
        0: reproduction step---> [1,0], negative
        """
        filename = './TextCNN_classification/' + project + '.csv'
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            textcnn_result = [0] * len(caselist)
            for index, row in enumerate(reader):
                if index % 2 == 0 and row[0] == '[描述异常行为]':
                    textcnn_result[index // 2] = 1

        reduced_description = []
        for index, case in enumerate(caselist):
            # 1. Text: Unexpected system behaviors
            if textcnn_result[index] == 1:
                print(textcnn_result[index], case.description)
                reduced_description.append(case.description)
                pass

            # 2. Text: Reproduction steps
            else:
                # print(textcnn_result[index], case.bug_category, case.description.replace('\n', ''))
                bug_context, bug_description = get_short_description(case.description)
                # print(textcnn_result[index], case.bug_category, bug_description, '\n')
                print(textcnn_result[index], bug_description)
                reduced_description.append(bug_description)
                pass

        filename = 'reduced_bug_description/' + project + '.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            for bug_description in reduced_description:
                f.write(bug_description.strip().replace('\n', '') + '\n')
