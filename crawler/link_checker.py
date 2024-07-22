import urllib.parse
import re

# Function to check if the URL is in the whitelist
def is_whitelisted(url):
    # create blacklist of url endings
    blacklist = [".xml", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".mp4", ".mp3", ".avi", ".mov", 
                 ".webm", ".flv", ".ogg", ".webp", ".ico", ".css", ".js", ".json", ".xml", ".rss", ".atom", 
                 ".gz", ".zip", ".rar", ".7z", ".tar", ".iso", ".dmg", ".exe", ".apk", ".torrent", ".woff", 
                 ".woff2", ".ttf", ".otf", ".eot", ".flac", ".wav", ".zip", ".rar", ".7z", ".tar", ".iso", 
                 ".dmg", ".exe", ".apk", ".torrent", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".flac", ".wav"]
    for ending in blacklist:
        if url.endswith(ending):
            return False
    return True

# Function to check if the URL has an anchor tag at the end
def is_anchortag_at_end(url):
    if urllib.parse.urlparse(url).fragment:
        return True
    return False

# Function to check if the URL is a query page with a page number higher than max_page
def is_query_page_higher(url, max_page=10):
    query = urllib.parse.urlparse(url).query.split("&")
    for q in query:
        if "page" in q:
            match = re.search('page=(\d+)', q)
            if match != None:
                if match.group(1).isdigit() and int(match.group(1)) > max_page:
                    return True
    return False

    