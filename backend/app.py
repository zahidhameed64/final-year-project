from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import datetime
import os

app = Flask(__name__)
CORS(app)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Model file not found. Please run train_model.py first.")

load_model()

import traceback

def safe_float(value, default=0.0):
    try:
        if value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        load_model()
        if not model:
            return jsonify({'error': 'Model not loaded. Ensure model.joblib exists.'}), 500
        
    data = request.json
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    print("Received data:", data) # Debug input

    try:
        # Extract features with defaults
        input_data = {
            'subscribers': [safe_float(data.get('subscribers'))],
            'video views': [safe_float(data.get('video_views'))],
            'uploads': [safe_float(data.get('uploads'))],
            'created_year': [safe_float(data.get('created_year'), datetime.datetime.now().year)],
            'category': [str(data.get('category', 'Unknown'))],
            'Country': [str(data.get('country', 'Unknown'))],
            'Title': [str(data.get('title', 'Unknown'))],
            'channel_type': [str(data.get('channel_type', 'Unknown'))]
        }
        
        df_input = pd.DataFrame(input_data)
        
        # --- Feature Engineering ---
        # Log transformations
        df_input['log_views'] = np.log1p(df_input['video views'])
        df_input['log_subs'] = np.log1p(df_input['subscribers'])
        df_input['log_uploads'] = np.log1p(df_input['uploads'])
        
        # Channel Age
        current_year = datetime.datetime.now().year
        df_input['channel_age'] = current_year - df_input['created_year']
        
        # Engagement Ratios
        df_input['views_per_upload'] = df_input['video views'] / (df_input['uploads'] + 1)
        df_input['subs_per_upload'] = df_input['subscribers'] / (df_input['uploads'] + 1)
        
        # Drop columns not used in model (must match training cleanup)
        drop_cols = ['created_year', 'channel_type']
        df_input = df_input.drop(columns=[c for c in drop_cols if c in df_input.columns])

        # Make prediction
        prediction = model.predict(df_input)
        
        return jsonify({
            'success': True,
            'predicted_earnings': float(prediction[0])
        })
        
    except Exception as e:
        print("Error during prediction:")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
