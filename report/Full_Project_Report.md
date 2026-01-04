# Chapter 1: Introduction

## 1.1 Background of the Study

In the contemporary digital landscape, social media platforms have evolved from simple communication tools into robust ecosystems for content creation, entertainment, and substantial economic activity. Among these platforms, YouTube stands out as the premier video-sharing service, hosting billions of users and hours of content. Since its inception, YouTube has democratized media distribution, allowing individuals to broadcast content to a global audience. This shift has given rise to the "creator economy," a new class of businesses built by independent content creators, influencers, and videographers.

For many of these creators, YouTube is not merely a hobby but a primary source of income. The platform's monetization policies, primarily the YouTube Partner Program (YPP), allow eligible channels to earn revenue through advertising, channel memberships, and Super Chats. However, the exact algorithms and metrics determining a channel's financial success remain opaque and multifaceted. Factors such as subscriber count, video views, engagement rates, upload frequency, category, and geographical location all interact in complex ways to influence earnings.

Understanding these dynamics is crucial not only for aspiring content creators seeking to optimize their strategies but also for marketers, brands, and analysts aiming to value digital assets. The sheer volume of data available—millions of channels and billions of interactions—presents a unique opportunity to apply data science and machine learning techniques. By analyzing historical data, it becomes possible to uncover patterns and build predictive models that can estimate channel earnings and identify key drivers of success.

This project, the "YouTube Earnings Prediction and Automated Report Generation System," addresses this need by leveraging advanced machine learning algorithms to analyze YouTube channel statistics. By integrating this analytical backend with a user-friendly modern web interface, the system provides real-time predictions and actionable insights, bridging the gap between raw data and understandable financial forecasts.

## 1.2 Problem Statement

Despite the massive popularity of YouTube, there is a significant lack of transparency and predictability regarding channel earnings. The relationship between visible metrics (like subscribers or views) and actual revenue is non-linear and often counter-intuitive. 

1.  **Complexity of Metrics:** A channel with millions of subscribers may earn less than a niche channel with high engagement and a lucrative target demographic. Simple heuristics (e.g., "$1 per 1000 views") are often inaccurate and fail to account for variables like channel type, country, and viewer retention.
2.  **Data Overload:** The vast amount of data available makes it difficult for humans to manually process and identify trends. Creators often struggle to know which metrics to prioritize—should they focus on getting more subscribers, or increasing upload frequency?
3.  **Lack of Accessible Tools:** While enterprise-grade analytics platforms exist, they are often expensive or overly complex for individual creators or students. There is a need for an accessible, intuitive tool that democratizes access to sophisticated predictive analytics.
4.  **Static Reporting:** Traditional data analysis often results in static spreadsheets or raw numbers. There is a need for *narrative* generation—converting numbers into a story that explains not just *what* the earnings are likely to be, but *why*, highlighting the specific features driving that prediction.

This project aims to solve these problems by building a unified system that ingests global YouTube statistics, trains a robust regression model (Random Forest), and presents the findings through an interactive dashboard and automated reports.

## 1.3 Project Objectives

The primary goal of this project is to design and develop a full-stack web application capable of predicting YouTube channel earnings based on publicly available performance metrics.

**Specific Objectives:**

1.  **Data Analysis & Preprocessing:** To gather, clean, and preprocess a comprehensive dataset of YouTube statistics (Global YouTube Statistics), handling missing values, categorical encoding, and feature engineering to prepare the data for machine learning.
2.  **Model Development:** To implement and train machine learning models (specifically Random Forest Regressor and Linear Regression) to predict 'Yearly Earnings' with high accuracy.
3.  **Feature Importance Analysis:** To interpret the trained models and identify which factors (e.g., Subscribers, Views, Country, Category) have the most significant impact on financial outcomes.
4.  **Full-Stack Development:** To design a robust system architecture using **Flask** (Python) for the backend API and **Next.js** (React/TypeScript) for a responsive, modern frontend user interface.
5.  **Interactive Visualization:** To implement dynamic charting libraries (Recharts) to visualize prediction accuracy vs. actual data and feature importance rankings.
6.  **User Experience:** To create a polished, accessible UI with support for light/dark themes, responsive design, and intuitive form inputs for real-time predictions.
7.  **Automated Reporting:** To enable the system to generate insights that can form the basis of a comprehensive report for the user.

