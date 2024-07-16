import urllib.parse

# only take normal websites (not xml etc..)
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

def is_anchortag_at_end(url):
    if urllib.parse.urlparse(url).fragment:
        return True
    return False
    