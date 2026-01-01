# Chapter 8: Appendix - Source Code

This appendix contains the full source code for the critical components of the system.

## A.1 Backend Implementation

### `backend/analyst.py`
This module contains the `YouTubeAnalyst` class, responsible for Data Cleaning, Feature Engineering, and Random Forest Training.

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

class YouTubeAnalyst:
    def __init__(self):
        self.pipeline = None
        self.model = None
        self.feature_names = None
        self.df = None
        self.X_test = None
        self.y_test = None
        self.y_pred = None

    def load_and_prep_data(self, filepath):
        try:
            self.df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(filepath, encoding='latin-1')
        
        self._clean_data()
        self._feature_engineering()
        return self.df.head()

    def _clean_data(self):
        columns_to_drop = [
            'rank', 'Abbreviation', 'country_rank', 'created_month',
            'created_date', 'Gross tertiary education enrollment (%)',
            'Unemployment rate', 'Urban_population', 'Latitude', 'Longitude'
        ]
        existing_cols = [c for c in columns_to_drop if c in self.df.columns]
        self.df = self.df.drop(columns=existing_cols)

        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].fillna("Unknown")

        for col in self.df.select_dtypes(include=['int64', 'float']).columns:
            median_val = self.df[col].median()
            self.df[col] = self.df[col].fillna(median_val)

        for col in ['video views', 'uploads', 'subscribers']:
            if col in self.df.columns:
                 self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0).astype('int64')

        if 'video views' in self.df.columns:
            self.df = self.df[self.df['video views'] > 0]
        if 'created_year' in self.df.columns:
            self.df = self.df[self.df['created_year'] >= 2005]

        self.df = self.df.reset_index(drop=True)

    def _feature_engineering(self):
        df = self.df
        def safe_div(a, b):
            return a / b if b > 0 else 0

        df['earnings_per_sub'] = df.apply(lambda x: safe_div(x['highest_yearly_earnings'], x['subscribers']), axis=1)
        df['views_per_upload'] = df.apply(lambda x: safe_div(x['video views'], x['uploads']), axis=1)
        
        if 'subscribers_for_last_30_days' in df.columns:
             df['subscribers_growth_rate'] = df.apply(lambda x: safe_div(x['subscribers_for_last_30_days'], x['subscribers']), axis=1)
        else:
             df['subscribers_growth_rate'] = 0

        if 'video_views_for_the_last_30_days' in df.columns:
            df['video_views_growth_rate'] = df.apply(lambda x: safe_div(x['video_views_for_the_last_30_days'], x['video views']), axis=1)
        else:
            df['video_views_growth_rate'] = 0

        current_year = datetime.datetime.now().year
        df['channel_age_years'] = current_year - df['created_year']
        df.fillna(0, inplace=True)
        self.df = df

    def train_models(self):
        if 'highest_yearly_earnings' in self.df.columns and 'lowest_yearly_earnings' in self.df.columns:
            self.df['average_yearly_earnings'] = (self.df['lowest_yearly_earnings'] + self.df['highest_yearly_earnings']) / 2
            target_col = 'average_yearly_earnings'
        else:
            target_col = 'highest_yearly_earnings'
        
        feature_cols = [
            'subscribers', 'video views', 'uploads', 
            'category', 'Country', 'channel_type',
            'views_per_upload', 'channel_age_years',
            'video_views_for_the_last_30_days', 'subscribers_for_last_30_days'
        ]
        
        feature_cols = [c for c in feature_cols if c in self.df.columns]
        
        X = self.df[feature_cols]
        y = self.df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.X_test = X_test
        self.y_test = y_test

        categorical_features = ['category', 'Country', 'channel_type']
        categorical_features = [c for c in categorical_features if c in X.columns]
        numeric_features = [c for c in X.columns if c not in categorical_features]

        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                ('num', 'passthrough', numeric_features)
            ]
        )

        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])

        self.pipeline.fit(X_train, y_train)
        self.model = self.pipeline.named_steps['regressor']
        self.y_pred = self.pipeline.predict(X_test)

    def predict(self, input_data):
        input_df = pd.DataFrame([input_data])
        input_df['created_year'] = input_df.get('created_year', 2015) 
        input_df['uploads'] = pd.to_numeric(input_df.get('uploads', 0))
        input_df['video views'] = pd.to_numeric(input_df.get('video views', 0))
        input_df['subscribers'] = pd.to_numeric(input_df.get('subscribers', 0))
        input_df['video_views_for_the_last_30_days'] = pd.to_numeric(input_df.get('video_views_for_the_last_30_days', 0))
        input_df['subscribers_for_last_30_days'] = pd.to_numeric(input_df.get('subscribers_for_last_30_days', 0))
        
        current_year = datetime.datetime.now().year
        input_df['channel_age_years'] = current_year - input_df['created_year']
        
        if input_df['uploads'][0] > 0:
            input_df['views_per_upload'] = input_df['video views'] / input_df['uploads']
        else:
            input_df['views_per_upload'] = 0
            
        prediction = self.pipeline.predict(input_df)
        return prediction[0]

    def get_feature_importances(self):
        if not self.model: return []
        importances = self.model.feature_importances_
        # Note: mapping names back to features is complex with OHE, simplified here
        return [] 

    def get_model_accuracy(self):
        if self.y_test is None: return {}
        mse = mean_squared_error(self.y_test, self.y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, self.y_pred)
        return {"rmse": rmse, "r2": r2}
```

## A.2 Frontend Implementation

### `frontend/src/components/PredictionForm.tsx` (Partial)
This React component handles the user input and API communication.

```tsx
"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function PredictionForm({ onPrediction }: { onPrediction: (data: any) => void }) {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    subscribers: "",
    video_views: "",
    uploads: "",
    category: "Entertainment",
    country: "United States"
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subscribers: Number(formData.subscribers),
          "video views": Number(formData.video_views),
          uploads: Number(formData.uploads),
          category: formData.category,
          Country: formData.country,
          // Defaults for other fields
          created_year: 2015,
          video_views_for_the_last_30_days: Number(formData.video_views) * 0.05 // Heuristic
        })
      })
      const data = await response.json()
      onPrediction(data)
    } catch (error) {
      console.error("Prediction failed:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Channel Statistics</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input 
            placeholder="Subscribers" 
            type="number"
            value={formData.subscribers}
            onChange={(e) => setFormData({...formData, subscribers: e.target.value})}
          />
          {/* Other inputs omitted for brevity */}
          <Button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Predict Earnings"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
```
