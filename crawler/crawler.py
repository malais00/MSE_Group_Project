import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import random
from datetime import datetime
import pre_processing
from langdetect import detect
from maxHeap import UrlMaxHeap
from url_ranker import url_ranker
from db import MongoDB
import pymongo
import link_checker

# Setup logging to output informational messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of user agents to spoof different browsers and avoid being blocked
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
]

# Cache to store robots.txt rules for each root URL
robots_cache = {}
heap = UrlMaxHeap()

# Function to fetch page content asynchronously
async def fetch_url(session, url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        # Perform an HTTP GET request with a 2-second timeout
        async with session.get(url, headers=headers, timeout=2) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            return await response.text()  # Return the content of the response
    except asyncio.TimeoutError:
        logging.warning(f"Timeout for {url}")
        return None
    except Exception as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return None

# Function to get all links from a page
def get_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)  # Construct full URL from relative link
        if urlparse(full_url).scheme in ['https'] and link_checker.is_whitelisted(full_url) and not link_checker.is_anchortag_at_end(full_url):  # Only consider http and https links
            links.add(full_url)
    return links

def get_title(content):
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    return title

# Function to save results to the db file
def save_results(results):
    for url, title, content, timestamp, links in results:
        processedContent = pre_processing.preprocess_content(content)
        mongoDb.savePage(url, title, processedContent, timestamp, list(links))
    logging.info(f"Batch of {len(results)} entries saved in DB")


# Function to check if a URL is allowed by robots.txt
async def is_allowed(session, url):
    parsed_url = urlparse(url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Check if the robots.txt rules are already cached
    if root_url not in robots_cache:
        robots_url = urljoin(root_url, 'robots.txt')
        robots_content = await fetch_url(session, robots_url)
        if robots_content:
            rules = []
            is_global_section = False

            for line in robots_content.splitlines():
                line = line.strip()
                if line.lower().startswith("user-agent:"):
                    user_agent = line.split(":")[1].strip()
                    is_global_section = (user_agent == "*")
                elif is_global_section:
                    if line.lower().startswith('disallow:'):
                        disallow_path = line.split(':', 1)[1].strip()
                        if(disallow_path != ""):
                            rules.append(disallow_path)
            robots_cache[root_url] = rules
        else:
            robots_cache[root_url] = []

    path = parsed_url.path
    # Check if the path is disallowed by any rule in robots.txt
    for rule in robots_cache[root_url]:
        if path.startswith(rule):
            return False
    return True

# Function to check if the page is in English
def is_english(content):
    soup = BeautifulSoup(content, 'html.parser')
    html_tag = soup.find('html')
    if html_tag:
        lang = html_tag.get('lang') or html_tag.get('xml:lang')
        if lang and detect(content) == 'en':
            return lang.startswith('en')
    return True  # Default to True if no lang attribute is found

# Main function to start crawling
async def crawl(seed_urls, max_depth=2, batch_size=10, max_links=100, visited=set()):
    pre_processing.preprocess_preparation()
    if(heap.counter == 0):
        for url in seed_urls:
            heap.add_url(url=url, score=url_ranker(url), depth=0)
    results = []  # List to store the results
    crawled_count = 0  # Counter to keep track of successfully crawled links
    
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        while heap.counter > 0 and crawled_count < max_links:
            _, url, depth = heap.pop_url()  # Get the next URL and its depth from the queue
            if url.endswith('/'):
                url = url[:-1]
            if not link_checker.is_whitelisted(url) or link_checker.is_anchortag_at_end(url):
                continue
            if int(depth) > max_depth or url in visited:
                continue  # Skip if the URL exceeds max depth or has been visited
            if not await is_allowed(session, url):
                logging.info(f"Blocked by robots.txt: {url}")
                continue  # Skip if the URL is disallowed by robots.txt
            
            content = await fetch_url(session, url)  # Fetch the URL content
            if content and is_english(content):  # Check if the content is in English and if it is whitelisted
                visited.add(url)  # Mark URL as visited
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = get_title(content)
                links = get_links(content, url)  # Extract links from the content
                results.append((url, title, content, timestamp, links))  # Add result to the list
                crawled_count += 1  # Increment the crawled count
                logging.info(f"{crawled_count} / {max_links} | Crawling: {url} (Depth: {depth})")
                for link in links:
                    if link not in visited:
                        heap.add_url(url=link, score= url_ranker(link), depth=depth+1) # Add new links to the queue
                        
                # Save batch of results when batch size is reached
                if len(results) >= batch_size:
                    save_results(results)
                    results.clear()
            else:
                # Requeue the URL to try again later, with score penalty so it rankes lower for now
                heap.add_url(url=url, score=url_ranker(url) - 1, depth=depth)

        # Save any remaining results
        if results:
            save_results(results)

# Example usage
if __name__ == "__main__":
    try:
        with open("../seed.txt") as f:
            data = f.read()
        seed_documents = data.split("\n")
        seed_url = "https://en.wikivoyage.org/wiki/T%C3%BCbingen"
        max_depth = 2
        batch_size = 1
        max_links = 1000
        mongoDb = MongoDB("mongodb://localhost:27017/")
        already_crawled = mongoDb.get_already_crawled_urls()
        previous_queue = mongoDb.getPreviousQueue()
        if(previous_queue != []):
            for entry in previous_queue:
                heap.add_url(entry[2], entry[0], entry[3])
        asyncio.run(crawl(seed_documents, max_depth, batch_size, max_links, already_crawled))
    finally:
        mongoDb.delete_collection("queue")
        mongoDb.saveQueue(heap.heap)
