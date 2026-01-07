import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib
import sys

# Add backend to path
sys.path.append(os.path.abspath("backend"))
from analyst import YouTubeAnalyst

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (10, 6), 'figure.dpi': 100})

# Create images directory
output_dir = "report/images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load Data directly using analyst class to ensure consistency
print("Initializing Analyst...")
analyst = YouTubeAnalyst()
analyst.load_and_prep_data("Global YouTube Statistics.csv")

print("Training Model to get Feature Importances...")
analyst.train_models() 
# This populates analyst.model and analyst.feature_names

# Save model while we are at it to fix the broken file
joblib.dump(analyst.model, "backend/model.joblib")

df = analyst.df

# 1. Correlation Heatmap
print("Generating Correlation Matrix...")
plt.figure(figsize=(12, 10))
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
target = 'highest_yearly_earnings'
# Fallback target if not in df (analyst logic might not expose it?)
if target not in df.columns:
    target = 'video views' # Proxy

if target in corr.columns:
    cols = corr.nlargest(10, target)[target].index
    cm = np.corrcoef(df[cols].values.T)
    sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, 
                yticklabels=cols.values, xticklabels=cols.values, cmap='coolwarm')
    plt.title('Top 10 Features Correlated with Earnings')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_matrix.png")
    plt.close()

# 2. Earnings Distribution
print("Generating Earnings Distribution...")
plt.figure(figsize=(10, 6))
# Analyst might have filtered or not, let's use what we have
if 'highest_yearly_earnings' in df.columns:
    sns.histplot(df['highest_yearly_earnings'], bins=50, kde=True, color='green')
    plt.xscale('log')
    plt.title('Distribution of Yearly Earnings (Log Scale)')
    plt.xlabel('Yearly Earnings ($)')
    plt.ylabel('Frequency')
    plt.savefig(f"{output_dir}/earnings_distribution.png")
    plt.close()

# 3. Views vs Earnings
print("Generating Views vs Earnings...")
plt.figure(figsize=(10, 6))
if 'video_views_for_the_last_30_days' in df.columns and 'highest_yearly_earnings' in df.columns:
    sns.scatterplot(x='video_views_for_the_last_30_days', y='highest_yearly_earnings', data=df, alpha=0.6)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Recent Views vs Highest Yearly Earnings')
    plt.xlabel('Views (Last 30 Days)')
    plt.ylabel('Earnings ($)')
    plt.savefig(f"{output_dir}/views_vs_earnings.png")
    plt.close()

# 4. Category Performance
print("Generating Category Performance...")
plt.figure(figsize=(14, 8))
if 'highest_yearly_earnings' in df.columns:
    avg_earnings = df.groupby('category')['highest_yearly_earnings'].mean().sort_values(ascending=False)
    sns.barplot(x=avg_earnings.values, y=avg_earnings.index, palette='viridis')
    plt.title('Average Yearly Earnings by Category')
    plt.xlabel('Average Earnings ($)')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_earnings.png")
    plt.close()

# 5. Feature Importance
print("Generating Feature Importance...")
try:
    importances = analyst.get_feature_importances()
    # importances is list of dicts [{'name':.., 'importance':..}]
    
    if importances:
        names = [x['name'] for x in importances]
        values = [x['importance'] for x in importances]
        
        plt.figure(figsize=(12, 6))
        plt.title("Feature Importances (Random Forest)")
        plt.bar(range(len(values)), values, align="center")
        plt.xticks(range(len(values)), names, rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/feature_importance.png")
        plt.close()
        print("Feature importance generated.")
    else:
        print("No feature importances returned.")

except Exception as e:
    print(f"Error plotting feature importance: {e}")

print("All plots generated.")
