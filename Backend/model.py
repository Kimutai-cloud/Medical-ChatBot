from sklearn.pipeline import make_pipeline
from sklearn.svm import LinearSVC

def create_model():
    return make_pipeline(LinearSVC())

def train_model(patterns_tfidf, tags):
    model = create_model()
    model.fit(patterns_tfidf, tags)
    return model
