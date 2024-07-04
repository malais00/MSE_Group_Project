from sklearn.feature_extraction.text import TfidfVectorizer

class Vectorizer:
    @staticmethod
    def vectorize(content):
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([content])
        return X.toarray().tolist(), vectorizer.get_feature_names_out().tolist()
