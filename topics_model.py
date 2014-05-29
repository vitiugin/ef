# -*- coding: utf-8 -*-

import csv

from gensim import models

class Method:
    def __init__(self, method):
        self.method = method

    def choose_method(self):
        if self.method == 'lda':
            model = models.LdaModel.load('tmp/lda_model.mm')
            method = model.show_topics(topics=50, topn=4494, log=False, formatted=False)
            return method
        elif self.method == 'lsi':
            model = models.LsiModel.load('tmp/lsi_model.mm')
            method = model.show_topics(num_topics=30, num_words=4494, log=False, formatted=False)
            return method
        else:
            raise Exception("ERROR\nIncorrect model or method.\nMore info: http://github.com/fedorvityugin/ef")

class TopicsModel:
    def __init__(self, document, method):
        self.document = document
        self.method = method

        f_texts = self.document
        method = Method(self.method).choose_method()

        prob_auth_topic = []
        for value in auth_dict.values():
            cand_prob = [[r[0] for r in t if value == r[1]] for t in method]
            temp = []
            for l in cand_prob:
                l.append(0)
                temp.append(l[0])
            prob_auth_topic.append(temp)

        temp_querylist = []
        for f in f_texts:
            queryword_prob_topic = [[r[0] for r in t if f == r[1]] for t in method]
            temp_querylist.append(queryword_prob_topic)

        querylist = []
        for query in temp_querylist:
            temp = []
            for l in query:
                l.append(0)
                temp.append(l[0])
                querylist.append(temp)

        fin_list = [i * 0 for i in range(len(querylist[0]))]
        for n in querylist:
            fin_list = [x + y for x, y in zip(fin_list, n)]

        expert_prob_list = []
        for n in prob_auth_topic:
            expert_prob = [x * y for x, y in zip(fin_list, n)]
            expert_prob = sum(expert_prob)
            expert_prob_list.append(expert_prob)

        fin_dict = {}
        n = 0
        for s in auth_dict:
            fin_dict[s] = expert_prob_list[n]
            n += 1

        answer_list = sorted([(value,key) for (key,value) in fin_dict.items()])

        print 'TOP-5 experts:'
        print str(answer_list[-1][1]) + ': ' + str(answer_list[-1][0])
        print str(answer_list[-2][1]) + ': ' + str(answer_list[-2][0])
        print str(answer_list[-3][1]) + ': ' + str(answer_list[-3][0])
        print str(answer_list[-4][1]) + ': ' + str(answer_list[-4][0])
        print str(answer_list[-5][1]) + ': ' + str(answer_list[-5][0])

auth_dict = {}
with open('authors_index.csv', 'rb') as csvauth:
    file = csv.reader(csvauth, delimiter='\t')
    n = 1
    for row in file:
        id = 'authid' + str(n)
        if auth_dict.has_key(row[0]) is False:
            auth_dict[row[0]] = id
            n += 1
