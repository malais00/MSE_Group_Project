from api import APIClient
from crawler import Crawler
from vectorizer import Vectorizer
from db import MongoDB
from settings import API_TOKEN, GET_LINKS_API, SEND_LINKS_API, SEND_VECTOR_API
import time
import pymongo

def main():
    api_client = APIClient(API_TOKEN)
    crawler = Crawler()
    vectorizer = Vectorizer()
    mongoDb = MongoDB("mongodb://localhost:27017/")

    # Example usage:
    mongoDb.savePage("http://example.com")

    while True:
        # Step 1: Get links to crawl
        links = api_client.get_links(GET_LINKS_API)
        
        if not links:
            print("No links found, retrying after some time...")
            time.sleep(60)  # Wait for a minute before retrying
            continue

        for link in links:
            print(f"Crawling link: {link}")

            # Step 2: Crawl link and extract links and content
            page_links, page_content = crawler.crawl(link)
            
            # Step 3: Send extracted links
            api_client.send_links(SEND_LINKS_API, page_links)
            
            # Step 4: Vectorize and send content as a tuple with the URL
            vector = vectorizer.vectorize(page_content)
            api_client.send_vectorized_content(SEND_VECTOR_API, link, vector)

if __name__ == '__main__':
    main()