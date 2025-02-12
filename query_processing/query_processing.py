from collections import Counter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../crawler'))
from db import MongoDB
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../index'))
from index import invertedIndex
import math
import numpy as np
from urllib.parse import urlparse
from page_rank import page_rank


mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
mongoDb = MongoDB(mongo_uri)

page_rank_dict = page_rank()

# Diversification of search results
def measure_relevance(ranking):
    return sum(doc[4] for doc in ranking)

def measure_diversity(unique_words):
    return len(unique_words)

# function for exponentially decaying exposure by rank
def exposure_dropoff(position, decay_rate = 0.2, e_0 = 1):
    return e_0 * np.exp((-decay_rate) * position)

#exposure to be expected, if the exposure were to follow ranking quality, scaled by 1
def expected_exposure(scores):
    return scores / np.sum(scores)

#assumed true exposure if exponentially decaying exposure by rank is assumed
def true_exposure(scores):
    return np.array([exposure_dropoff(position) for position, _ in enumerate(scores)])

#ratio of true exposure scaled by expected exposure per position
def fairness_metric(true_exposure_score, expected_exposure_score):
    return true_exposure_score / expected_exposure_score

def normalize_relevance(relevance, len_ranking):
    if(len_ranking > 0):
        return  relevance / len_ranking
    else:
        return 0

def normalize_diversity(diversity, max_diversity):
    if(max_diversity > 0):
        return diversity / max_diversity
    else:
        return 0

def normalize_fairness(fairness_ratio):
    # Using a sigmoid function to normalize
    return 1 / (1 + np.exp(-fairness_ratio))

def rerank_search_results(ranking, k, l, m):
    if(len(ranking)) == 0:
        return ranking
    reranked = [ranking[0]]
    unique_words = set(ranking[0][1])

    max_unique_words = []

    for doc in ranking:
        max_unique_words += [word for word in set(doc[1])]

    max_unique_words = set(max_unique_words)

    scores = [doc[4] for doc in ranking]

    expected_exposure_list = expected_exposure(scores)

    while len(reranked) < k and len(reranked) < len(ranking):
        max_score = float('-inf')
        best_doc = None
        for i, doc in enumerate(ranking):
            if doc in reranked:
                continue
            relevance = doc[4]
            # Calculate diversity incrementally
            new_words = set(doc[1])
            diversity = normalize_diversity(measure_diversity(unique_words.union(new_words)), len(max_unique_words))

            position = len(reranked)
            new_true_exposure = exposure_dropoff(position)

            fairness_score = normalize_fairness(fairness_metric(new_true_exposure, expected_exposure_list[i]))

            score = (1 - (l + m)) * relevance + l * diversity + m * fairness_score

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

def min_max_normalize(scores):
    if(len(scores) > 0):
        min_score = min(scores)
        max_score = max(scores)
        if(max_score != min_score):
            normalized_scores = [(score - min_score) / (max_score - min_score) for score in scores]
            return normalized_scores
        else:
            normalized_scores = [0 for score in scores]
            return normalized_scores
    else:
        return scores


def ranked_search(query, inverted_index, starting_index, b_okapi, k1_okapi, diversity, fairness, pagerank_weight=0, step=10):
    corpus = getCrawledContent(query, inverted_index)
    rsv_vector = []

    pagerank_scores = []
    okapi_scores = []

    for document in corpus:
        url = urlparse(document[0]).netloc
        # fix url not known to pagerank bug
        if(url in page_rank_dict.keys()):
            pagerank_scores += [page_rank_dict[url]]
        else:
            pagerank_scores += [0]
        okapi_scores += [okapi_bm25(query, document[1], inverted_index, b=b_okapi, k=k1_okapi)]

    normalized_pagerank_scores = min_max_normalize(pagerank_scores)
    normalized_okapi_scores = min_max_normalize(okapi_scores)

    for index, document in enumerate(corpus):

        combined_score = pagerank_weight * normalized_pagerank_scores[index] + (1 - pagerank_weight) * normalized_okapi_scores[index]

        tuple = (document[0], document[1], document[3], document[4], combined_score, document[5])
        rsv_vector.append(tuple)
    # sort rsv_vector
    rsv_vector.sort(key=lambda x: x[4], reverse=True)

    rsv_percentile = calculate_percentiles(rsv_vector)
    return rerank_search_results(rsv_percentile[starting_index*step:starting_index*step+step], step, diversity, fairness)

def calculate_percentiles(rsv_vector):

    total_vectors = len(rsv_vector)

    percentiles = []
    for idx, (url, content, id, title, score, favicon) in enumerate(rsv_vector):
        # Rank starts from 1
        rank = idx + 1
        percentile = math.floor((1 - (rank - 1) / total_vectors) * 100)
        percentiles.append((url, content, id, title, score, percentile, favicon))

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