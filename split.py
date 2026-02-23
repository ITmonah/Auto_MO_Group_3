import pandas as pd
from sklearn.model_selection import train_test_split
import sys

def main():
    try:
        df = pd.read_csv('vgsales.csv')
    except FileNotFoundError:
        print("vgsales.csv is missing.")
        sys.exit(1)

    X = df.drop('Global_Sales', axis=1)
    y = df['Global_Sales']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    train_df.to_csv('train.csv', index=False)
    test_df.to_csv('test.csv', index=False)

    print(f"split success")

if __name__ == '__main__':
    main()