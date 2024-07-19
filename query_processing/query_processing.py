from collections import Counter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../crawler'))
from db import MongoDB
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../index'))
from index import invertedIndex
import math


mongoDb = MongoDB("mongodb://localhost:27017/")

# URL, Content, Date
def getCrawledContent(query, iIndex):
    query_token = query.split()
    objectIds = iIndex.intersect_search_and(query_token)
    return mongoDb.getCrawledContentByIndex(objectIds)

def term_frequency(query, document):
    score = 0
    query_tokens = query.split()
    for token in query_tokens:
        for word in document:
            if token == word:
                score += 1
    return score

def document_frequency(query, iIndex):
    score = 0
    for token in query.split():
        if(token in iIndex.index.keys()):
            score += iIndex.index[token].get_document_frequency()
    return score

def inverse_document_frequency(query, inverted_index):
    return math.log(inverted_index.get_corpus_size() / document_frequency(query, inverted_index))

# OKAPI BM25
# b strength of document normalization
# k term frequency saturation  
def okapi_bm25(query, document, inverted_index, b=0.75, k=1.5):
    if len(document) == 0:
        return 0
    query_tokens = query.split()
    score = 0
    for token in query_tokens:
        tf = term_frequency(token, document)
        if tf == 0 or len(document) == 0:
            continue
        idf = inverse_document_frequency(token, inverted_index)
        score += idf * ((tf * (k + 1)) / (tf + k * (1 - b + b * (len(document) / inverted_index.get_corpus_size()))))
    return score

def ranked_search(query, inverted_index, starting_index, b_okapi, k1_okapi):
    corpus = getCrawledContent(query, inverted_index)
    rsv_vector = []

    for document in corpus:
        tuple = (document[0], document[1], document[3], document[4], okapi_bm25(query, document[1], inverted_index, b=b_okapi, k=k1_okapi))
        rsv_vector.append(tuple)
    # sort rsv_vector
    rsv_vector.sort(key=lambda x: x[4], reverse=True)

    return rsv_vector[starting_index*10:starting_index*10+10]

"""def main():
    inverted_index = invertedIndex(mongoDb)
    query = "bar"
    corpus = getCrawledContent(query, inverted_index)
    #print(corpus[0])

    #print(document_frequency(query, inverted_index))
    #print(term_frequency(query, corpus[0][1]))
    #print(term_frequency(query, corpus[0][1]))
    #print(inverse_document_frequency(query, inverted_index))
    rsv_vector = []
    token_classification = []
    for document in corpus:
        #print(document[0]) # print URL
        tuple = (document[0], okapi_bm25(query, document[1], inverted_index))
        rsv_vector.append(tuple)
        token_classification.append(document[1])
    predicts = find_topic_of_token(token_classification)
    # add prediction to rsv_vector
    for i in range(len(rsv_vector)):
        rsv_vector[i] += (predicts[i],)
    # sort rsv_vector
    rsv_vector.sort(key=lambda x: x[1], reverse=True)
    for i in rsv_vector[:10]:
        print(i)



main()"""