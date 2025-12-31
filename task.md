# Task List

- [x] Create Flask backend structure
    - [x] Create `backend` directory
    - [x] Create `backend/requirements.txt`
    - [x] Create `backend/train_model.py` (Script to train and save model)
    - [x] Create `backend/app.py` (Flask API)
- [x] Integrate with Frontend
    - [x] Update `frontend/src/componets/PredictionForm.tsx` to call Flask API
    - [x] Test integration
- [x] Verification
    - [x] Run `backend/train_model.py` to generate `model.joblib`
    - [x] Run `backend/app.py` to start server
    - [x] Test frontend prediction functionality
- [/] Optimization
    - [ ] Upgrade to Gradient Boosting Regressor for better accuracy
    - [ ] Retrain and verify