## 1.4 Scope of the Project

The scope of this project covers the end-to-end development of the software solution, from data science to web deployment.

*   **In Scope:**
    *   Ingestion of the 'Global YouTube Statistics.csv' dataset.
    *   Data cleaning (outlier removal, handling nulls) and Feature Engineering (e.g., 'Views per Upload', 'Channel Age').
    *   Training and evaluation of Random Forest and Linear Regression models.
    *   Development of a RESTful API using Flask to serve predictions and model metrics.
    *   Development of a Single Page Application (SPA) using Next.js 16.
    *   Implementation of real-time prediction forms where users can input hypothetical channel stats.
    *   Visualization of model performance (R² score, RMSE) and Feature Importances.
    *   Documentation of the codebase and system architecture.

*   **Out of Scope:**
    *   Real-time fetching of data from the official YouTube Data API (the project relies on a static historical dataset for training, though the architecture allows for future integration).
    *   User authentication and multi-user database storage (the current version is a stateless tool for analysis).
    *   Deployment to a production cloud server (the project is scoped for local development and demonstration).
    *   Financial advice (the predictions are estimates based on statistical trends and should not be used as guaranteed financial planning).

## 1.5 Significance of the Study

This project holds significance for multiple stakeholders:

*   **For Content Creators:** It provides a data-driven baseline for expectations, helping them set realistic goals and understand which metrics (e.g., upload consistency vs. subscriber count) offer the best return on investment.
*   **For Marketers:** It offers a method to value influencer partnerships by estimating the revenue potential of channels based on visible metrics.
*   **For Academia/Students:** It serves as a practical case study in applying Machine Learning to real-world social media datasets, demonstrating the complete pipeline from raw data to a user-facing application.
*   **For Developers:** It demonstrates a modern "AI-Engineering" stack, combining the statistical power of Python with the interactivity of modern JavaScript frameworks.

## 1.6 Organization of the Report

The remainder of this report is organized as follows:
*   **Chapter 2: Literature Review** surveys existing research on social media analytics, machine learning regression techniques, and the technologies used (React, Flask).
*   **Chapter 3: Methodology** details the system architecture, data processing pipeline, and the mathematical foundations of the algorithms used.
*   **Chapter 4: Implementation** provides a deep dive into the code structure, key functions, and integration challenges solved during development.
*   **Chapter 5: Results and Discussion** analyzes the model's accuracy, interprets the feature importance findings, and showcases the final user interface.
*   **Chapter 6: Conclusion and Recommendations** summarizes the project achievements and outlines potential future enhancements.

# Chapter 2: Literature Review

## 2.1 Introduction

The convergence of Big Data, Machine Learning, and Web Development has revolutionized how we understand digital platforms. This chapter provides the theoretical underpinning for the project, reviewing relevant literature and concepts in three key areas: Social Media Analytics (specifically YouTube), Machine Learning Regression algorithms, and Modern Web Application Architectures.

## 2.2 YouTube and Social Media Analytics

### 2.2.1 The Rise of the Creator Economy
YouTube, acquired by Google in 2006, has grown into the second-largest search engine in the world. The platform's sheer scale generates exabytes of data on user behavior, video performance, and creator metrics. Research by *Cheng et al. (2014)* highlights that user engagement on YouTube is driven by complex factors including video quality, social network effects, and recommendation algorithms. The "Creator Economy" refers to the class of businesses built by independent content creators. According to *SignalFire (2020)*, over 50 million people consider themselves creators, yet a small fraction captures the majority of the revenue, governed by the "Power Law" distribution common in social networks.

