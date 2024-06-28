import json
import os
import pickle
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model import create_model, train_model
from preprocess import preprocess_data

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "Data", "dataset.json")

def ensure_model_trained():
    global model, vectorizer, dataset
    if not os.path.exists(DATA_PATH):
        dataset = {"intents": []}
        with open(DATA_PATH, 'w') as f:
            json.dump(dataset, f)
    else:
        with open(DATA_PATH, 'r') as f:
            dataset = json.load(f)

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("Model or vectorizer not found, creating new ones...")
        patterns_tfidf, tags, vectorizer = preprocess_data(dataset)
        model = train_model(patterns_tfidf, tags)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        with open(VECTORIZER_PATH, 'wb') as f:
            pickle.dump(vectorizer, f)
        print("Model and vectorizer trained and saved.")
    else:
        print("Loading model and vectorizer...")
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        print("Model and vectorizer loaded.")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    print(f"Received question: {question}")

    ensure_model_trained()  # Ensure model is trained

    try:
        question_tfidf = vectorizer.transform([question])
        tag = model.predict(question_tfidf)[0]
        response = next(intent for intent in dataset['intents'] if intent['tag'] == tag)['responses'][0]
        print(f"Predicted tag: {tag}, Response: {response}")
        return jsonify({"answer": response})
    except Exception as e:
        print(f"Error predicting response: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = json.load(file)

    global dataset
    dataset['intents'].extend(data['intents'])

    patterns_tfidf, tags, vectorizer = preprocess_data(dataset)
    model = train_model(patterns_tfidf, tags)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    with open(DATA_PATH, 'w') as f:
        json.dump(dataset, f)

    return jsonify({"status": "Model updated successfully"})

if __name__ == '__main__':
    ensure_model_trained()
    app.run(debug=True)
