import pymongo
import datetime

class MongoDB:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client.searchEngine 

        schema = {
            "bsonType": "object",
            "required": ["url", "indexDate"],
            "properties": {
                "url": {
                    "bsonType": "string",
                },
                "indexDate": {
                    "bsonType": "date",
                },
            }
        }
        try:
            self.db.create_collection("index", validator={"$jsonSchema": schema})
        except pymongo.errors.CollectionInvalid:
            print("Collection already exists, no need to create collection: index.")

        self.createFrontier()

        
    def savePage(self, url):
        now = datetime.datetime.now()
        document = {"url": url, "indexDate": now}
        db = self.client.searchEngine
        collection = db.index
        collection.insert_one(document)

    def createFrontier(self):
        try:
            self.db.create_collection("frontier")
            frontier = [
                "https://www.tuebingen.de/en/",
                "https://uni-tuebingen.de/en/",
                "https://en.wikipedia.org/wiki/T%C3%BCbingen",
                "https://www.tripadvisor.de/Tourism-g198539-Tubingen_Baden_Wurttemberg-Vacations.html",
                "https://wikitravel.org/de/T%C3%BCbingen",
                "https://www.germany.travel/en/cities-culture/tuebingen.html#:~:text=The%20eternal%20student%20town%3A%20T%C3%BCbingen&text=More%20than%20900%20years%20of,way%20up%20to%20the%20castle",
            ]
            db = self.client.searchEngine
            frontierCollection = db.frontier
            for url in frontier:
                frontierCollection.insert_one({"url": url})

        except pymongo.errors.CollectionInvalid:
            print("Collection already exists, no need to create collection: frontier.")

        