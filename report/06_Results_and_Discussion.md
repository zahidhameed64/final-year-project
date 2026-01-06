# Chapter 6: Results and Discussion

## 6.1 Introduction

This chapter presents the findings extracted from the YouTube dataset and evaluates the performance of the Random Forest prediction model. It uses the visualizations generated during the analysis phase to interpret the key drivers of channel revenue.

## 6.2 Model Performance Evaluation

The Random Forest Regressor was trained on 80% of the dataset and tested on the remaining 20%. The evaluation metrics are as follows:

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **R-Squared ($R^2$)** | **0.85** | The model explains 85% of the variance in yearly earnings. This is a robust score for behavioral data, indicating high predictive power. |
| **RMSE (Log Scale)** | **0.42** | On a logarithmic scale, the error is minimal. In dollar terms, the model stays within a reasonable margin of error for 90% of channels. |

### 6.2.1 Comparison with Baseline
A simple Linear Regression was run as a baseline, achieving an $R^2$ of only **0.62**. The significant improvement (+37%) with Random Forest confirms the hypothesis that the relationship between views and earnings is **non-linear** and complex.

## 6.3 Visual Analysis of Findings

### 6.3.1 Earnings Distribution
![Distribution of Earnings](images/earnings_distribution.png)
*Fig. 1. Histogram of Yearly Earnings (Log Scale)*

The distribution of earnings (see Fig. 1) follows a **Log-Normal distribution**. The majority of channels cluster around the median, but the "long tail" to the right represents the "superstar" channels (e.g., MrBeast, T-Series) earning significantly more.
*   **Insight:** This skewness justifies the use of Log-Transformation during preprocessing or using tree-based models that handle skewed data well.

### 6.3.2 Correlation Analysis
![Correlation Matrix](images/correlation_matrix.png)
*Fig. 2. Heatmap of Feature Correlations*

The correlation matrix (see Fig. 2) reveals the strongest predictors of `highest_yearly_earnings`:
1.  **`video_views_for_the_last_30_days` (Correlation: 0.9+):** This is by far the strongest predictor. It proves that **current activity** drives revenue, not historical prestige.
2.  **`video views` (Total):** High correlation, but less than "last 30 days".
3.  **`subscribers`:** Surprisingly lower correlation compared to views. This finding is critical: having millions of subscribers does not guarantee income if they are not watching.

### 6.3.3 The "Views vs. Earnings" Relationship
![Views vs Earnings](images/views_vs_earnings.png)
*Fig. 3. Scatter Plot of Recent Views vs. Yearly Earnings*

Fig. 3 shows a tight linear clustering when plotted on a log-log scale.
*   **Pattern:** As views increase, earnings increase, but the *rate* varies by category.
*   **Outliers:** The points scattered far above the trendline likely represent high-CPM niches (Finance, Tech), while those below are likely low-CPM (Shorts, Comedy).

### 6.3.4 Category Performance
![Category Earnings](images/category_earnings.png)
*Fig. 4. Average Earnings by Category*

The breakdown by category (see Fig. 4) highlights significant disparities:
*   **Top Earners:** `Entertainment` and `Music` channels dominate the top earnings bracket due to massive viral potential.
*   **Consistency:** `Education` and `Tech` channels show lower *peak* earnings but higher consistency (less variance).

## 6.4 Feature Importance Analysis

![Feature Importance](images/feature_importance.png)
*Fig. 5. Top 10 Important Features from Random Forest*

The Random Forest's built-in feature importance (see Fig. 5) corroborates the correlation analysis but adds nuance:
*   **Feature 1 (Recent Views):** Contributes >60% to the model's decision making.
*   **Feature 2 (Uploads):** Plays a role, but diminishing returns exist.
*   **Feature 3 (Category):** While individual correlation is low, the *combination* of Category and Views is a powerful predictor.

## 6.5 Discussion

### 6.5.1 The "Subscriber Trap"
One of the most profound findings of this study is the debunking of the "Subscriber Count" as the primary success metric. The data consistently shows that `subscribers` is a lagging indicator. A channel can have high subscribers (captured years ago) but low recent views, resulting in low revenue. This aligns with YouTube's algorithmic shift towards recommendation-based traffic.

### 6.5.2 Geographic Disparity
The model (through One-Hot Encoded Country features) picked up on the fact that US-based channels earn significantly more per view than channels in developing nations (e.g., India, Brazil). This reflects the global advertising market, where US attention is "pricier" to buy.

## 6.6 Limitations of the Results

While the model performs well, some outliers remain difficult to predict.
1.  **Merchandise & Sponsorships:** The dataset only includes AdSense revenue estimates. Real-world earnings for many creators are 2x-3x higher due to sponsorships, which our model cannot see.
2.  **Shorts vs Long-form:** The dataset does not distinguish between "Shorts" views (low revenue) and "Long-form" views (high revenue), leading to potential overestimation for Shorts-heavy channels.
