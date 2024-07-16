from collections import Counter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../crawler'))
from db import MongoDB
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../index'))
from index import invertedIndex
import math

# URL, Content, Date
def getCrawledContent():
    mongoDb = MongoDB("mongodb://localhost:27017/")
    #invIndex = invertedIndex(mongoDb)
    #invIndex.intersect_search_and(["Tübingen", "Travel", "guide"])
    return mongoDb.getCrawledContent()

def term_frequency(query, document):
    score = 0
    query_tokens = query.split()
    for token in query_tokens:
        for word in document:
            if token == word:
                score += 1
    return score

def document_frequency(query, corpus):
    score = 0
    query_tokens = query.split()
    for document in corpus:
        for token in query_tokens:
            if token in document[1]:
                score += 1
                break
    return score

def inverse_document_frequency(query, corpus):
    return math.log(len(corpus) / document_frequency(query, corpus))

# OKAPI BM25
# b strength of document normalization
# k term frequency saturation  
def okapi_bm25(query, document, corpus, b=0.75, k=1.5):
    if len(document) == 0:
        return 0
    query_tokens = query.split()
    score = 0
    for token in query_tokens:
        tf = term_frequency(token, document)
        if tf == 0 or len(document) == 0:
            continue
        idf = inverse_document_frequency(token, corpus)
        score += idf * ((tf * (k + 1)) / (tf + k * (1 - b + b * (len(document) / len(corpus)))))
    return score
    

def main():
    #import crawled content
    corpus = getCrawledContent()
    #print(corpus[0])
    #print(document_frequency("tübingen skip", corpus))
    #print(term_frequency("tübingen", corpus[0][1]))
    #print(term_frequency("skip", corpus[0][1]))
    #print(inverse_document_frequency("tübingen", corpus))
    #print(inverse_document_frequency("script", corpus))
    rsv_vector = []
    for document in corpus:
        #print(document[0]) # print URL
        tuple = (document[0], okapi_bm25("food", document[1], corpus))
        rsv_vector.append(tuple)
    # sort rsv_vector
    rsv_vector.sort(key=lambda x: x[1], reverse=False)
    print(rsv_vector)

        

main()