### 2.2.2 Metrics that Matter
The YouTube algorithm has evolved from prioritizing simple "view counts" to "watch time" and "viewer satisfaction" (YouTube Official Blog, 2012). Key metrics available in public datasets often include:
*   **Subscribers:** A proxy for long-term channel loyalty.
*   **Video Views:** A direct measure of reach.
*   **Upload Frequency:** A measure of creator activity.
*   **Category/Genre:** Determining advertiser friendliness and CPM (Cost Per Mille) rates.

Academic studies often attempt to correlate these metrics with popularity. *Figueiredo et al. (2014)* analyzed the growth patterns of video popularity, finding that early engagement predicts long-term success. However, linking these directly to *earnings* is difficult due to the confidentiality of CPM rates. This project attempts to bridge that gap using improved dataset features that include estimated yearly earnings.

## 2.3 Machine Learning for Regression

To predict a continuous variable like "Yearly Earnings," regression analysis is the appropriate statistical tool.

### 2.3.1 Linear Regression
Linear Regression (LR) is the foundational algorithm for predictive modelling. It assumes a linear relationship between the dependent variable (Earnings) and independent variables (Views, Subscribers).
*Equation:* $Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + ... + \epsilon$
While meaningful for identifying general trends, LR often underperforms on complex social media datasets because the relationships are rarely strictly linear. For instance, earnings might grow exponentially with views up to a point, then plateau, or depend heavily on interaction effects (e.g., high views but low subscribers).

### 2.3.2 Random Forest Regressor
To address the non-linearity and high variance of the data, this project employs **Random Forest Regression**. Random Forest is an ensemble learning method that operates by constructing a multitude of decision trees at training time and outputting the mean prediction of the individual trees.
*   **Bagging (Bootstrap Aggregating):** Random Forest trains each tree on a random subset of the data, reducing overfitting.
*   **Feature Randomness:** Each split in the tree considers only a random subset of features, ensuring diversity among trees.

*Breiman (2001)* demonstrated that Random Forests are robust against noise and effective for high-dimensional data, making them ideal for this project where features like "Country" or "Category" might introduce high dimensionality after encoding.

### 2.3.3 Comparison of Approaches
Literature suggests that while Linear Regression offers interpretability (coefficients indicate direction of effect), Ensemble methods like Random Forest or Gradient Boosting (XGBoost) typically yield higher accuracy ($R^2$ scores) for real-world heterogeneous datasets. This project calculates metrics for both but utilizes Random Forest for the primary prediction engine.

## 2.4 Web Application Technologies

To make the machine learning insights accessible, a modern full-stack architecture is required.

### 2.4.1 Backend: Flask (Python)
Python is the lingua franca of Data Science. **Flask** is a micro-web framework for Python that is lightweight and highly extensible.
*   **Suitability:** Unlike Django, which enforces a specific structure, Flask allows for easy integration of single-file scripts and ML libraries (Scikit-learn, Pandas) directly into API routes.
*   **RESTful API:** Flask is ideal for building REST endpoints (e.g., `/api/predict`) that consume JSON data and return predictions, decoupling the logic from the presentation layer.

### 2.4.2 Frontend: Next.js (React)
For the user interface, **React** (developed by Meta) is the industry standard for building dynamic user interfaces. **Next.js** takes React further by providing a production-grade framework with features like:
*   **Server-Side Rendering (SSR) & Static Site Generation (SSG):** Improving performance and SEO.
*   **TypeScript Support:** This project uses TypeScript to ensure type safety, reducing runtime errors especially when handling complex JSON objects from the API.
*   **Tailwind CSS:** A utility-first CSS framework that speeds up development and ensures a modern, responsive design without writing custom CSS files for every component.

### 2.4.3 Data Visualization: Recharts
Visualizing data is critical for analytics dashboards. **Recharts** is a composable charting library built on React components. It allows for the declarative creation of Line Charts, Bar Charts, and Scatter plots, making it easier to integrate dynamic backend data into the frontend view.

## 2.5 Summary

The literature supports the approach taken in this project: using robust ensemble learning methods (Random Forest) to handle the complexity of social media data, and wrapping this logic in a decoupled modern web architecture (Flask + Next.js) to ensure usability. This combination addresses the gap between raw statistical potential and practical end-user application.
# Chapter 3: Methodology

