# YouTube Income Predictor

## Overview
This project is a full-stack web application designed to predict the yearly earnings of YouTube channels based on their public statistics (Subscribers, Views, Uploads, etc.). It utilizes a **Machine Learning** backend to analyze historical trends and a modern **React** frontend to display real-time predictions and insights.

## Project Structure
*   **`backend/`**: A Flask (Python) API that handles data processing and runs the Random Forest regression model.
*   **`frontend/`**: A Next.js (React) application that provides the user interface.
*   **`report/`**: Contains the detailed project dissertation and documentation chapters.
*   **`Global YouTube Statistics.csv`**: The dataset used for training the model.

## Prerequisites
*   **Node.js** (v18 or higher)
*   **Python** (v3.8 or higher)
*   **Git**

## Quick Start (Automated)

The easiest way to run the project is using the included PowerShell script, which installs dependencies and launches both servers concurrently.

1.  Open PowerShell in the project root:
    ```powershell
    ./start_project.ps1
    ```
2.  The script will:
    *   Install Python requirements.
    *   Install Node.js packages.
    *   Start the Flask API on **port 5000**.
    *   Start the Next.js Frontend on **port 3000**.
3.  Open your browser to **http://localhost:3000**.

## Manual Setup

If you prefer to run components individually:

### Backend (Python)
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```
*   The server will start at `http://localhost:5000`.
*   *Note: On first run, it will take a moment to train the model.*

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
*   The application will start at `http://localhost:3000`.

## Features
*   **Real-time Predictions:** Estimate earnings for any hypothetical channel stats.
*   **Data Visualization:** Interactive charts showing prediction accuracy and feature importance.
*   **Dark Mode:** Fully responsive UI with theme support.
*   **Report Generation:** (See `report/` folder for the generated project documentation).

## Tech Stack
*   **Frontend:** Next.js 15, React 19, Tailwind CSS, Recharts, Lucide Icons.
*   **Backend:** Flask, Pandas, Scikit-learn (Random Forest Regressor).
*   **Tools:** PowerShell, Git.
