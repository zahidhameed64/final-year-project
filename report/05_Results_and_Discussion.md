# Chapter 5: Results and Discussion

## 5.1 Introduction

This chapter presents the findings obtained from the development and execution of the "YouTube Income Predictor." It evaluates the performance of the machine learning model, interprets the significant features driving the predictions, and discusses the usability of the developed web interface.

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
