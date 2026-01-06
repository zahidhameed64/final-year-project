# Chapter 8: Appendices

## Appendix A: Source Code Listings

This appendix contains the complete source code for the "Youtube Income Predictor" application.

### A.1 Backend Implementation

#### A.1.1 `backend/app.py` (Main Flask Application)
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyst import YouTubeAnalyst

app = Flask(__name__)
CORS(app)

analyst = YouTubeAnalyst()
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Global YouTube Statistics.csv')

def initialize_model():
    if os.path.exists(DATASET_PATH):
        try:
            analyst.load_and_prep_data(DATASET_PATH)
            analyst.train_models()
            return True
        except Exception as e:
            return False
    return False

model_ready = initialize_model()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_ready": model_ready}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model_ready:
        return jsonify({"error": "Model not ready"}), 503
    try:
        data = request.json
        prediction = analyst.predict(data)
        accuracy = analyst.get_model_accuracy().get("r2", 0)
        return jsonify({"prediction": prediction, "accuracy": accuracy})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### A.1.2 `backend/analyst.py` (Machine Learning Logic)
```python
import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

class YouTubeAnalyst:
    def __init__(self):
        self.pipeline = None
        self.model = None
        self.df = None

    def load_and_prep_data(self, filepath):
        try:
            self.df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(filepath, encoding='latin-1')
        self._clean_data()
        self._feature_engineering()

    def _clean_data(self):
        # Cleaning steps
        cols_drop = ['rank', 'Abbreviation', 'Latitude', 'Longitude']
        self.df = self.df.drop(columns=[c for c in cols_drop if c in self.df.columns])
        
        # Imputation
        for col in self.df.select_dtypes(include=['int64', 'float']).columns:
            self.df[col] = self.df[col].fillna(self.df[col].median())
        
        # Validation
        if 'video views' in self.df.columns:
            self.df = self.df[self.df['video views'] > 0]

    def _feature_engineering(self):
        self.df['views_per_upload'] = self.df['video views'] / self.df['uploads'].replace(0, 1)
        self.df['channel_age'] = datetime.datetime.now().year - self.df['created_year']
        # Target creation
        self.df['average_earnings'] = (self.df['lowest_yearly_earnings'] + self.df['highest_yearly_earnings']) / 2

    def train_models(self):
        X = self.df[['subscribers', 'video views', 'uploads', 'category', 'Country']]
        y = self.df['average_earnings']
        
        preprocessor = ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['category', 'Country']),
            ('num', 'passthrough', ['subscribers', 'video views', 'uploads'])
        ])
        
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', RandomForestRegressor(n_estimators=100))
        ])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.pipeline.fit(X_train, y_train)
        self.y_test = y_test
        self.y_pred = self.pipeline.predict(X_test)

    def predict(self, input_data):
        input_df = pd.DataFrame([input_data])
        # Add basic feature engineering for single input
        input_df['uploads'] = pd.to_numeric(input_df.get('uploads', 1))
        return self.pipeline.predict(input_df)[0]
```

### A.2 Frontend Implementation

#### A.2.1 `frontend/src/components/PredictionForm.tsx` (User Interface)
```tsx
"use client";
import { useState } from "react";
// ... imports

export function PredictionForm() {
    const [result, setResult] = useState<number | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        const payload = {
            subscribers: Number(formData.get("subscribers")),
            "video views": Number(formData.get("views")),
            category: formData.get("category"),
            Country: formData.get("country")
        };

        const response = await fetch("http://localhost:5000/api/predict", {
            method: "POST",
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        setResult(data.prediction);
    };

    return (
        <form onSubmit={handleSubmit}>
            {/* Input fields for Subscribers, Views, etc. */}
             <Input name="subscribers" placeholder="Subscribers" />
             <Input name="views" placeholder="Video Views" />
             <Button type="submit">Predict</Button>
        </form>
    );
}
```

## Appendix B: Dataset Sample

This appendix includes the first 20 records of the **Global YouTube Statistics** dataset used for training.

| Rank | Youtuber | Subscribers | Video Views | Category | Uploads | Country | Earnings (High) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | T-Series | 245M | 228B | Music | 20K | India | $108M |
| 2 | YouTube Movies | 170M | 0 | Film | 1 | US | $0 |
| 3 | MrBeast | 166M | 28B | Entertainment | 741 | US | $64M |
| 4 | Cocomelon | 162M | 164B | Education | 966 | US | $94M |
| 5 | SET India | 159M | 148B | Shows | 116K | India | $87M |
| 6 | Music | 119M | 0 | Music | 0 | Unknown | $0 |
| 7 | Kids Diana Show | 112M | 93B | People | 1.1K | US | $53M |
| 8 | PewDiePie | 111M | 29B | Gaming | 4.7K | Japan | $4M |
| 9 | Like Nastya | 106M | 90B | People | 4.9K | Russia | $51M |
| 10 | Vlad and Niki | 98M | 77B | Entertainment | 574 | US | $44M |
| 11 | Zee Music | 98M | 57B | Music | 8.5K | India | $33M |
| 12 | WWE | 96M | 77B | Sports | 70K | US | $44M |
| 13 | Gaming | 93M | 0 | Gaming | 0 | Unknown | $0 |
| 14 | BLACKPINK | 89M | 32B | Music | 537 | South Korea | $18M |
| 15 | Goldmines | 87M | 24B | Film | 6.5K | India | $13M |
| 16 | 5-Minute Crafts | 80M | 26B | Howto | 6.2K | US | $15M |
| 17 | BANGTANTV | 75M | 20B | Music | 2.2K | South Korea | $11M |
| 18 | Sports | 75M | 0 | Sports | 0 | Unknown | $0 |
| 19 | Justin Bieber | 71M | 30B | Music | 249 | Canada | $17M |
| 20 | HYBE LABELS | 71M | 28B | Music | 1.3K | South Korea | $16M |

*(Note: Data truncated for brevity. Full dataset contains 995 records.)*
