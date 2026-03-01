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

def parse_input(line):
    tokens = line.strip().split()
    if len(tokens) != 5:
        print("Ошибка: нужно ввести ровно 5 значений разделённых пробелами")
        return None
    values = []
    for i, token in enumerate(tokens):
        if token == '_':
            values.append(np.nan)
        else:
            try:
                values.append(float(token))
            except ValueError:
                print(f"Ошибка: '{token}' не является числом и не является символом пропуска '_'")
                return None
    return values

def predict_interactive(model, imputer, scaler):
    feature_names = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year']
    print("\nПредсказание глобальных продаж")
    print("Введите пять чисел через пробел в следующем порядке:")
    print("NA_Sales  EU_Sales  JP_Sales  Other_Sales  Year")
    print("Если какое-то значение неизвестно, поставьте символ '_'")
    print("Для выхода введите 'q'\n")
    
    while True:
        inp = input("Введите данные: ").strip()
        if inp.lower() == 'q':
            break
        if not inp:
            continue
        
        values = parse_input(inp)
        if values is None:
            continue 
        
        X = np.array([values])
        X_imputed = imputer.transform(X)
        X_scaled = scaler.transform(X_imputed)
        
        pred = model.predict(X_scaled)[0]
        
        print(f"Предсказанные глобальные продажи: {pred:.2f} млн копий\n")

def main():
    model, imputer, scaler = load_artifacts()
    predict_interactive(model, imputer, scaler)
    print("Работа завершена")

if __name__ == "__main__":
    main()