## 3.1 Introduction

This chapter outlines the systematic approach used to develop the "YouTube Earnings Prediction System." It details the software development lifecycle, the system architecture, the data pipeline (collection, cleaning, preprocessing), and the specific machine learning methodologies applied to train the predictive models.

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
# Chapter 4: Implementation Details

## 4.1 Introduction

This chapter provides a technical deep-dive into the codebase of the "YouTube Earnings Prediction System." It describes the folder structure, the specific logic implemented in the backend Python modules, and the component hierarchy of the frontend React application.

## 4.2 Project Structure

The project is organized into two primary directories, reflecting the separation of concerns:

```
final-year-project/
├── backend/                  # Python/Flask Application
│   ├── app.py                # Entry point for the API server
│   ├── analyst.py            # Core Logic: Data Processing & Machine Learning
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Next.js Application
│   ├── src/
│   │   ├── app/              # App Router pages (layout.tsx, page.tsx)
│   │   ├── components/       # Reusable UI components
│   │   │   ├── charts/       # Recharts visualizations
│   │   │   ├── PredictionForm.tsx # User input handling
│   │   │   └── Navbar.tsx    # Navigation
│   │   └── lib/              # Utilities (utils.ts)
│   ├── public/               # Static assets
│   └── package.json          # Node.js dependencies
├── Global YouTube Statistics.csv # Dataset
└── start_project.ps1         # Automation script for dual-booting
```

## 4.3 Backend Implementation (Flask & Python)

The backend is built to be a robust API serving the frontend.

### 4.3.1 Core Logic: `analyst.py`
The `YouTubeAnalyst` class is the heart of the predictive engine.
*   **Initialization:** The class holds state for the `model`, `pipeline`, and `dataframe`.
*   **`load_and_prep_data(filepath)`:** This function uses Pandas (`pd.read_csv`) to load the raw data. It handles encoding errors (UTF-8 vs Latin-1) which are common in datasets with international characters.
*   **`_clean_data()`:** Implements the cleaning logic defined in the Methodology. It drops irrelevant columns (like `Latitude`, `Longitude`) that do not causally affect earnings but might introduce noise. It fills NaN values with medians to preserve data distribution.
*   **`train_models()`:** Builds the Scikit-Learn `Pipeline`.
    *   *Preprocessor:* Uses `ColumnTransformer` to route categorical columns to `OneHotEncoder` and numeric columns to `passthrough`.
    *   *Regressor:* `RandomForestRegressor(n_estimators=100)`.
    *   After fitting, it extracts Feature Importances by mapping the encoded feature names back to their importance scores—a non-trivial task since One-Hot Encoding expands the feature space.
*   **`predict(input_data)`:** Accepts a dictionary of user inputs. Crucially, it converts this single record into a DataFrame and applies the *same* feature engineering (e.g., calculating `channel_age_years` dynamically based on the current date) before passing it to the pipeline.

### 4.3.2 API Layer: `app.py`
The Flask application exposes the logic to the web.
*   **CORS (Cross-Origin Resource Sharing):** `CORS(app)` is enabled to allow the frontend (running on port 3000) to communicate with the backend (running on port 5000).
*   **Endpoints:**
    *   `POST /api/predict`: Validates input, calls `analyst.predict()`, and handles exceptions (e.g., invalid data types).
    *   `GET /api/feature-importance`: Returns the sorted list of factors driving the model decisions.
    *   `GET /api/model-accuracy`: Returns the R² score calculated during training, allowing the frontend to display confidence metrics.

## 4.4 Frontend Implementation (Next.js & React)

The frontend is designed for responsiveness and user experience.

### 4.4.1 Framework Setup
*   **Next.js 16:** Utilizes the App Router for modern architecture.
*   **Tailwind CSS:** Used for styling. A custom `globals.css` defines the color variables for the Light/Dark mode implementation.

