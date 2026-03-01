#!/usr/bin/env python3
import pickle
import numpy as np
import sys

def load_artifacts():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("Ошибка: модель model.pkl не найдена")
        sys.exit(1)
    try:
        with open('imputer.pkl', 'rb') as f:
            imputer = pickle.load(f)
    except FileNotFoundError:
        print("Ошибка: imputer.pkl не найден")
        sys.exit(1)
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
    except FileNotFoundError:
        print("Ошибка: scaler.pkl не найден")
        sys.exit(1)
    return model, imputer, scaler

def predict_interactive(model, imputer, scaler):
    feature_names = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year']

    while True:
        values = []
        for feat in feature_names:
            while True:
                inp = input(f"{feat}: ").strip()
                if inp == "":
                    values.append(np.nan)
                    break
                try:
                    val = float(inp)
                    values.append(val)
                    break
                except ValueError:
                    print("Ошибка: введите число или оставьте пустым")

        X = np.array([values])
        X_imputed = imputer.transform(X)
        X_scaled = scaler.transform(X_imputed)
        
        pred = model.predict(X_scaled)[0]
        
        print(f"\nПредсказанные глобальные продажи: {pred:.2f} копий\n")
        cont = input("Хотите сделать еще одно предсказание? (y/n): ").strip().lower()
        if cont != 'y':
            break

def main():
    model, imputer, scaler = load_artifacts()
    predict_interactive(model, imputer, scaler)
    print("Работа завершена")

if __name__ == "__main__":
    main()