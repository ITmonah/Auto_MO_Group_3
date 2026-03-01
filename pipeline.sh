#!/bin/bash

set -e  

if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "can't create venv"
        exit 1
    fi
    echo "venv created"
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "can't Install requirements."
        deactivate
        exit 1
    fi
    echo "requirements installed."
else
    echo "can't find requirements"
fi


python split.py
if [ $? -ne 0 ]; then
    echo "split error"
    deactivate
    exit 1
fi
echo "split success"

python preprocess.py
if [ $? -ne 0 ]; then
    echo "preprocess error"
    deactivate
    exit 1
fi
echo "preprocess finished"

python train.py
if [ $? -ne 0 ]; then
    echo "train error"
    deactivate
    exit 1
fi

python test.py
if [ $? -ne 0 ]; then
    echo "test error"
    deactivate
    exit 1
fi

read -r answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    echo "Запуск интерактивного предсказания..."
    venv/bin/python predict.py
    if [ $? -ne 0 ]; then
        echo "Ошибка при выполнении predict.py."
        exit 1
    fi
else
    echo "Для запуска предсказаний вручную выполните: venv/bin/python predict.py"
fi

deactivate