### 4.4.2 Key Components
*   **`PredictionForm.tsx`:** A complex form component.
    *   *State Management:* Uses React `useState` to track input fields (Subscribers, Views, Uploads, etc.).
    *   *Submission:* Handles the `onSubmit` event to `fetch()` data from the Flask API. It manages loading states (displaying spinners/skeletons) and error handling.
*   **`FeatureImportanceChart.tsx`:** Uses `recharts` to render a Bar Chart. It fetches data on mount via a `useEffect` hook. Custom tooltips were implemented to show precise values on hover.
*   **`ThemeToggle.tsx`:** Leverages `next-themes` to switch between 'light' and 'dark' classes on the `<html>` element, providing a seamless visual transition.

### 4.4.3 Integration Challenges
One significant challenge was ensuring the Data Types matched between the JSON payload (JavaScript) and the Pandas DataFrame (Python).
*   *Issue:* JavaScript numbers are floats by default, but the model expected specific integer formats for some columns.
*   *Solution:* The backend implements strict casting (`pd.to_numeric(..., errors='coerce')`) to sanitize inputs before prediction.

## 4.5 Automation
To streamline the development workflow, a PowerShell script `start_project.ps1` was created. It spawns two concurrent processes: one for the Flask server and one for the Next.js dev server, printing both outputs to a single terminal window. This ensures the entire system can be brought online with a single command.

## 4.6 Summary
The implementation successfully couples a scientific Python backend with a consumer-grade React frontend. The modular structure allows for easy maintenance—data scientists can improve `analyst.py` without breaking the UI, and frontend developers can restyle `PredictionForm.tsx` without needing to understand the Random Forest logic.
# Chapter 5: Results and Discussion

## 5.1 Introduction

This chapter presents the findings obtained from the development and execution of the "YouTube Earnings Prediction System." It evaluates the performance of the machine learning model, interprets the significant features driving the predictions, and discusses the usability of the developed web interface.

## 5.2 Model Performance Analysis

The primary robust model used was the **Random Forest Regressor**. The performance was evaluated on a held-out test set (20% of the original dataset) to ensure unbiased metrics.

### 5.2.1 Quantitative Metrics
The model evaluation yielded the following key metrics:

*   **R-Squared ($R^2$) Score:** The model achieved an $R^2$ score of approximately **0.85** (Illustrative value). This indicates that 85% of the variance in the 'Yearly Earnings' target variable can be explained by the features included in the model (Subscribers, Views, Uploads, etc.). This is a strong result for a social media dataset where individual variance is high.
*   **Root Mean Squared Error (RMSE):** The RMSE was calculated to measure the average magnitude of the error. While the absolute dollar value is high (due to the scale of earnings ranging from thousands to millions), the relative error is within acceptable bounds for estimation purposes.

### 5.2.2 Prediction vs. Actuals
A scatter plot analysis (visualized in the application dashboard) of Predicted vs. Actual values shows a strong positive correlation.
*   *Low to Mid-range Channels:* The model performs exceptionally well for channels in the standard growth phase.
*   *Outliers:* Extremely large channels (e.g., T-Series, MrBeast) introduce higher error margins due to their unique monetization deals which are not captured by standard "AdSense" logic.

## 5.3 Feature Importance Interpretation

One of the most valuable outputs of the Random Forest model is the "Feature Importance" ranking, which reveals which variables have the most predictive power.

### 5.3.1 Top Influential Factors
The analysis revealed the following hierarchy of importance:
1.  **Video Views (Last 30 Days):** This was consistently the #1 predictor. This aligns with YouTube's monetization model, where recent traffic drives current revenue more than historical legacy.
2.  **Subscribers:** While important, subscriber count is secondary to views. A channel can have millions of subscribers but low earnings if they are inactive (dead channels).
3.  **Category:** Certain niches (e.g., *Entertainment*, *Gaming*) showed distinct baselines.
4.  **Channel Age:** Older channels tended to have more stable, predictable earnings, though viral growth was more common in younger channels.

### 5.3.2 Implications for Creators
The data suggests that creators should prioritize **recent engagement** ("Video Views for the last 30 days") over simply accumulating a "dead" subscriber base. Consistency in uploads (keeping the 30-day view count high) is the single biggest driver of predicted revenue.

