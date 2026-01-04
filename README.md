# YouTube Income Predictor

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**YouTube Income Predictor** is an advanced AI-powered application designed to estimate the yearly earnings of YouTube channels with high precision. By leveraging a **Random Forest Regression** model trained on a comprehensive global dataset, it analyzes key channel metrics—including subscribers, total views, and recent performance (last 30 days)—to provide realistic revenue forecasts.

## 🚀 Features

*   **💰 AI-Powered Prediction**: Uses a robust machine learning model to predict yearly earnings.
*   **📊 Key Metrics Analysis**: Takes into account critical factors like `Subscribers`, `Total Video Views`, `Uploads`, and `Views (Last 30 Days)`.
*   **🎯 Real-Time Accuracy**: Dynamically displays the model's current accuracy score (R²) alongside every prediction, building user trust.
*   **🔍 Feature Importance**: Visualizes which channel statistics contribute most to the predicted earnings.
*   **✨ Modern UI**: built with **Next.js** and **Tailwind CSS**, featuring a sleek dark mode, glassmorphism effects, and responsive design.

## 🛠️ Technology Stack

### Backend
*   **Framework**: Flask (Python)
*   **ML Library**: Scikit-learn (Random Forest Regressor)
*   **Data Processing**: Pandas, NumPy
*   **API**: RESTful endpoints with CORS support

### Frontend
*   **Framework**: Next.js (React)
*   **Styling**: Tailwind CSS, Lucide Icons
*   **Animation**: Framer Motion
*   **Visualization**: Recharts

## 📂 Project Structure

```bash
final-year-project/
├── backend/                # Flask Server & ML Logic
│   ├── analyst.py          # Machine Learning Class (Training & Prediction)
│   ├── app.py              # API Routes & Application Entry Point
│   ├── requirements.txt    # Python Dependencies
│   └── ...
├── frontend/               # Next.js Client Application
│   ├── src/components/     # UI Components (PredictionForm, Navbar, etc.)
│   ├── src/app/            # Pages & Layouts
│   └── ...
├── report/                 # Project Documentation & Thesis
├── start_project.ps1       # Automated Startup Script
└── README.md               # Project Documentation
```

## ⚡ Quick Start

### Option 1: Automated Script (Windows)
The easiest way to run the project. This script checks dependencies, installs them, and launches both servers.
```powershell
./start_project.ps1
```

### Option 2: Manual Setup

**1. Backend Setup**
Navigate to the backend folder and install Python dependencies.
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```
*Server will start at `http://localhost:5000`*

**2. Frontend Setup**
Open a new terminal, navigate to the frontend folder, and install Node modules.
```bash
cd frontend
npm install
npm run dev
```
*Client will start at `http://localhost:3000`*

## 🧠 Model Insights
The core of the system is the `YouTubeAnalyst` class in `backend/analyst.py`. It uses a **Random Forest Regressor** to handle non-linear relationships between channel stats and earnings.
*   **Input Features**: Subscribers, Video Views, Uploads, Created Year, Category, Country, and more.
*   **Crucial Feature**: `Video Views for the Last 30 Days` is heavily weighted to ensure predictions reflect current channel activity rather than just historical accumulation.

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).
