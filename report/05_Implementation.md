# Chapter 5: Implementation

## 5.1 Development Environment

The project was developed in a robust local environment designed to ensure stability and performance. We utilized **Windows 10/11** as the primary Operating System. The core coding was done in **Visual Studio Code (VS Code)**, enriched with extensions for Python, Prettier, and ESLint to maintain code quality. **Git** was employed for source code management, allowing us to track changes and revert to previous states if necessary. For dependency management, we used `pip` for Python libraries and `npm` for JavaScript packages, ensuring that all libraries were kept up to date and compatible.

## 5.2 Backend Implementation


### 5.2.1 Directory Structure
The backend is organized as a micro-application:
```text
backend/
├── app.py              # Main entry point (Flask Server)
├── analyst.py          # ML Logic (YouTubeAnalyst class)
├── requirements.txt    # Dependency list
└── model.joblib        # Serialized Random Forest Model
```

### 5.2.2 The Analyst Module (`analyst.py`)
This is the core class responsible for handling data.
*   **Initialization:** Loads the CSV dataset and trains the model if `model.joblib` is missing.
*   **Encapsulation:** All logic is wrapped in the `YouTubeAnalyst` class, following Object-Oriented Programming (OOP) principles.
*   **Pipeline:** It defines current Scikit-Learn pipelines for preprocessing (Imputation -> Scaling -> Encoding).

### 5.2.3 API Design (`app.py`)
The Flask application exposes RESTful endpoints:
*   `GET /api/health`: A heartbeat endpoint to check if the server is running.
*   `POST /api/predict`: The primary endpoint.
    *   **Input:** JSON object (subscribers, views, etc.).
    *   **Process:** Calls `analyst.predict_earnings()`.
    *   **Output:** JSON object with `predicted_earnings` (float) and `feature_importance` (dictionary).

**Code Snippet: Prediction Endpoint**
```python
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        # Convert raw JSON to DataFrame semantics
        prediction, factors = analyst.predict(data)
        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'factors': factors
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 5.3 Frontend Implementation

The frontend serves as the "Face" of the application, ensuring a seamless user experience.

### 5.3.1 Tech Stack Selection
*   **Next.js (React):** Chosen for its component-based architecture and fast rendering.
*   **Tailwind CSS:** A utility-first CSS framework that allowed for rapid, responsive styling without writing thousands of lines of custom CSS.

### 5.3.2 Component Architecture
The UI is broken down into reusable components:
*   `PredictionForm.tsx`: Contains the input fields (controlled components) and validation logic.
*   `Dashboard.tsx`: The main container that manages state (loading, error, result) and passes data to children.
*   `FeatureImportanceChart.tsx`: A visualization component using `Recharts` to display the bar chart of influential metrics.

### 5.3.3 State Management
React's `useState` hook is used to manage local state.
*   `formData`: Stores the user's current input.
*   `predictionResult`: Stores the response from the Flask API.
*   `isLoading`: Boolean flag to toggle loading spinners, enhancing UI responsiveness.

## 5.4 Integration

The integration between Frontend and Backend is achieved via HTTP/JSON.
1.  **CORS (Cross-Origin Resource Sharing):** `Flask-CORS` was installed on the backend to allow requests from `localhost:3000` (Frontend) to `localhost:5000` (Backend). Without this, the browser would block the API calls for security reasons.
2.  **Proxying:** The Frontend uses JavaScript's `fetch` API to talk to the backend asynchronous endpoints.

## 5.5 Challenges & Solutions during Implementation

### 5.5.1 Challenge: Data Shape Mismatch
*   **Issue:** The user inputs only 5-6 fields, but the model expects the original 28 columns (including `0` for all non-selected countries).
*   **Solution:** A helper function `prepare_input_vector` was written in `analyst.py`. It creates a template DataFrame with all zeros (matching the training schema) and fills in *only* the user's values, ensuring the model receives the correct input shape.

### 5.5.2 Challenge: Categorical Encoding
*   **Issue:** The model deals with "One-Hot" columns (e.g., `Category_Music`). The user selects "Music" from a dropdown.
*   **Solution:** The backend logic dynamically maps the string "Music" to set the column `Category_Music` to `1`, leaving `Category_Gaming`, etc., as `0`.

## 5.6 Deployment Strategy for Testing
A unified startup script (`run.bat`) was created to automate:
1.  Checking Python/Node installation.
2.  Installing dependencies (`pip install`, `npm install`).
3.  Launching both servers concurrently.
This ensured that the application could be reliably started on any Windows machine with a single click.
