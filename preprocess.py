import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import sys

def main():
    try:
        train = pd.read_csv('train.csv')
        test = pd.read_csv('test.csv')
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    numeric_features = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year']
    missing = [col for col in numeric_features if col not in train.columns]
    if missing:
        print(f"column is missing: {missing}")
        sys.exit(1)

    X_train = train[numeric_features]
    y_train = train['Global_Sales']
    X_test = test[numeric_features]
    y_test = test['Global_Sales']

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=numeric_features)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=numeric_features)

    train_processed = pd.concat([X_train_scaled_df, y_train.reset_index(drop=True)], axis=1)
    test_processed = pd.concat([X_test_scaled_df, y_test.reset_index(drop=True)], axis=1)

    train_processed.to_csv('train_processed.csv', index=False)
    test_processed.to_csv('test_processed.csv', index=False)

    print("preprocess success")

if __name__ == '__main__':
    main()