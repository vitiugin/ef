# -*- coding: utf-8 -*-

import sys
import codecs
import re

import pymorphy2

import topics_model
import documents_model
import candidates_model

morph = pymorphy2.MorphAnalyzer()

class ModelDecision:
    def __init__(self, query, model, method):
        self.query = query
        self.model = model
        self.method = method

        if self.model == 'topics':
            topics_model.TopicsModel(self.query, self.method)
        elif self.model == 'candidates':
            candidates_model.CandidatesModel(self.query, self.method)
        elif self.model == 'documents':
            documents_model.DocumentsModel(self.query, self.method)

class DocumentsSplit:
    def __init__(self, documents):
        self.documents = documents

    def split_file(self):
        with codecs.open(self.documents, 'r', 'utf-8') as file:
            for query in file:
                docs = []
                words = re.sub(r"\»+", '', query)
                words = re.sub(r"\«+", '', words)
                words = re.split(r'[\s+\t\n\.\|\:\/\,\!\"()]+', words)
                for word in words:
                    if len(word) > 3:
                        a = morph.parse(word.lower())
                        for t in a[:1]:
                            docs.append(t.normal_form.encode('utf-8'))

                ModelDecision(docs, sys.argv[2], sys.argv[3])

try:
    split = DocumentsSplit(sys.argv[1])
    split.split_file()
except IndexError:
    print "ERROR\nNo attributes. Need file, model and method.\nMore info: http://github.com/fedorvityugin/ef"
