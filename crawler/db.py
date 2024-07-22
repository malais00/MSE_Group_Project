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
                "title": {
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
                "links": {
                    "bsonType": "array",
                    "items": {
                         "bsonType": "string"
                    }
                },
                "favicon": {    
                    "bsonType": "string",
                },
            }
        }
        try:
            # Create collection with schema
            self.db.create_collection("crawled", validator={"$jsonSchema": schema})
        except pymongo.errors.CollectionInvalid:
            # Collection already exists
            print("Collection already exists, no need to create collection: crawled.")
        try:
            # Create collection with schema
            self.db.create_collection("queue")
        except pymongo.errors.CollectionInvalid:
            # Collection already exists
            print("Collection already exists, no need to create collection: queue.")

        # self.createFrontier()

    # Function to save the results of the crawler in the database
    def savePage(self, url, title, content, date, links, favicon):
        document = {"url": url, "title": title, "content": content, "indexDate": date, "links": links, "favicon": favicon}
        db = self.client.searchEngine
        collection = db.crawled
        collection.insert_one(document)

    # Function to save the Queue in the database
    def saveQueue(self, queue):
        for score, counter, url, depth in queue:
            document = {"score": score, "counter": counter, "url": url, "depth": depth}
            db = self.client.searchEngine
            collection = db.queue
            collection.insert_one(document)

    # Function to get the already crawled URLs
    def get_already_crawled_urls(self):
        urls = set()
        cursor = self.db.crawled.find({}, {"url": 1, "_id": 0})
        for document in cursor:
            urls.add(document["url"])
        return urls
    
    # Function to get previous queue
    def getPreviousQueue(self):
        queue = []
        cursor = self.db.queue.find()
        for document in cursor:
            queue.append([document["score"], document["counter"], document["url"], document["depth"]])
        return queue
    
    # Function to get the crawled content by index
    def getCrawledContentByIndex(self, index):
        content = []
        for objectId in index:
            document = self.db.crawled.find_one({"_id": objectId})
            if(document["content"]):
                content.append([document["url"], document["content"], document["indexDate"], document["_id"], document["title"], document["favicon"]])
        return content
    
    # Function to delete a collection
    def delete_collection(self, collection_name):
        self.db[collection_name].drop()
        print(f"Collection {collection_name} deleted.")

    # Function to get the documents stream
    def get_documents_stream(self):
        cursor = self.db.crawled.find({}, {"url": 1, "content": 1})
        for document in cursor:
            if "content" in document.keys():
                yield document
        return None

    # Function to get the documents stream with links
    def get_documents_stream_links(self):
        cursor = self.db.crawled.find({}, {"url": 1, "links": 1})
        for document in cursor:
            if "links" in document.keys():
                yield document
        return None