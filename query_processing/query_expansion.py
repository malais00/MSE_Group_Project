import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def process_query(query):
    words = word_tokenize(query)

    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]

    return lemmatized_words

def get_synonyms(word):
    synonyms = set()
    original_synsets = wordnet.synsets(word)

    for syn in original_synsets:
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym != word:  # Avoid adding the word itself as a synonym
                synonyms.add((synonym, syn))

    return synonyms

def filter_synonyms(word, synonyms, threshold):
    filtered_synonyms = set()
    original_synsets = wordnet.synsets(word)

    for synonym, syn_synset in synonyms:
        max_similarity = 0
        for orig_synset in original_synsets:
            similarity = orig_synset.path_similarity(syn_synset)
            if similarity and similarity > max_similarity:
                max_similarity = similarity
        
        if max_similarity >= threshold:
            filtered_synonyms.add(synonym)

    return filtered_synonyms

def expand_query(query, threshold=1):
    words = word_tokenize(query)
    expanded_query = set(words)

    for word in words:
        synonyms = get_synonyms(word)
        filtered_synonyms = filter_synonyms(word, synonyms, threshold)
        expanded_query.update(filtered_synonyms)
    print("Expanded query \'" + query + "\' to: " + ' '.join(expanded_query))
    return ' '.join(expanded_query)
