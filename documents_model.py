# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities
import csv, re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
documents = []
texts = []
dictionary = corpora.Dictionary.load('tmp/deerwester.dict')
corpus = corpora.MmCorpus('tmp/deerwester.mm')

class Method:
    def __init__(self, method, vec_bow):
        self.method = method
        self.vec_bow = vec_bow

    def choose_method(self):
        if self.method == 'lda':
            method = models.LdaModel(corpus, id2word=dictionary, num_topics=100)
            vec_lda = method[self.vec_bow]
            index = similarities.MatrixSimilarity(method[corpus])
            index.save('tmp/deerwester.index')
            index = similarities.MatrixSimilarity.load('tmp/deerwester.index')
            sims = index[vec_lda]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            return sims[:5]
        elif self.method == 'lsi':
            method = models.LsiModel(corpus, id2word=dictionary, num_topics=50)
            vec_lsi = method[self.vec_bow]
            index = similarities.MatrixSimilarity(method[corpus])
            index.save('tmp/deerwester.index')
            index = similarities.MatrixSimilarity.load('tmp/deerwester.index')
            sims = index[vec_lsi]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            return sims[:5]
        else:
            raise Exception("ERROR\nIncorrect model or method.\nMore info: http://github.com/fedorvityugin/ef")

class DocumentsModel:
    def __init__(self, document, method):
        self.document = document
        self.method = method

        f_texts = self.document
        vec_bow = dictionary.doc2bow(f_texts)
        method = Method(self.method, vec_bow).choose_method()
        print method
