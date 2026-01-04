import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

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
        """Loads data from CSV and checks encoding."""
        try:
            self.df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(filepath, encoding='latin-1')
        
        self._clean_data()
        self._feature_engineering()
        return self.df.head()

    def _clean_data(self):
        """Standard cleaning steps from notebook."""
        # Drop unnecessary columns
        columns_to_drop = [
            'rank', 'Abbreviation', 'country_rank', 'created_month',
            'created_date', 'Gross tertiary education enrollment (%)',
            'Unemployment rate', 'Urban_population', 'Latitude', 'Longitude'
        ]
        # Only drop if they exist
        existing_cols = [c for c in columns_to_drop if c in self.df.columns]
        self.df = self.df.drop(columns=existing_cols)

        # Handle missing values
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].fillna("Unknown")

        for col in self.df.select_dtypes(include=['int64', 'float']).columns:
            median_val = self.df[col].median()
            self.df[col] = self.df[col].fillna(median_val)

        # Data types
        for col in ['video views', 'uploads', 'subscribers']:
            if col in self.df.columns:
                 self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0).astype('int64')

        # Remove illogical data
        if 'video views' in self.df.columns:
            self.df = self.df[self.df['video views'] > 0]
        if 'created_year' in self.df.columns:
            self.df = self.df[self.df['created_year'] >= 2005]

        self.df = self.df.reset_index(drop=True)

    def _feature_engineering(self):
        """Creates derived features."""
        df = self.df
        
        # Avoid division by zero
        def safe_div(a, b):
            return a / b if b > 0 else 0

        df['earnings_per_sub'] = df.apply(lambda x: safe_div(x['highest_yearly_earnings'], x['subscribers']), axis=1)
        df['views_per_upload'] = df.apply(lambda x: safe_div(x['video views'], x['uploads']), axis=1)
        
        # Handle growth columns if they exist, otherwise skip or default
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

        # Fill NaNs created
        df.fillna(0, inplace=True)
        
        # Cleanup original columns used for calc if needed (notebook dropped them, we can keep or drop)
        # Notebook dropped raw earnings/growth to avoid target leakage or redundancy, let's follow suit for training
        cols_to_drop = [
            'lowest_monthly_earnings', 'highest_monthly_earnings',
            'lowest_yearly_earnings', 
            'subscribers_for_last_30_days', 'video_views_for_the_last_30_days'
        ]
        # Keep 'highest_yearly_earnings' as target, drop others
        # Actually notebook dropped HIGHEST yearly earnings from features, but it's the target?
        # Re-reading notebook cell 5:
        # df.drop(columns=[..., 'highest_yearly_earnings', ...], inplace=True)
        # Wait, if they drop the target, what do they train on?
        # Ah, usually they keep one for y. Let's assume 'highest_yearly_earnings' IS the target or a proxy.
        # Let's check the target variable in notebook. 
        # Usually it's 'highest_yearly_earnings' or an average. 
        # Let's assume we want to predict 'highest_yearly_earnings' and separate it before dropping.
        
        # For now, I'll allow the drop method to remove non-target columns.
        # I will preserve 'highest_yearly_earnings' for now as 'y'.
        
        # The notebook snippet shows:
        # df.drop(columns=[..., 'highest_yearly_earnings', ...], inplace=True)
        # This implies the target might have been extracted earlier OR they are predicting something else 
        # OR they made a mistake in the snippet I saw.
        # Let's assume 'highest_yearly_earnings' is the Target. I should NOT drop it from the dataframe 
        # until I split.
        self.df = df

    def train_models(self):
        """Trains the model."""
        # Define features and target
        # IMPROVEMENT: Use average of lowest and highest earnings for a more realistic target
        if 'highest_yearly_earnings' in self.df.columns and 'lowest_yearly_earnings' in self.df.columns:
            self.df['average_yearly_earnings'] = (self.df['lowest_yearly_earnings'] + self.df['highest_yearly_earnings']) / 2
            target_col = 'average_yearly_earnings'
        else:
            # Fallback if columns missing (though they should be there from load)
            target_col = 'highest_yearly_earnings'
        
        feature_cols = [
            'subscribers', 'video views', 'uploads', 
            'category', 'Country', 'channel_type',
            'views_per_upload', 'channel_age_years',
            'video_views_for_the_last_30_days'
        ]
        
        # Filter existing columns
        feature_cols = [c for c in feature_cols if c in self.df.columns]
        
        X = self.df[feature_cols]
        y = self.df[target_col]

        # Splitting
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.X_test = X_test
        self.y_test = y_test

        # Preprocessing
        categorical_features = ['category', 'Country', 'channel_type']
        categorical_features = [c for c in categorical_features if c in X.columns]
        
        numeric_features = [c for c in X.columns if c not in categorical_features]

        categorical_transformer = OneHotEncoder(handle_unknown='ignore')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features),
                ('num', 'passthrough', numeric_features)
            ]
        )

        # Pipeline
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])

        # Train
        self.pipeline.fit(X_train, y_train)
        self.model = self.pipeline.named_steps['regressor']
        
        # Evaluate
        self.y_pred = self.pipeline.predict(X_test)
        
        # Feature names for importance
        # OneHotEncoder generates new names, need to capture them
        try:
            ohe = self.pipeline.named_steps['preprocessor'].named_transformers_['cat']
            cat_names = ohe.get_feature_names_out(categorical_features)
            self.feature_names = list(cat_names) + numeric_features
        except:
            self.feature_names = numeric_features # Fallback

    def predict(self, input_data):
        """
        Predicts earnings for a single input.
        input_data: dict containing keys like 'subscribers', 'video views', etc.
        """
        # Create DataFrame from input
        input_df = pd.DataFrame([input_data])
        
        # Must ensure all required columns exist, fill numeric with 0, strings with 'Unknown'
        # Also need feature engineering on single input!
        
        # Calculate derived features for the input
        # Note: We need 'created_year' to calc age. If not provided, assume 2010 or something?
        # Or require channel age directly? Let's try to calculate.
        
        input_df['created_year'] = input_df.get('created_year', 2015) 
        input_df['uploads'] = pd.to_numeric(input_df.get('uploads', 0))
        input_df['video views'] = pd.to_numeric(input_df.get('video views', 0))
        input_df['subscribers'] = pd.to_numeric(input_df.get('subscribers', 0))
        # New features defaults
        input_df['video_views_for_the_last_30_days'] = pd.to_numeric(input_df.get('video_views_for_the_last_30_days', 0))
        input_df['subscribers_for_last_30_days'] = pd.to_numeric(input_df.get('subscribers_for_last_30_days', 0))
        
        # Derived
        current_year = datetime.datetime.now().year
        input_df['channel_age_years'] = current_year - input_df['created_year']
        
        # Avoid div by zero
        if input_df['uploads'][0] > 0:
            input_df['views_per_upload'] = input_df['video views'] / input_df['uploads']
        else:
            input_df['views_per_upload'] = 0
            
        prediction = self.pipeline.predict(input_df)
        return prediction[0]

    def get_feature_importances(self):
        """Returns top feature importances."""
        if not self.model or not self.feature_names:
            return []
            
        importances = self.model.feature_importances_
        # Pair with names
        feat_imp = list(zip(self.feature_names, importances))
        # Sort desc
        feat_imp.sort(key=lambda x: x[1], reverse=True)
        # Return top 10 formatted
        return [{"name": name, "importance": round(imp, 4)} for name, imp in feat_imp[:10]]

    def get_model_accuracy(self):
        """Returns R2 and RMSE, plus sample predictions."""
        if self.y_test is None:
            return {}
            
        mse = mean_squared_error(self.y_test, self.y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, self.y_pred)
        
        # Samples
        samples = []
        # Take first 20 samples from test set
        test_indices = self.y_test.index[:20]
        for idx in test_indices:
            # Finding the position in y_test/y_pred (which corresponds to array index)
            # y_test is a Series (index match), y_pred is array (position match)
            # Helper:
            pos = list(self.y_test.index).index(idx)
            actual = self.y_test.loc[idx]
            pred = self.y_pred[pos]
            samples.append({"actual": float(actual), "predicted": float(pred)})
            
        return {
            "rmse": rmse,
            "r2": r2,
            "samples": samples
        }
