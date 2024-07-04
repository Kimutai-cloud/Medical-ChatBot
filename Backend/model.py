from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

def create_model():
    return make_pipeline(LogisticRegression(max_iter=200))

def train_model(patterns_tfidf, tags):
    model = create_model()
    model.fit(patterns_tfidf, tags)
    return model
