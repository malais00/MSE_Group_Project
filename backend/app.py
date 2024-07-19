from flask import Flask, jsonify, request
from flask_cors import CORS
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
from spellchecker import SpellChecker

app = Flask(__name__)
CORS(app)

def spellcheck(query):
    misspelled = False
    query_tokenized = query.split()
    unknown = spell_checker.unknown(query_tokenized)

    return_array = []

    for word in query_tokenized:
        if(word not in unknown):
            return_array += [word]
        else:
            misspelled = True
            return_array += [spell_checker.correction(word)]

    corrected = " ".join(return_array)
    return corrected, misspelled


def search(query, inverted_index, starting_index, b_okapi, k1_okapi):
    preprocessed_query = " ".join(preprocess_content(query))
    resulting_document_urls = ranked_search(query=preprocessed_query, inverted_index=inverted_index, starting_index=starting_index, b_okapi=b_okapi, k1_okapi=k1_okapi)
    return_object = []
    for url, content, _id, title, rank in resulting_document_urls:
        return_object.append({"url": url, "title": title, "_id": str(_id), "rank": str(rank)})
    return return_object

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


with app.app_context():
    mongoDb = MongoDB("mongodb://localhost:27017/")
    inverted_index = invertedIndex(mongoDb)
    spell_checker = SpellChecker(language="en", distance= 2)
    keys = list(inverted_index.index.keys())
    keys = [str(key) for key in keys]
    spell_checker.word_frequency.load_words(keys)

@app.route("/api/query/spellcheck/<string:query>", methods=["GET"])
def get_spellcheck(query):
    try:
        corrected, misspelled = spellcheck(query)

        return_object = {"corrected_query": corrected, "misspelled": misspelled}

        return jsonify(return_object), 200
    except Exception as e:
        return_object = {"error": repr(e)}

        return jsonify(return_object), 400

@app.route("/api/query/<string:query>/<string:index>/okapi/<string:b_okapi>/<string:k1_okapi>", methods=["GET"])
def get_query(query, index, b_okapi, k1_okapi):
    if not index.isdigit():
        return jsonify({"error": "Index must be a valid non negative integer"}), 400
    if not int(index) >= 0:
        return jsonify({"error": "Index must be a valid non negative integer"}), 400
    if (not is_float(b_okapi)) or (not is_float(k1_okapi)):
        return jsonify({"error": "Okapi parameters must be a valid number"}), 400

    return_json = search(query=query, inverted_index=inverted_index, starting_index=int(index), b_okapi=float(b_okapi), k1_okapi=float(k1_okapi))
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
