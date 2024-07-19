import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ranking_keywords.txt'))

with open("../ranking_keywords.txt", "r") as f:
    ranking_keywords = f.read().lower().split(",")

def url_ranker(url, depth, keyword_score = 0.1):
    url = url.lower()
    score = 1
    for keyword in ranking_keywords:
        if keyword in url:
            score += keyword_score
    if(len(url) > 0):
        score = score / (len(url) * depth)
    else:
        score = -np.inf

    return score