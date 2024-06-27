from flask import Flask, request, jsonify
import os
import pickle
import json 
from model import create_model, train_model
from preprocess import preprocess_data

app = Flask(__name__)

MODEL_PATH = "model.pkl"
DATA_PATH = "data.json"

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    model = create_model()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = json.load(file)

    global dataset
    dataset['intent'].extenf(data['intent'])

    patterns, tags = preprocess_data(dataset)
    model = train_model(patterns, tags)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model,f)

    with open(DATA_PATH, 'w') as f:
        json.dump(dataset, f)
    
    return jsonify ({"Status": "Model Updated Successfully"})

if __name__ == '__main__';
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            dataset = json.load(f)
    
    else:
        dataset = {"intents": []}
    
    app.run(debug=True)