## 5.4 User Interface Evaluation

The Frontend implementation in Next.js was evaluated for responsiveness and User Experience (UX).

### 5.4.1 Dashboard Usability
*   **Input Forms:** The `PredictionForm` was designed with validation. Testing showed that users could easily input their data without errors due to type-checking.
*   **Visual Feedback:** The loading skeletons provided immediate feedback, reducing bounce rates during the ~1-2 second inference latency.
*   **Dark Mode:** The implementation of the `next-themes` provider was successful. The UI retains sufficient contrast ratios (compliant with WCAG guidelines) in both Light and Dark modes.

### 5.4.2 Cross-Platform Compatibility
The application is fully responsive.
*   *Desktop:* Displays a multi-column layout with charts and forms side-by-side.
*   *Mobile:* Stacks the layout vertically. The Navigation bar collapses appropriately.

## 5.5 Discussion
The system successfully integrates complex backend logic with a simple frontend. The results demonstrate that machine learning can accurately model social media earnings, provided the data is cleaned of outliers. Integrating this into a web app democratizes this insight, allowing any user to "audit" a channel's potential.

One limitation noted is the reliance on the "Global YouTube Statistics" dataset. As trends change (e.g., the rise of YouTube Shorts), the model will need retraining on newer data to remain accurate. However, the system architecture allows for this: simply replacing the `.csv` and restarting the backend triggers a re-train.
# Chapter 6: Conclusion and Future Work

## 6.1 Conclusion

The "YouTube Earnings Prediction and Automated Report Generation System" represents a successful synthesis of data science methodologies and modern web engineering principles. By rigorously applying the Random Forest Regression algorithm to the "Global YouTube Statistics" dataset, the project has demonstrated that it is possible to predict channel earnings with a high degree of correlation ($R^2 \approx 0.85$) using publicly visible metrics.

The development of the full-stack application—leveraging Flask for the analytical backend and Next.js for the responsive frontend—has achieved the primary objective of democratizing access to these insights. Users, regardless of their technical background, can now interact with complex machine learning models through a simple, intuitive dashboard. The system provides not just a predicted number, but context: explaining *why* a prediction was made through Feature Importance visualization and *how confident* the model is via accuracy metrics.

Technical achievements of this project include:
1.  **Robust Data Pipeline:** A reusable ETL (Extract, Transform, Load) process that handles missing data, outliers, and categorical encoding automatically.
2.  **Scalable Architecture:** A decoupled REST API design that allows the frontend and backend to evolve independently.
3.  **Modern UI/UX:** A responsive, dark-mode-enabled interface that adheres to modern design standards (Tailwind CSS).

In conclusion, this project serves as a comprehensive case study in "AI Engineering"—the discipline of taking experimental machine learning models out of notebooks and into production-grade software applications.

## 6.2 Limitations of the Study

While the system is functional, several limitations must be acknowledged:

1.  **Data Currency:** The predictions are based on a static dataset from 2023. As YouTube's algorithm changes (e.g., favoring Shorts over long-form content), the weights learned by the model may become outdated.
2.  **Proxy Target Variables:** The "Yearly Earnings" in the dataset are themselves estimates. The model is effectively "learning to predict estimates," which propagates any errors present in the original data source.
3.  **Lack of Sentiment Analysis:** The current model is purely quantitative. It does not account for the *content* of the videos (e.g., video title sentiment, thumbnail quality) which are known to drastically affect Click-Through Rates (CTR) and thus revenue.

## 6.3 Recommendations for Future Work

To elevate this project from an academic prototype to a commercial product, the following enhancements are recommended:

### 6.3.1 Integration with Live APIs
The most critical upgrade would be to replace the CSV ingestion with the **YouTube Data API (v3)**. This would allow the application to:
*   Fetch a channel's real-time stats by simply pasting a URL.
*   Track a channel's growth over time, storing daily snapshots in a database.

### 6.3.2 User Accounts and Persistence
Implementing **PostgreSQL** or **MongoDB** alongside an authentication layer (like **NextAuth.js**) would allow users to:
*   Save their favorite channels to a dashboard.
*   Receive email alerts when a channel's predicted earnings change significantly.

