# Chapter 4: Methodology

## 4.1 Introduction

This chapter details the methodology employed to develop the prediction model. It follows the standard **KDD (Knowledge Discovery in Databases)** process: Data Collection, Preprocessing, Transformation, Data Mining (Modeling), and Evaluation. This systematic approach ensures that the model is built on clean, reliable data and that its results are scientifically valid and reproducible.

## 4.2 Research Design

The study adopts a **Quantitative Research Design**. We analyze numerical and categorical data from an existing dataset to find statistical relationships. The problem is defined as a **Supervised Regression Task**, where the goal is to predict a continuous target variable (`highest_yearly_earnings`) based on a set of input features. Unlike classification, which predicts a label, regression allows us to estimate specific monetary values, which is far more useful for financial planning.

## 4.3 Data Collection

### 4.3.1 Dataset Source
The primary data source for this study is the **"Global YouTube Statistics 2023"** dataset, curated by **Nidula Elgiriyewithana** and hosted on **Kaggle**. This comprehensive dataset provides a detailed snapshot of the digital landscape, aggregating public metrics for approximately 1,000 of the most subscribed YouTube channels globally. Unlike fragmented data scrapes, this curated collection offers standardized attributes including subscriber counts, video views, upload frequency, country of origin, and earnings estimates. It serves as a vital resource for analyzing the "Creator Economy," allowing researchers to dissect the factors that drive success—from content categories to regional influence—within the platform's elite tier.

### 4.3.2 Dataset Attributes
The dataset consists of 28 columns covering a wide range of attributes. **Identification** attributes like `Youtuber` and `Title` allow us to verify the data against the real platform. **Categorical** variables such as `category` and `Country` provide the context needed to segment the market; for example, distinguishing between Music and Entertainment channels. **Numerical Metrics** form the core of our analysis, including `subscribers`, `video views`, `uploads`, and `video_views_for_the_last_30_days`. Finally, **Temporal** attributes like `created_year` allow us to calculate the age of the channel, which is a critical factor in determining its maturity and stability.

## 4.4 Data Preprocessing

Raw data is rarely suitable for direct modeling. A robust preprocessing pipeline was implemented in Python using the `Pandas` and `Scikit-Learn` libraries to clean and prepare the data for the algorithm.

### 4.4.1 Data Cleaning
The first step was **Removing Irrelevant Features**. Attributes that do not causally affect earnings were dropped to reduce noise and the "Curse of Dimensionality." These included `Latitude`, `Longitude`, `Abbreviation`, `Gross tertiary education enrollment`, `Population`, `Unemployment rate`, and `Urban_population`. While these are interesting demographic statistics, they are properties of the *country*, not the *channel*. Including them would have introduced excessive dimensions that could confuse the model without adding predictive power.

Next, we handled **Zero Values**. Channels with `0` total views or `0` uploads were identified as data errors or inactive placeholder accounts and were removed from the dataset. Training a model on active, healthy channels ensures that our predictions are relevant to active creators. We also addressed **Outliers**. The target variable `highest_yearly_earnings` showed extreme right-skewness, adhering to a Power Law. While Random Forests are generally robust to outliers, extreme cases (e.g., T-Series) can dominate the loss function. However, we decided to **retain** most outliers as they represent the "Viral" nature of YouTube, which is a real phenomenon we want to capture.

### 4.4.2 Missing Value Imputation
Missing data can significantly impact or even crash Machine Learning models. We analyzed the sparsity of the data and found two major gaps. The `Country` column had approximately 12% missing values. These were imputed with the mode ("United States") or labeled as "Unknown" to allow the model to process them. The `video_views_for_the_last_30_days` column had about 5% missing data. We imputed these using the **Median** value of the column. Verification showed that Mean imputation was skewed by superstars, making Median the safer, more representative choice for the typical channel.

### 4.4.3 Feature Engineering
Feature Engineering involves creating new features from existing ones to better represent the underlying problem. We derived two key metrics. First, **`channel_age`** was calculated as `Current Year (2023) - created_year`. This captures the "legacy" advantage; older channels often have a built-in audience that new channels do not. Second, **`views_per_upload`** was calculated as `video views / uploads`. This serves as a proxy for "Quality vs Quantity," helping the model distinguish between channels that spam thousands of low-quality videos (low views per video) and those that release high-quality hits (high views per video).

