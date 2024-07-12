import re
import nltk
from nltk.corpus import stopwords
from io import StringIO
from html.parser import HTMLParser
from bs4 import BeautifulSoup


def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.strict = False
            self.convert_charrefs= True
            self.text = StringIO()
        def handle_data(self, d):
            self.text.write(d)
        def get_data(self):
            return self.text.getvalue()
    
    def _strip_once(value):
        s = MLStripper()
        s.feed(value)
        return s.get_data()
    
    # _strip_once runs HTMLParser once, pulling out just the text of all the nodes.
    while '<' in value and '>' in value:
        new_value = _strip_once(value)
        if len(new_value) >= len(value):
            # _strip_once was not able to detect more tags
            break
        value = new_value
    return value

def cleanMe(html):
    soup = BeautifulSoup(html, "html.parser") # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word.lower() not in stop_words])

def remove_urls(text):
    return re.sub(r'http\S+', '', text)

def remove_emoji(text):
    emoji_clean = re.compile("["
                             u"\U0001F600-\U0001F64F"  # emoticons
                             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                             u"\U0001F680-\U0001F6FF"  # transport & map symbols
                             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                             u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             "]+", flags=re.UNICODE)
    text = emoji_clean.sub(r'', text)
    url_clean = re.compile(r"https://\S+|www\.\S+")
    text = url_clean.sub(r'', text)
    return text

def stem_text(words):
    stemmer = nltk.stem.PorterStemmer()
    return [stemmer.stem(word) for word in words]

def lemmatize_text(words):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]

def remove_39s(text):
    return re.sub(r'39s', '', text)

def preprocess_content(text):
    pipeline = [cleanMe, remove_punctuation, remove_stopwords, remove_urls, remove_emoji, remove_39s ,nltk.tokenize.word_tokenize, lemmatize_text]
    for step in pipeline:
        text = step(text)
    return text

def preprocess_preparation():
    nltk.download('stopwords')
    nltk.download('wordnet')