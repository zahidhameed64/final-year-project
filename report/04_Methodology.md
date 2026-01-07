# Chapter 4: Methodology

## 4.1 Introduction

This chapter details the methodology employed to develop the prediction model. It follows the standard **KDD (Knowledge Discovery in Databases)** process: Data Collection, Preprocessing, Transformation, Data Mining (Modeling), and Evaluation. This systematic approach ensures that the model is built on clean, reliable data and that its results are scientifically valid and reproducible.

## 4.2 Research Design

The study adopts a **Quantitative Research Design**. We analyze numerical and categorical data from an existing dataset to find statistical relationships. The problem is defined as a **Supervised Regression Task**, where the goal is to predict a continuous target variable (`highest_yearly_earnings`) based on a set of input features. Unlike classification, which predicts a label, regression allows us to estimate specific monetary values, which is far more useful for financial planning.

## 4.3 Data Collection

### 4.3.1 Dataset Source
The primary data source is the **"Global YouTube Statistics"** dataset, obtained from Kaggle. This dataset aggregates public metrics for approximately 1,000 of the most subscribed YouTube channels as of 2023. It provides a snapshot of the elite tier of the Creator Economy, allowing us to model the characteristics of highly successful channels.

### 4.3.2 Dataset Attributes
The dataset consists of 28 columns, categorized as follows:
*   **Identification:** `Youtuber`, `Title`, `Rank`.
*   **Categorical:** `category` (e.g., Music, Entertainment), `Country`, `channel_type`, `Abbreviation`.
*   **Numerical (Metrics):** `subscribers`, `video views`, `uploads`, `video_views_for_the_last_30_days`, `lowest_monthly_earnings`, `highest_monthly_earnings`, etc.
*   **Temporal:** `created_year`, `created_month`, `created_date`.
*   **Geospatial:** `Latitude`, `Longitude` (Not used).

## 4.4 Data Preprocessing

Raw data is rarely suitable for direct modeling. A robust preprocessing pipeline was implemented in Python using the `Pandas` and `Scikit-Learn` libraries.

### 4.4.1 Data Cleaning
1.  **Removing Irrelevant Features:** Attributes that do not causally affect earnings were dropped to reduce noise. These included `Latitude`, `Longitude`, `Abbreviation`, `Gross tertiary education enrollment`, `Population`, `Unemployment rate`, `Urban_population`. While these are interesting demographic stats, they are properties of the *country*, not the *channel*, and introduced excessive dimensions.
2.  **Handling Zero Values:** Channels with `0` total views or `0` uploads (data errors) were removed from the dataset.
3.  **Outlier Removal:** The target variable `highest_yearly_earnings` showed extreme right-skewness (Power Law). While Random Forests are robust to outliers, extreme cases (e.g., T-Series) can dominate the loss function. However, we decided to **retain** most outliers as they represent the "Viral" nature of YouTube, which is a real phenomenon we want to capture.

### 4.4.2 Missing Value Imputation
Missing data can crash ML models. We analyzed the sparsity of the data:
*   `Country`: ~12% missing. Imputed with the mode ("United States") or labeled as "Unknown".
*   `video_views_for_the_last_30_days`: ~5% missing. Imputed using the **Median** value of the column. Verification showed that Mean imputation was skewed by superstars, making Median the safer choice.

### 4.4.3 Feature Engineering
New features were derived to better represent channel performance:
1.  **`channel_age`**: Calculated as `Current Year (2023) - created_year`. Older channels have a "legacy" advantage.
2.  **`views_per_upload`**: Calculated as `video views / uploads`. This proxy for "Quality vs Quantity" helps distinguish between channels that spam videos (low views per video) and those that release high-quality hits.

### 4.4.4 Data Transformation (Encoding)
Machine Learning models require numerical input.
*   **One-Hot Encoding:** Applied to `category` and `Country`. This converts a column like `Category` with values ["Music", "Gaming"] into two binary columns: `Category_Music` (1/0) and `Category_Gaming` (1/0). This avoids the problem of Label Encoding where the model might assume "Music" (value 2) is "greater than" "Gaming" (value 1).

## 4.5 Machine Learning Algorithm

### 4.5.1 Algorithm Selection
We compared three potential algorithms:
1.  **Linear Regression:** Assumes a linear relationship ($y = mx + c$). Rejected due to high bias (Underfitting).
2.  **Decision Tree Regressor:** Can capture non-linear patterns but is prone to overfitting (high variance).
3.  **Random Forest Regressor:** Selected as the final model.

### 4.5.2 Mathematical Foundation of Random Forest
Random Forest is an **Ensemble Learning** method that operates by constructing a multitude of decision trees at training time.

*   **Bagging (Bootstrap Aggregating):** Given a training set $X = x_1, ..., x_n$ with responses $Y = y_1, ..., y_n$, the algorithm repeatedly selects a random sample with replacement of the training set and fits trees to these samples.
*   **Prediction:** For regression tasks, the prediction is the average of the predictions of the individual trees:
    $$ \hat{f} = \frac{1}{B} \sum_{b=1}^{B} f_b(x') $$
    Where $B$ is the number of trees and $f_b$ is the prediction of the $b$-th tree.

Because each tree sees a slightly different subset of data and features, the errors of individual trees (which might be high variance) tend to average out, leading to a model that generalizes well.

## 4.6 Model Training and Tuning

The model was implemented using `sklearn.ensemble.RandomForestRegressor`.

### 4.6.1 Hyperparameters
*   `n_estimators` (Number of Trees): Set to **100**. Experiments showed that performance plateaued after 100 trees, making this a computationally efficient choice.
*   `random_state`: Set to **42** to ensure reproducibility of results.
*   `max_depth`: Left as **None** (nodes are expanded until all leaves are pure). We rely on the ensemble nature to prevent overfitting.

### 4.6.2 Training Process
1.  The dataset was split into **Training (80%)** and **Testing (20%)** sets.
2.  The `Pipeline` object was used to chain the Preprocessor and the Regressor. This ensures that any transformation applied to the training data is identically applied to the testing data, preventing **Data Leakage**.

## 4.7 Evaluation Metrics

To quantitatively assess model performance, we utilized:.

1.  **Coefficient of Determination ($R^2$):** Represents the proportion of variance in the dependent variable that is predictable from the independent variables. An $R^2$ of 1.0 indicates perfect prediction.
    $$ R^2 = 1 - \frac{SS_{res}}{SS_{tot}} $$
    Where $SS_{res}$ is the sum of squares of residuals and $SS_{tot}$ is the total sum of squares.

2.  **Root Mean Squared Error (RMSE):** The standard deviation of the prediction errors (residuals). It tells us how far off our predictions are, on average, in the same units as the target variable ($).
    $$ RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2} $$

These metrics provide a comprehensive view of both the *fit* (R2) and the *accuracy* (RMSE) of the model.
