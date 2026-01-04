from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Ensure backend directory is in path if needed (standard import should work if run from root as python backend/app.py)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyst import YouTubeAnalyst

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

analyst = YouTubeAnalyst()

# Path to the dataset in the root directory
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Global YouTube Statistics.csv')

def initialize_model():
    """Initializes the model if dataset exists."""
    if os.path.exists(DATASET_PATH):
        print(f"Loading dataset from {DATASET_PATH}...")
        try:
            analyst.load_and_prep_data(DATASET_PATH)
            print("Training models...")
            analyst.train_models()
            print("Model trained and ready.")
            return True
        except Exception as e:
            print(f"Error initializing model: {e}")
            return False
    else:
        print(f"Dataset not found at {DATASET_PATH}. Please ensure the file is present.")
        return False

# Initialize on startup
model_ready = initialize_model()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_ready": model_ready}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model_ready:
        return jsonify({"error": "Model not initialized. Dataset missing?"}), 503
        
    try:
        data = request.json
        # Expected keys: subscribers, video views, etc.
        prediction = analyst.predict(data)
        accuracy_metrics = analyst.get_model_accuracy()
        r2_score = accuracy_metrics.get("r2", 0)
        return jsonify({"prediction": prediction, "accuracy": r2_score})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    if not model_ready:
        return jsonify({"error": "Model not initialized"}), 503
    
    try:
        importance = analyst.get_feature_importances()
        return jsonify(importance)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/model-accuracy', methods=['GET'])
def model_accuracy():
    if not model_ready:
        return jsonify({"error": "Model not initialized"}), 503
        
    try:
        accuracy = analyst.get_model_accuracy()
        return jsonify(accuracy)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