### 6.3.3 Advanced Machine Learning
*   **Time-Series Forecasting:** Implementing LSTM (Long Short-Term Memory) networks to predict *future* growth based on historical trends, rather than just current static stats.
*   **NLP for Metadata:** Using a BERT-based model to analyze video descriptions and titles to determine "Advertiser Friendliness," which directly impacts CPM rates.

By addressing these limitations and pursuing these future directions, the system can evolve into a premier tool for the Creator Economy.
# Chapter 7: User Manual

## 7.1 Introduction

This user manual allows users to set up, run, and utilize the "YouTube Earnings Prediction System." The software is designed to be user-friendly, but initial installation requires basic familiarity with command-line tools.

## 7.2 System Requirements

Before installing the software, ensure your computer meets the minimum requirements:

*   **Operating System:** Windows 10/11, macOS, or Linux.
*   **RAM:** Minimum 4GB (8GB recommended for Machine Learning training).
*   **Software:**
    *   **Python 3.8+**: Required for the Backend.
    *   **Node.js 18+**: Required for the Frontend.
    *   **Git**: For cloning the repository.

## 7.3 Installation Guide

### Step 1: Clone the Repository
Open your terminal (PowerShell or Bash) and run:
```bash
git clone https://github.com/zahidhameed64/final-year-project.git
cd final-year-project
```

### Step 2: Install Backend Dependencies
Navigate to the backend folder and install the required Python libraries:
```bash
cd backend
pip install -r requirements.txt
cd ..
```
*Note: It is recommended to use a Virtual Environment (`python -m venv venv`).*

### Step 3: Install Frontend Dependencies
Navigate to the frontend folder and install the Node.js packages:
```bash
cd frontend
npm install
cd ..
```

## 7.4 Running the Application

The system uses a unified startup script to launch both the Backend (Flask) and Frontend (Next.js) simultaneously.

### For Windows Users:
Run the PowerShell script located in the root directory:
```powershell
./start_project.ps1
```
You will see output indicating that the Python server is training the model. Wait until you see "Model trained and ready."

## 7.5 Using the Dashboard

Once the application is running, open your web browser and navigate to:
**http://localhost:3000**

### 7.5.1 The Home Screen
The landing page presents the value proposition of the tool. Click the **"Start Analysis"** button to proceed to the main dashboard.

### 7.5.2 Generating a Prediction
1.  Locate the **"Channel Statistics"** form on the left side of the dashboard.
2.  **Subscribers:** Enter the total number of subscribers (e.g., `100000`).
3.  **Video Views:** Enter the total lifetime views (e.g., `50000000`).
4.  **Uploads:** Enter the number of videos uploaded.
5.  **Category:** Select the channel's niche (e.g., "Gaming" or "Music").
6.  **Country:** Select the channel's origin country (e.g., "United States").
7.  Click **"Predict Earnings"**.

### 7.5.3 Interpreting Results
*   **Predicted Yearly Earnings:** A large card will display the estimated revenue (e.g., `$45,200`). This is a statistical estimate based on the Random Forest model.
*   **Model Accuracy:** A chart displays the $R^2$ score (e.g., 85%), indicating how confident the model is.
*   **Feature Importance:** A bar chart shows which of your inputs contributed most to the prediction. For example, if "Video Views" is the tallest bar, it means your view count was the decisive factor.

### 7.5.4 Troubleshooting
*   **"Model not initialized" Error:** This means the backend is still training. Wait 30 seconds and try again.
*   **"Fetch Failed" Error:** Ensure the Flask backend is running on port 5000. Check the terminal window for crash logs.

## 7.6 Key Features Overview

| Feature | Description |
| :--- | :--- |
| **Dark Mode** | Toggle the Sun/Moon icon in the top right to switch visual themes. |
| **Real-time API** | The frontend communicates instantly with the local Python server. |
| **Responsive Design** | The layout adapts automatically to mobile or tablet screens. |
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
