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
