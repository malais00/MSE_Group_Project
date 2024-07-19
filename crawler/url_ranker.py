import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ranking_keywords.txt'))

with open("../ranking_keywords.txt", "r") as f:
    ranking_keywords = f.read().lower().split(",")

def url_ranker(url):
    url = url.lower()
    score = 1
    for keyword in ranking_keywords:
        if keyword in url:
            score += 1
    score = score / len(url)

    return score