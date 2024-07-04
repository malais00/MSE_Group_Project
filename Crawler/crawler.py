import requests
from bs4 import BeautifulSoup

class Crawler:
    @staticmethod
    def crawl(link):
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_content = soup.get_text()
        page_links = [a['href'] for a in soup.find_all('a', href=True)]
        return page_links, page_content
