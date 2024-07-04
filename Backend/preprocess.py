import json
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_data(dataset):
    patterns = []
    tags = []
    for intent in dataset['intents']:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            tags.append(intent['tag'])
    vectorizer = TfidfVectorizer(stop_words='english')
    patterns_tfidf = vectorizer.fit_transform(patterns)
    return patterns_tfidf, tags, vectorizer
