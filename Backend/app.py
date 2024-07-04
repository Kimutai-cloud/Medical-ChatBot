import json
import os
import pickle
from flask import Flask, request, jsonify, send_from_directory
from model import create_model, train_model
from preprocess import preprocess_data

app = Flask(__name__, static_folder="../frontend", static_url_path="")

MODEL_PATH = "model.pkl"
VECTOR_PATH = "vectorizer.pkl"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "Data", "dataset.json")
FEEDBACK_PATH = os.path.join(os.path.dirname(__file__), "..", "Data", "feedback.json")

def load_dataset():
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def ensure_model_trained():
    global model, vectorizer
    dataset = load_dataset()
    if not hasattr(model, 'steps'):
        print("Model not trained or loaded, creating new model...")
        patterns_tfidf, tags, vectorizer = preprocess_data(dataset)
        model = train_model(patterns_tfidf, tags)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        with open(VECTOR_PATH, 'wb') as f:
            pickle.dump(vectorizer, f)
        print("Model trained and saved.")
    else:
        print("Model already trained and loaded.")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    print(f"Received question: {question}")

    ensure_model_trained()

    try:
        question_tfidf = vectorizer.transform([question])
        tag = model.predict(question_tfidf)[0]
        response = next(intent for intent in dataset['intents'] if intent['tag'] == tag)['responses'][0]
        print(f"Predicted tag: {tag}, Response: {response}")
        return jsonify({"answer": response})
    except Exception as e:
        print(f"Error predicting response: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    answer = data.get('answer')
    feedback = data.get('feedback')

    feedback_data = {"answer": answer, "feedback": feedback}

    if os.path.exists(FEEDBACK_PATH):
        try:
            with open(FEEDBACK_PATH, 'r') as f:
                feedback_list = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            feedback_list = []
    else:
        feedback_list = []

    feedback_list.append(feedback_data)

    with open(FEEDBACK_PATH, 'w') as f:
        json.dump(feedback_list, f)

    return jsonify({"status": "Feedback received"})

if __name__ == '__main__':
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            dataset = json.load(f)
    else:
        dataset = {"intents": []}

    if os.path.exists(MODEL_PATH) and os.path.exists(VECTOR_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTOR_PATH, 'rb') as vf:
            vectorizer = pickle.load(vf)
    else:
        model = create_model()
        vectorizer = None

    ensure_model_trained()
    app.run(debug=True)
