# -*- coding: UTF-8 -*-

class case:
    def __init__(self, case_id):
        self.case_id = case_id
        self.bug_id = str()
        self.report_id = str()
        self.bug_category = str()
        self.description = str()
        self.keyword = []
        self.shotlist = []
        self.severity = str()
        self.recurrent = str()

    def print_case(self):
        print('case_id: %s' % self.case_id)
        print('bug_category: %s' % self.bug_category)
        print('description: %s' % self.description)
        print('severity: %s' % self.severity)
        print('keyword: %d' % len(self.keyword))
        print(self.keyword)
        print('shotlist: %d' % len(self.shotlist))
        print(self.shotlist)
        print('')


class cluster:
    def __init__(self, cluster_id):
        self.cluster_id = cluster_id
        self.report_state = []  # report_state[i][0] is report index

    def print_cluster(self):
        print('cluster_id: %s' % self.cluster_id)
        print('report_state:', self.report_state)
