import pandas as pd
import pickle
from sklearn.metrics import mean_absolute_error, r2_score
import sys

def main():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("Can't find model model.pkl")
        sys.exit(1)

    try:
        test = pd.read_csv('test_processed.csv')
    except FileNotFoundError:
        print("Can't find test_processed.csv")
        sys.exit(1)

    feature_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year']
    X_test = test[feature_columns]
    y_test = test['Global_Sales']

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MAE = {mae:.4f}")
    print(f"R^2 = {r2:.4f}")

if __name__ == '__main__':
    main()