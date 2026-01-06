import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (10, 6), 'figure.dpi': 100})

# Create images directory
output_dir = "report/images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load Data
try:
    df = pd.read_csv("Global YouTube Statistics.csv", encoding='latin1')
except:
    df = pd.read_csv("Global YouTube Statistics.csv", encoding='utf-8')

# Preprocessing (Basic, just for visualization)
df = df[df['video views'] > 0]
df = df.dropna(subset=['video_views_for_the_last_30_days', 'highest_yearly_earnings'])

# 1. Correlation Heatmap
plt.figure(figsize=(12, 10))
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
# Select only top correlated features to earnings
target = 'highest_yearly_earnings'
if target in corr.columns:
    cols = corr.nlargest(10, target)[target].index
    cm = np.corrcoef(df[cols].values.T)
    sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, 
                yticklabels=cols.values, xticklabels=cols.values, cmap='coolwarm')
    plt.title('Top 10 Features Correlated with Earnings')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_matrix.png")
    plt.close()

# 2. Distribution of Earnings (Log Scale)
plt.figure(figsize=(10, 6))
sns.histplot(df['highest_yearly_earnings'], bins=50, kde=True, color='green')
plt.xscale('log')
plt.title('Distribution of Yearly Earnings (Log Scale)')
plt.xlabel('Yearly Earnings ($)')
plt.ylabel('Frequency')
plt.savefig(f"{output_dir}/earnings_distribution.png")
plt.close()

# 3. Views vs Earnings Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(x='video_views_for_the_last_30_days', y='highest_yearly_earnings', data=df, alpha=0.6, hue='category', legend=False)
plt.xscale('log')
plt.yscale('log')
plt.title('Recent Views vs Highest Yearly Earnings')
plt.xlabel('Views (Last 30 Days)')
plt.ylabel('Earnings ($)')
plt.savefig(f"{output_dir}/views_vs_earnings.png")
plt.close()

# 4. Category Performance (Bar Chart)
plt.figure(figsize=(14, 8))
avg_earnings = df.groupby('category')['highest_yearly_earnings'].mean().sort_values(ascending=False)
sns.barplot(x=avg_earnings.values, y=avg_earnings.index, palette='viridis')
plt.title('Average Yearly Earnings by Category')
plt.xlabel('Average Earnings ($)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig(f"{output_dir}/category_earnings.png")
plt.close()

# 5. Feature Importance (if model exists)
if os.path.exists("backend/model.joblib"):
    try:
        model_data = joblib.load("backend/model.joblib")
        # Handle different save formats
        if isinstance(model_data, dict) and 'model' in model_data:
             model = model_data['model']
             # Try to get feature names
             feature_names = model_data.get('feature_names', [f'Feature {i}' for i in range(len(model.feature_importances_))])
        else:
            model = model_data
            feature_names = [f'Feature {i}' for i in range(len(model.feature_importances_))]
            
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Take top 10
        top_n = 10
        plt.figure(figsize=(12, 6))
        plt.title("Feature Importances")
        plt.bar(range(top_n), importances[indices][:top_n], align="center")
        # If we can match names, great, otherwise generic
        plt.xticks(range(top_n), [feature_names[i] for i in indices[:top_n]], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/feature_importance.png")
        plt.close()
    except Exception as e:
        print(f"Could not generate feature importance: {e}")

print("Images generated successfully.")
