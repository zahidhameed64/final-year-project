# Chapter 3: Data Description

## 3.1 Dataset Profile

The project utilizes the **"Global YouTube Statistics"** dataset, a comprehensive collection of performance metrics for top YouTube channels worldwide.

*   **Source:** Publicly available Kaggle dataset.
*   **Size:** Approximately 1,000 records of top-performing channels.
*   **Format:** CSV (Comma Separated Values).

## 3.2 Key Attributes

The dataset contains a mix of numerical and categorical features:
*   **Identity:** `Youtuber` (Channel Name), `category`, `Country`.
*   **Performance:** `subscribers`, `video analysis` (Total Views), `uploads`, `video_views_for_the_last_30_days`.
*   **Financial:** `highest_yearly_earnings`, `lowest_yearly_earnings`.
*   **Temporal:** `created_year`.

## 3.3 Exploratory Data Analysis (EDA)

Initial analysis revealed several key patterns:
1.  **Skewed Distribution:** The data follows a heavy-tailed distribution. A few "superstar" channels (like T-Series or MrBeast) have outlier metrics that are orders of magnitude higher than the median.
2.  **Missing Values:** Significant missing data was found in the `Country` and specific monthly stat columns, requiring imputation.
3.  **Correlation:** A correlation matrix heatmap showed a strong positive correlation ($r > 0.8$) between `video_views` and `earnings`, but a weaker correlation for `subscribers`, confirming the hypothesis that "active views" matter more than "legacy subs."

## 3.4 Data Preprocessing Pipeline

To prepare the data for the Random Forest model, the following steps were implemented in `analyst.py`:

1.  **Cleaning:**
    *   *Removal:* Irrelevant columns (`Latitude`, `Longitude`, `Abbreviation`) were dropped.
    *   *Filtering:* Channels with `0` views or `created_year` < 2005 (invalid dates) were removed.
2.  **Imputation:**
    *   *Numerical:* Missing values filled with the **Median** to avoid skewing by outliers.
    *   *Categorical:* Missing string values filled with "Unknown".
3.  **Feature Engineering:**
    *   `average_yearly_earnings`: Calculated as the mean of highest and lowest estimates to create a single target variable.
    *   `channel_age_years`: Derived from `created_year`.
    *   `views_per_upload`: A derived efficiency metric.
4.  **Encoding:**
    *   Categorical variables (`category`, `Country`, `channel_type`) were processed using **One-Hot Encoding** to convert them into a machine-readable binary format.
