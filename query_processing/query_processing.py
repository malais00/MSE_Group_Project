from collections import Counter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../crawler'))
from db import MongoDB
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../index'))
from index import invertedIndex
import math
import numpy as np


mongoDb = MongoDB("mongodb://localhost:27017/")

# Diversification of search results
def measure_relevance(ranking):
    return sum(doc[4] for doc in ranking)

def measure_diversity(unique_words):
    return len(unique_words)

def diversify_search_results(ranking, k, l):
    if(len(ranking)) == 0:
        return ranking
    reranked = [ranking[0]]
    unique_words = set(ranking[0][1])

    while len(reranked) < k:
        max_score = float('-inf')
        best_doc = None
        for doc in ranking:
            if doc in reranked:
                continue
            relevance = doc[4]
            # Calculate diversity incrementally
            new_words = set(doc[1])
            diversity = measure_diversity(unique_words.union(new_words))
            score = l * relevance + (1 - l) * diversity
            if score > max_score:
                max_score = score
                best_doc = doc
        if best_doc:
            reranked.append(best_doc)
            unique_words.update(best_doc[1])

    return reranked

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

    rsv_percentile = calculate_percentiles(rsv_vector)
    return diversify_search_results(rsv_percentile[starting_index*10:starting_index*10+10], 10, 0.5)

def calculate_percentiles(rsv_vector):

    total_vectors = len(rsv_vector)

    percentiles = []
    for idx, (url, content, id, title, score) in enumerate(rsv_vector):
        # Rank starts from 1
        rank = idx + 1
        percentile = math.floor((1 - (rank - 1) / total_vectors) * 100)
        percentiles.append((url, content, id, title, score, percentile))

    return percentiles



"""def main():
    inverted_index = invertedIndex(mongoDb)
    query = "food and drinks"
    corpus = getCrawledContent(query, inverted_index)
    #print(corpus[0])

    #print(document_frequency(query, inverted_index))
    #print(term_frequency(query, corpus[0][1]))
    #print(term_frequency(query, corpus[0][1]))
    #print(inverse_document_frequency(query, inverted_index))
    rsv_vector = []

    for document in corpus:
        # URL, Content, ObjectID, Title, Score
        tuple = (document[0], document[1], document[3], document[4], okapi_bm25(query, document[1], inverted_index))
        rsv_vector.append(tuple)
    # sort rsv_vector
    rsv_vector.sort(key=lambda x: x[4], reverse=True)

    reranked = diversify_search_results(rsv_vector, 10, 0.1)
    # sort rsv_vector
    for i in range(10):
        print(reranked[i][0], reranked[i][4])
        print(rsv_vector[i][0], rsv_vector[i][4])



main()"""