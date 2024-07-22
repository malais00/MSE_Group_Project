# MSE_Group_Project
Modern Search Engines Group Project Summer by Jannik Brandstetter, Julian Borbeck, Nico Martin, Hoang An Nguyen

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Features](#features)
  - [Supported Parameters](#supported-parameters)
- [Endpoints](#Endpoints)
## Introduction
### Tü-be-fair
Introducing Tü-be-fair, our approach to a webapp search engine, following the lecture of Modern Search Engines of SS24. Our main goal was to create a search engine that incorporates user preferences into its decision-making process and aims to be as transparent as possible in its output. Users can select parameters and see how their choices affect the search results.

## Setup

To get started with using our search engine:

Clone the repository:

```sh
git clone https://github.com/your-repo/MSE_Group_Project.git
```

Navigate to the project directory:

```sh
cd MSE_Group_Project
```
Our project is deployed via Docker. After installing Docker the project can be build by running:
```sh
docker compose build
```
After building, you can start the project with:
```sh
docker compose up
```
This may take a while. After deployment of the containers is complete, you can access the frontend on port 3000 of the hosting server.
Please make sure that port 3000, 5000 and 27018 are free. 
## Features

Our search engine is built upon the concepts of transparency, customizability, and performance. Just as there is no single type of user, there isn't a single set of search engine parameters that works best for everyone.

For example, one user might prioritize fair and diverse results when searching for a good restaurant, while another might focus on finding the best matches for a specific research topic, such as nematode biology. To address this, we give users full control over how searches are performed. Users can customize search parameters to their liking, affecting how documents are ranked.

We use Okapi BM25 as our base ranking system, a well-established ranker used in various search systems. This is further augmented by PageRank and reranking based on result diversity and fairness in document exposure.

Additionally, we also provide query spellchecking suggestions to improve search results.
### Supported Parameters

- Okapi BM25 b: Document length normalization
- Okapi BM25 k: Term frequency saturation
- Diversity weight: Weighs the importance of diversity in reranking
- Fairness weight: Weighs the difference between ranking score and expected exposure in reranking
- Pagerank weight: Weighs the importance of the PageRank score

Users have full control over these parameters on a per-query basis. The original, non-reranked score percentiles for each query are displayed, allowing users to see how their changes impact search results. We have also identified standard parameters that produce acceptable results for most queries.

## Endpoints

Endpoint to spellcheck queries, returns a json object of the following form {"corrected_query": corrected query, "misspelled": Boolean, True if the input was detected to be misspelled}
```
/api/query/spellcheck/<string:query>
```
Endpoint to search query the database, returns a list of json objects of the following form {"url": webpage url, "title": webpage title, "_id": database id of url, "rank": rank after reranking, "percentile": percentile rank of the url before reranking, "favicon": favicon url}
```
/api/query/<string:query>/<string:index>/okapi/<string:b_okapi>/<string:k1_okapi>/<string:diversity_okapi>/<string:fairness_okapi>/pagerank/<string:pagerank_weight>
```
Endpoint to get document content, returns a json object of form {"content": tokenized website content, "index_date": date at which website was indexed}
```
/api/document/details/<string:documentId>
```
Endpoint to get the first paragraph of the content that contains the query terms given the query and the url, returns a json object of form {"first_paragraph": first paragraph as string}
```
/api/document/first-paragraph/<string:query>
```
Endpoint to batch query the search engine. query_list is of the form: first search term, second search term, ... Returns a tsv file with the 100 top ranked results per query
```
/api/batch/<string:query_list>
```