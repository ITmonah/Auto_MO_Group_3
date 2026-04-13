from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
import joblib

data = load_wine()
X, y = data.data, data.target

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

joblib.dump(model, 'model.pkl')
print("Model saved to model.pkl")