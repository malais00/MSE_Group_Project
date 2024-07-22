import sys
import math
import numpy as np
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../crawler'))
from db import MongoDB

class invertedIndex():
    def __init__(self, mongoDb):
        self.index = {}
        self.document_mapping = {}
        self.corpus_size = 0

        counter = 0
        for document in mongoDb.get_documents_stream():
            keywords = document["content"]
            self.document_mapping[counter] = document["_id"]

            for key in keywords:
                if(key not in self.index.keys()):
                    self.index[key] = posting_list(counter, count=1)
                else:
                    self.index[key].append(counter, count = 1)
            counter += 1
            self.corpus_size += 1

        for key in self.index.keys():
            self.index[key].generate_skips()

    def get_corpus_size(self):
        return self.corpus_size
    
    def intersect_search_and(self, keywords):
        intersected_list = []

        keywords_in_index = [key for key in keywords if key in self.index.keys()]


        if(len(keywords_in_index) == 0):
            return []

        if(len(keywords_in_index) < 2):
            return [self.document_mapping[index] for index in self.index[keywords_in_index[0]].to_list()]

        indices = [0 for key in keywords_in_index]

        while all([indices[i] < self.index[key].get_length() for i, key in enumerate(keywords_in_index)]):

            mapped_indices = [self.index[keywords_in_index[i]].get_index_at(index) for i, index in enumerate(indices)]

            if (len(set(mapped_indices)) <= 1):
                
                ind = self.index[keywords_in_index[0]].get_index_at(indices[0])

                intersected_list += [self.document_mapping[ind]]

                for i, _ in enumerate(indices):
                    indices[i] += 1
            else:

                lowest_pointer = np.argmin(mapped_indices)

                mapped_indices[lowest_pointer] = np.inf

                second_lowest_pointer = np.argmin(mapped_indices)

                if(self.index[keywords_in_index[lowest_pointer]].get_index_at(self.index[keywords_in_index[lowest_pointer]].get_skip(indices[lowest_pointer])) < mapped_indices[second_lowest_pointer]):
                    indices[lowest_pointer] = self.index[keywords_in_index[lowest_pointer]].get_skip(indices[lowest_pointer])
                else:
                    indices[lowest_pointer] = indices[lowest_pointer] + 1

        return intersected_list

    def intersect_search_or(self, keywords):
        intersected_list = []

        keywords_in_index = [key for key in keywords if key in self.index.keys()]

        if(len(keywords_in_index) == 0):
            return []

        if(len(keywords_in_index) < 2):
            return [self.document_mapping[index] for index in self.index[keywords_in_index[0]].to_list()]

        documents = []

        for key in keywords_in_index:
            documents += self.index[key].to_list()

        documents = list(set(documents))

        return [self.document_mapping[index] for index in documents]

class posting_list():
    def __init__(self, index, count):
        self.plist = [index]
        self.skip_pointers = {}
        self.count = count

    def append(self, index, count):
        if(index != self.plist[-1]):
            self.plist.append(index)
        self.count += count

    def get_length(self):
        return len(self.plist)

    def generate_skips(self):
        skip_distance = math.floor(len(self.plist) // math.floor(math.sqrt(len(self.plist))))
        for i in range(0, len(self.plist), skip_distance):
           self.skip_pointers[i] = i + skip_distance

    def get_skip(self, index):
        if(index in self.skip_pointers.keys()):
            if(self.skip_pointers[index] < len(self.plist)):
                return self.skip_pointers[index]
        return index + 1

    def to_list(self):
        return self.plist

    def get_last(self):
        return self.plist[-1]

    def get_first(self):
        return self.plist[0]

    def get_index_at(self, index):
        if(index < len(self.plist)):
            return self.plist[index]
        else:
            return np.inf
    
    def get_document_frequency(self):
        return self.count

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

mongoDb = MongoDB(mongo_uri)
