from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def create_model():
    return make_pipeline(TfidfVectorizer(), LogisticRegression())

def train_model(patterns, tags):
    model = create_model()
    model.fit(patterns, tags)
    return model