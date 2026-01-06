# Chapter 10: Appendices

## A. Code Snippets

### A.1 Model Training (Python)
```python
# Random Forest Initialization
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)
```

### A.2 Frontend Fetch (TypeScript)
```typescript
const response = await fetch("http://localhost:5000/api/predict", {
    method: "POST",
    body: JSON.stringify(formData)
});
```

## B. System Configuration

*   **Environment:** Node.js v18+, Python 3.9+
*   **Dependencies:** `scikit-learn`, `pandas`, `flask`, `next`, `react`, `tailwindcss`.
