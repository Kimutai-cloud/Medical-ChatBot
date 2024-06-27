def preprocess_data(dataset):
    patterns = []
    tags = []
    for intent in dataset['intents']:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            tags.append(intent['tag'])
    
    return patterns, tags