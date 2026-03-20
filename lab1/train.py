import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import sys

def main():
    try:
        train = pd.read_csv('train_processed.csv')
    except FileNotFoundError:
        print("Can't find train_processed.csv")
        sys.exit(1)

    feature_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year']
    X_train = train[feature_columns]
    y_train = train['Global_Sales']

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    r2_train = r2_score(y_train, y_pred_train)
    print(f"Metrics: MAE = {mae_train:.4f}, R2 = {r2_train:.4f}")

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("model saved in model.pkl")

if __name__ == '__main__':
    main()