### 4.4.4 Data Transformation (Encoding)
Machine Learning models require strictly numerical input. Therefore, we applied **This One-Hot Encoding** to categorical variables `category` and `Country`. This process converts a column like `Category` with values ["Music", "Gaming"] into two binary columns: `Category_Music` (1/0) and `Category_Gaming` (1/0). This avoids the problem of Label Encoding where the model might mathematically assume "Music" (value 2) is "greater than" "Gaming" (value 1), which is a logical fallacy.

## 4.5 Machine Learning Algorithm

### 4.5.1 Algorithm Selection
We compared three potential algorithms. **Linear Regression** assumes a linear relationship ($y = mx + c$) and was rejected due to high bias (Underfitting); it simply could not capture the complexity of viral growth. **Decision Tree Regressor** can capture non-linear patterns but is prone to overfitting (high variance), memorizing the training data. Consequently, **Random Forest Regressor** was selected as the final model because it balances these two extremes effectively.

### 4.5.2 Mathematical Foundation of Random Forest
Random Forest is an **Ensemble Learning** method that operates by constructing a multitude of decision trees at training time. The fundamental concept relies on two pillars. **Bagging (Bootstrap Aggregating)** involves the algorithm selecting random samples with replacement from the training set. This ensures diversity among trees, reducing the variance of the final model without increasing bias. **Feature Randomness** is the second pillar; unlike standard trees, which search for the best feature among *all* features to split a node, Random Forest searches for the best feature among a *random subset* of features. This forces the model to verify features it might otherwise ignore.

For regression tasks, the prediction is the average of the predictions of the individual trees:
$$ \hat{f} = \frac{1}{B} \sum_{b=1}^{B} f_b(x') $$
Where $B$ is the number of trees and $f_b$ is the prediction of the $b$-th tree. Because each tree sees a slightly different subset of data and features, the errors of individual trees (which might be high variance) tend to average out. This "wisdom of crowds" approach leads to a model that generalizes well to unseen data, making it highly effective for our purpose.

## 4.6 Model Training and Tuning

The model was implemented using the `sklearn.ensemble.RandomForestRegressor` library.

### 4.6.1 Hyperparameters
We tuned the model with specific hyperparameters. The `n_estimators` (Number of Trees) was set to **100**. Experiments showed that performance plateaued after 100 trees, making this a computationally efficient choice that balances accuracy with training speed. The `random_state` was set to **42** to ensure reproducibility of results; this ensures that our findings can be verified by others. The `max_depth` was left as **None**, meaning nodes are expanded until all leaves are pure. We rely on the ensemble nature of the forest to prevent the overfitting that would usually occur with a single deep tree.

### 4.6.2 Training Process
The training process involved splitting the dataset into a **Training set (80%)** and a **Testing set (20%)**. The `Pipeline` object was used to chain the Preprocessor and the Regressor. This is a best practice that ensures that any transformation applied to the training data (like scaling or imputation statistics) is identically applied to the testing data. This effectively prevents **Data Leakage**, ensuring that our test results are a true reflection of the model's real-world performance.

## 4.7 Evaluation Metrics

To quantitatively assess model performance, we utilized two standard metrics.

The first is the **Coefficient of Determination ($R^2$)**. This represents the proportion of variance in the dependent variable that is predictable from the independent variables. An $R^2$ of 1.0 indicates perfect prediction.
$$ R^2 = 1 - \frac{SS_{res}}{SS_{tot}} $$
Where $SS_{res}$ is the sum of squares of residuals and $SS_{tot}$ is the total sum of squares.

The second is the **Root Mean Squared Error (RMSE)**. This measures the standard deviation of the prediction errors (residuals). It tells us how far off our predictions are, on average, in the same units as the target variable ($).
$$ RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2} $$

These metrics provide a comprehensive view of both the *fit* (R2) and the *accuracy* (RMSE) of the model, allowing us to be confident in our results.
