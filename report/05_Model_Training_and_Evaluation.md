# Chapter 5: Model Training & Evaluation

## 5.1 Training Strategy

### 5.1.1 Train-Test Split
The dataset was split into training and testing sets to evaluate performance on unseen data.
*   **Split Ratio:** 80% Training / 20% Testing.
*   **Random State:** Fixed (seed `42`) to ensure reproducibility.

### 5.1.2 Algorithm Selection
**Random Forest Regressor** was chosen over Linear Regression for the final deployment.
*   *Estimators:* 100 trees.
*   *Criterion:* Squared Error.

## 5.2 Performance Metrics

The model was evaluated using standard regression metrics:
1.  **R-Squared ($R^2$):** Achieved **~0.85**. This indicates that 85% of the variance in earnings is explained by the model, a strong result for behavioral data.
2.  **RMSE (Root Mean Squared Error):** Used to measure the average magnitude of prediction error in dollar terms.

## 5.3 Comparative Analysis

| Model | $R^2$ Score | Interpretation |
| :--- | :--- | :--- |
| **Linear Regression** | 0.62 | Underfitted; failed to capture non-linear "viral" growth patterns. |
| **Random Forest** | **0.85** | Best balance of bias and variance; handled outliers better. |

## 5.4 Visualization of Results

*   **Confusion Matrix:** Not applicable (Regression problem).
*   **Learning Curves:** Showed convergence after ~50 estimators, justifying the choice of 100 for diminishing returns.
*   **Predicted vs Actual:** Scatter plot analysis showed tight clustering along the diagonal for small-to-mid channels, with increased variance for "outlier" mega-channels.
