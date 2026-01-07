import joblib
import sys
import os

# Add backend to path so we can import custom classes if needed
sys.path.append('backend')

try:
    from analyst import YouTubeAnalyst
    print("Successfully imported YouTubeAnalyst class")
except ImportError as e:
    print(f"Could not import YouTubeAnalyst: {e}")

try:
    path = "backend/model.joblib"
    print(f"Attempting to load model from {path}")
    if not os.path.exists(path):
        print("File does not exist!")
    else:
        model_data = joblib.load(path)
        print("Successfully loaded model object")
        print(f"Type: {type(model_data)}")
        if isinstance(model_data, dict):
             print(f"Keys: {model_data.keys()}")
        
except Exception as e:
    print(f"CRITICAL ERROR LOADING MODEL: {e}")
    import traceback
    traceback.print_exc()
