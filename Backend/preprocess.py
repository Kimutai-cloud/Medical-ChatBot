import json
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_data(data):
    vectorizer = TfidfVectorizer()
    patterns = [pattern for intent in data['intents'] for pattern in intent['patterns']]
    
    if not patterns:
        raise ValueError("Empty patterns list")
    
    patterns_tfidf = vectorizer.fit_transform(patterns)
    tags = [intent['tag'] for intent in data['intents'] for _ in intent['patterns']]
    return patterns_tfidf, tags, vectorizer
