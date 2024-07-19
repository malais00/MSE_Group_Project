import numpy as np
from db import MongoDB
from urllib.parse import urlparse

mongoDb = MongoDB("mongodb://localhost:27017/")

def build_link_matrix(page_dict):
    pages = list(page_dict.keys())
    index = {page: i for i, page in enumerate(pages)}
    N = len(pages)
    matrix = np.zeros((N, N))

    for page, links in page_dict.items():
        if not links:
            continue
        i = index[page]
        for link in links:
            if link in index:
                j = index[link]
                matrix[j][i] = 1.0 / len(links)

    return matrix, pages

def calculate_page_dict():
    page_dict = {}

    for document in mongoDb.get_documents_stream_links():
        if("links" in document.keys()):
            outlink_urls = list(set(document["links"]))
        else:
            outlink_urls = []
        if (urlparse(document["url"]).netloc not in page_dict.keys()):
            page_dict[urlparse(document["url"]).netloc] = list(set([urlparse(link).netloc for link in outlink_urls]))
        else:
            page_dict[urlparse(document["url"]).netloc] = list(set(page_dict[urlparse(document["url"]).netloc] + [urlparse(link).netloc for link in outlink_urls]))

    return page_dict

def page_rank(damping_factor=0.85, max_iterations=100, tol=1.0e-6):
    page_dict = calculate_page_dict()
    M, pages = build_link_matrix(page_dict)
    N = len(pages)
    ranks = np.ones(N) / N
    damping_value = (1 - damping_factor) / N

    for iteration in range(max_iterations):
        new_ranks = damping_value + damping_factor * M.dot(ranks)
        if np.linalg.norm(new_ranks - ranks) < tol:
            break
        ranks = new_ranks

    return {pages[i]: ranks[i] for i in range(N)}