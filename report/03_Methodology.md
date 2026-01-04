# Chapter 3: Methodology

## 3.1 Introduction

This chapter outlines the systematic approach used to develop the "YouTube Income Predictor." It details the software development lifecycle, the system architecture, the data pipeline (collection, cleaning, preprocessing), and the specific machine learning methodologies applied to train the predictive models.

## 3.2 System Architecture

The project follows a standard client-server architecture, decoupled to allow for independent development and scalability of the frontend and backend.

### 3.2.1 High-Level Design
The system consists of three main layers:
1.  **Presentation Layer (Frontend):** A Next.js (React) application serving as the user interface. It handles user inputs (channel statistics), sends HTTP requests to the backend, and renders the returned JSON data into interactive charts and dashboards.
2.  **Application Logic Layer (Backend):** A Flask (Python) server. This layer hosts the `YouTubeAnalyst` class, which encapsulates the machine learning logic. It exposes RESTful API endpoints (e.g., POST `/api/predict`, GET `/api/model-accuracy`).
3.  **Data Layer:**
    *   **Raw Data:** The `Global YouTube Statistics.csv` file acting as the training knowledge base.
    *   **Model Artifacts:** The trained Random Forest model and preprocessing pipelines stored in memory (or serialized via `joblib/pickle` in production environments) during the application lifecycle.

### 3.2.2 Data Flow
1.  **Training Phase (Startup):** Upon starting the Flask server (`app.py`), the system triggers `analyst.load_and_prep_data()`. It reads the CSV, cleans it, trains the model, and holds the model object in global state.
2.  **Inference Phase (User Interaction):**
    *   User enters data (e.g., Subscribers: 1M, Views: 500M) in the Frontend `PredictionForm`.
    *   Frontend sends a JSON payload to Backend `/api/predict`.
    *   Backend `predict()` method creates a mini-dataframe for the single input, runs it through the preprocessing pipeline (scaling/encoding), and passes it to the Random Forest model.
    *   The predicted float value (Earnings) is returned as JSON.
    *   Frontend displays the result.

## 3.3 Data Collection and Understanding

### 3.3.1 Dataset Source
The dataset used is the "Global YouTube Statistics" dataset (commonly available on platforms like Kaggle). It contains comprehensive metrics for top YouTube channels worldwide.

### 3.3.2 Key Features
The raw dataset includes columns such as:
*   **Numerical:** `subscribers`, `video analysis` (views), `uploads`, `highest_yearly_earnings`, `lowest_yearly_earnings`, `created_year`.
*   **Categorical:** `category`, `Country`, `channel_type`.
*   **Target Variable:** The primary target for prediction is the channel's earning potential. Since the dataset provides a range (`lowest` to `highest`), the system engineers a proxy target (often the `highest_yearly_earnings` or an average) to train the regressor.

## 3.4 Data Preprocessing Pipeline

Raw data is rarely suitable for direct machine learning. The `YouTubeAnalyst` class implements a rigorous cleaning and engineering pipeline.

### 3.4.1 Data Cleaning
1.  **Handling Missing Values:**
    *   *Categorical:* Missing values in columns like `Country` or `category` are filled with a placeholder "Unknown".
    *   *Numerical:* Missing values in columns like `video views` are imputed using the **median** of the column to be robust against outliers.
2.  **Type Conversion:** Ensuring columns meant to be numeric (like `subscribers`) are stripped of non-numeric characters and cast to `int` or `float`.
3.  **Outlier Removal:** Rows with illogical data (e.g., negative views, year < 2005) or extreme edge cases that might skew the model are removed.

### 3.4.2 Feature Engineering
New features were derived to provide the model with better signals:
*   **Traffic Quality:** `views_per_upload` = Total Views / Total Uploads. High views per video often correlate better with earnings than total views alone.
*   **Channel Age:** `channel_age_years` = Current Year - `created_year`. Impacting the maturity and library size of the channel.
*   **Growth Rate:** `subscribers_growth_rate` (if temporal data is available) to indicate trending status.

### 3.4.3 Encoding and Scaling
Machine learning models require numerical input.
*   **One-Hot Encoding:** Applied to categorical variables (`category`, `channel_type`, `Country`). This converts a column like "Category" with values ["Music", "Gaming"] into binary columns [`Category_Music`, `Category_Gaming`].
*   **Pipeline Integration:** These steps are wrapped in a Scikit-Learn `ColumnTransformer` to ensure the exact same transformations are applied to both the training set and new user input during prediction.

## 3.5 Model Selection and Training

### 3.5.1 Algorithm: Random Forest Regressor
The Random Forest algorithm was selected for its comprehensive strengths:
*   **Non-Linearity:** It can capture complex relationships (e.g., earnings might not scale linearly with views).
*   **Robustness:** Less prone to overfitting than a single Decision Tree.
*   **Feature Importance:** It naturally provides scores indicating which features contributed most to the prediction (used in the Dashboard).

### 3.5.2 Training Process
1.  **Splitting:** The data is split into Training (80%) and Testing (20%) sets using `train_test_split`.
2.  **Hyperparameters:** Key parameters like `n_estimators` (number of trees) are set (e.g., 100) to balance performance and speed.
3.  **Fitting:** The model `fit()` method learns the patterns mapping the features ($X$) to the target ($y$).
4.  **Evaluation:** The model is tested against the hold-out test set to calculate `RMSE` (Root Mean Squared Error) and `R²` (Coefficient of Determination).

## 3.6 Summary
The methodology ensures a robust data pipeline. By combining thorough cleaning, intelligent feature engineering, and a powerful ensemble model, the system is designed to produce reliable predictions within a scalable software architecture.
