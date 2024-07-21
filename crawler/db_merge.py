from db import MongoDB
import pymongo

mongoDb = MongoDB("mongodb://localhost:27017/")

def removeURLDuplicates():
    cursor = list(mongoDb.db.crawled.find({}, {"url": 1, "_id": 1}))
    for document in cursor:
        results = list(mongoDb.db.crawled.find({"url": document["url"]}))
        if(len(results) > 1):
            for result in results:
                if result["_id"] != document["_id"]:
                    mongoDb.db.crawled.delete_one({"_id": result["_id"]})
                    print("Deleting duplicates of URL '", document, "'")

def checkForIdDuplicates():
    cursor = list(mongoDb.db.crawled.find({}, {"_id": 1}))
    for document in cursor:
        results = list(mongoDb.db.crawled.find({"_id": document["_id"]}))
        if(len(results) > 1):
            for result in results:
                mongoDb.db.crawled.delete_one({"url": result["url"]})
                mongoDb.savePage(result["url"], result["title"], result["content"], result["indexDate"], result["links"], result["favicon"])
                print("Recreating entrys with duplicate _id'", document, "'")


if __name__ == "__main__":
    removeURLDuplicates()
    # checkForIdDuplicates() // _id duplicates throw errors when trying to import them into mongoDB compass