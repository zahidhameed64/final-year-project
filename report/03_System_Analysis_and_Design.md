# Chapter 3: System Analysis and Design

## 3.1 Introduction

Before implementation, a thorough analysis and design phase was conducted to ensure the "Data-to-Narrative" system meets the needs of its users. This chapter outlines the software requirements, assesses the feasibility of the project, and details the architectural blueprints that guided the development.

## 3.2 Requirement Analysis

The system requirements are categorized into Functional Requirements (what the system does) and Non-Functional Requirements (how the system performs).

### 3.2.1 Functional Requirements (FR)

*   **FR-1 Data Ingestion:** The system shall accept user input for standard YouTube metrics, specifically:
    *   Channel Subscribers
    *   Video Views (Total & Last 30 Days)
    *   Upload count
    *   Channel Category (e.g., Music, Entertainment)
    *   Country of Origin
*   **FR-2 Prediction Engine:** The system shall use the trained Random Forest model to process inputs and return a numerical prediction for "Highest Yearly Earnings".
*   **FR-3 Visualization:** The system shall generate dynamic graphs (Bar charts, Scatter plots) to display Feature Importance and compare the user's input against dataset averages.
*   **FR-4 Data Validation:** The system must validate inputs (e.g., preventing negative view counts) before sending requests to the server.
*   **FR-5 Narrative Generation:** The system shall generate a text-based summary of the prediction, explaining the result in plain English.
*   **FR-6 Theme Management:** The system shall allow users to toggle between Light and Dark modes for accessibility.

### 3.2.2 Non-Functional Requirements (NFR)

*   **NFR-1 Performance:** The prediction API response time should be less than 200 milliseconds under normal load.
*   **NFR-2 Reliability:** The system should handle missing input fields gracefully by using default arithmetic means or prompting the user.
*   **NFR-3 Scalability:** The backend architecture should support concurrent requests without blocking, facilitated by Flask's WSGI capability.
*   **NFR-4 Usability:** The User Interface (UI) must be responsive, adapting layout for Desktop, Tablet, and Mobile screens.

## 3.3 Feasibility Study

A feasibility study determines if the project is viable given the constraints.

### 3.3.1 Technical Feasibility
*   **Technology Stack:** The chosen stack (Python/Flask + JavaScript/React) is industry standard, well-documented, and free to use.
*   **Computational Resources:** The Random Forest algorithm is computationally efficient. Training on 1,000 rows takes seconds, and inference is near-instantaneous, making it feasible to run on standard consumer hardware (e.g., the development laptop).
*   **Conclusion:** The project is technically highly feasible.

### 3.3.2 Economic Feasibility
*   **Cost:** All tools used (VS Code, Python, Node.js, Scikit-Learn) are Open Source (FOSS). The dataset was acquired for free from Kaggle.
*   **Development Cost:** The primary cost is developer time. No proprietary software licenses were required.
*   **Conclusion:** The project has zero monetary startup cost.

### 3.3.3 Operational Feasibility
*   **Maintenance:** The decoupled architecture allows for easy updates. If a better model is trained, the `.joblib` file can be replaced without touching the frontend code.
*   **Adoption:** The intuitive web interface ensures that users with no coding experience can utilize the tool, ensuring high operational usability.

## 3.4 System Architecture

The project follows a **Client-Server Architecture** (specifically, a Three-Tier Architecture).

### 3.4.1 High-Level Design Diagram
*   **Client Tier (Presentation):** The User's Browser running the React Application. It handles rendering, state management, and user interaction.
*   **Logic Tier (Application):** The Flask Server. It hosts the API endpoints (`/api/predict`, `/api/health`) and the Machine Learning Model pipeline.
*   **Data Tier (Persistence):**
    *   **Static Data:** The `Global YouTube Statistics.csv` file used for training.
    *   **Serialized Model:** The `model.joblib` file acting as the knowledge base.

### 3.4.2 Component Interaction
1.  **User** fills out the form on the **Next.js Frontend**.
2.  **Frontend** validates data and sends a `POST` request with a JSON payload to `localhost:5000/api/predict`.
3.  **Flask Backend** receives the request.
4.  **Analyst Module** (`analyst.py`) preprocesses the JSON data (One-Hot Encoding categories to match training schema).
5.  **Model** performs inference and returns the predicted float value.
6.  **Backend** constructs a JSON response containing the prediction and additional context (Feature Importances).
7.  **Frontend** receives the response and updates the Dashboard state, rendering the charts.

## 3.5 Data Modeling

Although a relational database was not used for the MVP, the data schema is structured as follows:

### 3.5.1 Input Schema (JSON)
```json
{
  "subscribers": "integer",
  "video_views": "integer",
  "uploads": "integer",
  "category": "string (enum)",
  "country": "string (enum)",
  "channel_type": "string"
}
```

### 3.5.2 Internal Data Structure (DataFrame)
During processing, the data is transformed into a Pandas DataFrame with 30+ columns after One-Hot Encoding:
*   `subscribers`, `video_views`, `uploads`, ...
*   `category_Music`, `category_Entertainment`, `category_Gaming` (Binary 0/1)
*   `Country_United States`, `Country_India`, etc. (Binary 0/1)

## 3.6 User Interface (UI) Design

The UI design philosophy centers on **"Minimalism"** and **"Data Density"**.

*   **Dashboard Layout:** A central control panel (Sidebar) for inputs, ensuring that changing parameters doesn't require scrolling away from the results (Main View).
*   **Color Scheme:**
    *   **Primary:** Deep Blue/Purple (signifying Intelligence/Tech).
    *   **Accents:** Emerald Green (for Revenue/Success metrics).
    *   **Dark Mode:** Dark Grey (`#1a1a1a`) background to reduce eye strain, suitable for prolonged usage by analysts.
*   **Feedback Mechanisms:** Loading spinners indicate processing states, and error toasts appear for invalid inputs.

## 3.7 Conclusion

The System Analysis phase confirmed that the proposed architecture is robust and the requirements are well-defined. The separation of concerns between the Frontend and Backend ensures a modular system that is easy to develop, test, and maintain.
