import pymongo

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
                "content": {
                    "bsonType": "array",
                    "items": {
                         "bsonType": "string"
                    }
                },
                "date": {
                    "bsonType": "date",
                },
            }
        }
        try:
            self.db.create_collection("crawled", validator={"$jsonSchema": schema})
        except pymongo.errors.CollectionInvalid:
            print("Collection already exists, no need to create collection: crawled.")
        try:
            self.db.create_collection("queue")
        except pymongo.errors.CollectionInvalid:
            print("Collection already exists, no need to create collection: queue.")

        # self.createFrontier()

        
    def savePage(self, url, content, date):
        document = {"url": url, "content": content, "indexDate": date}
        db = self.client.searchEngine
        collection = db.crawled
        collection.insert_one(document)

    def saveQueue(self, queue):
        for score, counter, url, depth in queue:
            document = {"score": score, "counter": counter, "url": url, "depth": depth}
            db = self.client.searchEngine
            collection = db.queue
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

    def get_already_crawled_urls(self):
        urls = set()
        cursor = self.db.crawled.find({}, {"url": 1, "_id": 0})
        for document in cursor:
            urls.add(document["url"])
        return urls
    
    def getPreviousQueue(self):
        queue = []
        cursor = self.db.queue.find()
        for document in cursor:
            queue.append([document["score"], document["counter"], document["url"], document["depth"]])
        return queue
    
    def getCrawledContentByIndex(self, index):
        content = []
        for objectId in index:
            document = self.db.crawled.find_one({"_id": objectId})
            content.append([document["url"], document["content"], document["indexDate"]])
        return content
    
    def delete_collection(self, collection_name):
        self.db[collection_name].drop()
        print(f"Collection {collection_name} deleted.")

    def get_documents_stream(self):
        cursor = self.db.crawled.find({}, {"url": 1, "content": 1})
        for document in cursor:
            yield document
        return None