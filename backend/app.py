from flask import Flask, jsonify, request
from bson import ObjectId
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../crawler'))
from db import MongoDB
from pre_processing import preprocess_content
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../index'))
from index import invertedIndex
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../query_processing'))
from query_processing import ranked_search
from query_expansion import expand_query, process_query

app = Flask(__name__)


def search(query, inverted_index, starting_index):
    preprocessed_query = " ".join(preprocess_content(query))
    preprocessed_query = " ".join(preprocess_content(query))
    # this doesnt seem to work well, so im excluding it for now
    #expanded_query = expand_query(preprocessed_query)
    #lemmatized = " ".join(process_query(expanded_query))
    #print(lemmatized)

    resulting_document_urls= ranked_search(query=preprocessed_query, inverted_index=inverted_index, starting_index=starting_index)

    return_object = []

    for url, document_id, rank in resulting_document_urls:
        return_object.append({"url": url, "document_id": str(document_id)})

    return return_object

with app.app_context():
    mongoDb= MongoDB("mongodb://localhost:27017/")
    inverted_index = invertedIndex(mongoDb)

@app.route("/api/query/<string:query>/<string:index>", methods=["GET"])
def get_query(query, index):

    if not index.isdigit():
        return jsonify({"error": "Index must be a valid non negative integer"}), 400
    if not int(index) >= 0:
        return jsonify({"error": "Index must be a valid non negative integer"}), 400

    return_json = search(query=query, inverted_index=inverted_index, starting_index=int(index))

    return jsonify(return_json), 200

@app.route("/api/document/details/<string:documentId>", methods=["GET"])
def get_document_content(documentId):

    try:
        content = mongoDb.getCrawledContentByIndex([ObjectId(documentId)])[0]
    except Exception as e:
        return jsonify({"error": repr(e)}), 400

    response_object = {"content": content[1], "index_date": content[2]}

    return jsonify(response_object), 200

if __name__ == '__main__':
    app.run(debug=True)
