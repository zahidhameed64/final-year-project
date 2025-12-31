import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import datetime
import os

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'Global YouTube Statistics.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model.joblib')

def load_and_clean_data(filepath):
    # Load data
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='latin-1')
        
    # Cell 3 cleaning
    columns_to_drop = [
        'rank', 'Abbreviation', 'country_rank', 'created_month',
        'created_date', 'Gross tertiary education enrollment (%)',
        'Unemployment rate', 'Urban_population', 'Latitude', 'Longitude'
    ]
    # Check if columns exist before dropping to be safe
    existing_cols_to_drop = [c for c in columns_to_drop if c in df.columns]
    df = df.drop(columns=existing_cols_to_drop)
    
    # Fill NA
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna("Unknown")
        
    for col in df.select_dtypes(include=['int64', 'float']).columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        
    # Correct Data Types
    for col in ['video views', 'uploads', 'subscribers']:
        if col in df.columns:
             df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
             
    # Remove illogical data
    if 'video views' in df.columns:
        df = df[df['video views'] > 0]
    if 'created_year' in df.columns:
        df = df[df['created_year'] >= 2005]
        
    # Sort
    if 'subscribers' in df.columns:
        df = df.sort_values(by='subscribers', ascending=False).reset_index(drop=True)
        
    return df

def feature_engineering(df):
    df_ml = df.copy()
    
    # Outlier removal
    if 'Youtuber' in df_ml.columns:
        df_ml = df_ml[~df_ml['Youtuber'].str.contains('KIMPRO|ýýý', case=False, na=False)]
        
    # Log transform
    for col, source in [('log_views', 'video views'), ('log_subs', 'subscribers'), ('log_uploads', 'uploads')]:
        if source in df_ml.columns:
            df_ml[col] = np.log1p(df_ml[source])
            
    # Channel Age
    if 'created_year' in df_ml.columns:
        current_year = datetime.datetime.now().year
        df_ml['channel_age'] = current_year - df_ml['created_year']
        
    # Engagement Ratios
    if all(x in df_ml.columns for x in ['video views', 'uploads', 'subscribers']):
        df_ml['views_per_upload'] = df_ml['video views'] / (df_ml['uploads'] + 1)
        df_ml['subs_per_upload'] = df_ml['subscribers'] / (df_ml['uploads'] + 1)
        
    # Target Variable
    if 'lowest_yearly_earnings' in df_ml.columns and 'highest_yearly_earnings' in df_ml.columns:
        df_ml['avg_yearly_earnings'] = (df_ml['lowest_yearly_earnings'] + df_ml['highest_yearly_earnings']) / 2
        
    # Cleanup
    cols_to_drop = ['lowest_monthly_earnings', 'highest_monthly_earnings',
                           'lowest_yearly_earnings', 'highest_yearly_earnings',
                           'Youtuber', 'created_year']
    existing_to_drop = [c for c in cols_to_drop if c in df_ml.columns]
    df_ml = df_ml.drop(columns=existing_to_drop)
    
    return df_ml

def train_and_save_model(df_ml):
    # Define Features and Target
    # We explicitly select only features available in the frontend app
    feature_cols = [
        'subscribers', 'video views', 'uploads', 
        'category', 'Country', 'Title',
        'log_views', 'log_subs', 'log_uploads', 
        'channel_age', 'views_per_upload', 'subs_per_upload'
    ]
    # Ensure these cols exist (Title might be Youtuber in some contexts but we checked Cell 2)
    existing_feats = [c for c in feature_cols if c in df_ml.columns]
    
    X = df_ml[existing_feats]
    y = df_ml['avg_yearly_earnings']
    
    # Identify Numeric and Categorical
    numeric_features = X.select_dtypes(include=np.number).columns.tolist()
    categorical_features = X.select_dtypes(exclude=np.number).columns.tolist()
    
    print(f"Numeric features: {numeric_features}")
    print(f"Categorical features: {categorical_features}")

    # Create Pipelines
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    # Model Pipeline (Gradient Boosting)
    gb_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('model', GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42))])
                                  
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    print("Training Gradient Boosting model...")
    gb_pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = gb_pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"R-squared: {r2:.3f}")
    print(f"RMSE: ${rmse:,.2f}")
    
    # Save
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(gb_pipeline, MODEL_PATH)
    print("Model saved.")

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
    else:
        print("Loading data...")
        df = load_and_clean_data(DATA_PATH)
        print("Feature engineering...")
        df_ml = feature_engineering(df)
        print("Training...")
        train_and_save_model(df_ml)
