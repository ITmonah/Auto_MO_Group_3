import os
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "data/model.pkl"
os.makedirs("data", exist_ok=True)

if not os.path.exists(MODEL_PATH):
    data = load_wine()
    X, y = data.data, data.target
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
else:
    model = joblib.load(MODEL_PATH)

app = FastAPI(title="Wine Classifier API")

class WineFeatures(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float
    proline: float

@app.get("/")
def read_root():
    return {"message": "Wine classification model API"}

@app.post("/predict")
def predict(features: WineFeatures):
    data = np.array([[
        features.alcohol,
        features.malic_acid,
        features.ash,
        features.alcalinity_of_ash,
        features.magnesium,
        features.total_phenols,
        features.flavanoids,
        features.nonflavanoid_phenols,
        features.proanthocyanins,
        features.color_intensity,
        features.hue,
        features.od280_od315_of_diluted_wines,
        features.proline
    ]])
    prediction = model.predict(data)[0]
    proba = model.predict_proba(data)[0].tolist()
    class_names = ['class_0', 'class_1', 'class_2']
    return {
        "prediction": int(prediction),
        "class_name": class_names[prediction],
        "probabilities": proba
    }