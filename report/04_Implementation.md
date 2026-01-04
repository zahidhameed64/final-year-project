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
