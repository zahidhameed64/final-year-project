# Chapter 8: Appendices

## Appendix A: Source Code Listings

### A.1 Backend Logic (`analyst.py`)

```python
class YouTubeAnalyst:
    def __init__(self, data_path="Global YouTube Statistics.csv"):
        self.data_path = data_path
        self.model = None
        self.preprocessor = None
        self.load_data()
        
    def load_data(self):
        # Data Loading and Cleaning Pipeline
        df = pd.read_csv(self.data_path, encoding='latin1')
        df = df[df['video views'] > 0]  # Remove bad data
        
        # Feature Engineering
        df['channel_age'] = 2023 - df['created_year']
        
        # Pipeline Definition
        numeric_features = ['subscribers', 'video views', 'uploads']
        categorical_features = ['category', 'Country']
        
        self.preprocessor = ColumnTransformer([
            ('num', SimpleImputer(strategy='median'), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
```

### A.2 Frontend Component (`PredictionForm.tsx`)

```tsx
export default function PredictionForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState(initialState);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input 
        label="Subscribers" 
        value={formData.subscribers} 
        onChange={handleChange} 
      />
      <Button type="submit" disabled={isLoading}>
        {isLoading ? 'Calculating...' : 'Predict Earnings'}
      </Button>
    </form>
  );
}
```

## Appendix B: User Guide

### B.1 Getting Started
1.  Open the application URL (e.g., `http://localhost:3000`).
2.  You will be greeted by the **Dashboard Home**.

### B.2 Making a Prediction
1.  Locate the **"Channel Metrics"** form on the left sidebar.
2.  **Subscribers:** Enter the total subscriber count (e.g., 1000000).
3.  **Video Views (Last 30 Days):** Enter the monthly traffic. *Tip: This is the most important field.*
4.  **Category:** Select the channel niche from the dropdown.
5.  Click **"Generate Report"**.

### B.3 Interpreting Results
*   **Predicted Earnings:** The card displays the estimated yearly revenue range.
*   **Feature Importance Chart:** Hover over the bars to see which of your inputs positively or negatively affected the score.

## Appendix C: Installation Guide

To run the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Start-Project/DataNarrator.git
    cd DataNarrator
    ```
2.  **Run the Setup Script:**
    *   **Windows:** Double-click `run.bat` or run `.\start_project.ps1` in PowerShell.
    *   **Mac/Linux:** Run `python backend/app.py` and `npm run dev` in separate terminals.
3.  **Access:** Open browser to `http://localhost:3000`.

---

# Chapter 9: References

1.  **Breiman, L.** (2001). Random Forests. *Machine Learning*, 45(1), 5-32.
2.  **Cheng, X., Dale, C., & Liu, J.** (2008). Statistics and Social Network of YouTube Videos. *2008 16th International Workshop on Quality of Service*.
3.  **Figueiredo, F., Benevenuto, F., & Almeida, J. M.** (2014). The Tube over time: characterizing popularity growth of YouTube videos. *Proceedings of the 4th ACM international conference on Web search and data mining*.
4.  **Goldhaber, M. H.** (1997). The attention economy and the net. *First Monday*, 2(4).
5.  **Grinberg, M.** (2018). *Flask Web Development: Developing Web Applications with Python*. "O'Reilly Media, Inc."
6.  **Hou, M.** (2018). Social media celebrity and the institutionalization of YouTube. *Convergence*.
7.  **Pedregosa, F., et al.** (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
8.  **Richardson, C.** (2018). *Microservices patterns: with examples in Java*. Manning Publications.
9.  **Wooldridge, J. M.** (2012). *Introductory econometrics: A modern approach*. Cengage Learning.
