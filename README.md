# YouTube Income Predictor

## Overview
YouTube Income Predictor is an intelligent application that uses machine learning to estimate the yearly earnings of YouTube channels. By analyzing public metrics such as subscribers, video views, and uploads, the system provides accurate revenue predictions to help creators understand their potential.

## Tech Stack
*   **Frontend**: Next.js, React, Tailwind CSS
*   **Backend**: Flask (Python), Scikit-learn
*   **Database**: CSV Dataset (Global YouTube Statistics)
*   **AI Model**: Random Forest Regressor

## Quick Start
1.  **Run the Setup Script**:
    ```powershell
    ./start_project.ps1
    ```
    This script will check your environment, install necessary Python/Node.js dependencies, and launch both the backend (port 5000) and frontend (port 3000).

2.  **Manual Start**:
    *   **Backend**: `cd backend` -> `python -m pip install -r requirements.txt` -> `python app.py`
    *   **Frontend**: `cd frontend` -> `npm install` -> `npm run dev`

## Features
*   **Income Prediction**: Estimate earnings based on channel stats.
*   **Feature Importance**: Understand which metrics drive revenue (e.g., Views, Uploads).
*   **Interactive Dashboard**: Modern, dark-mode UI for easy data entry.
