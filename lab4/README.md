# lab4

Практика по `git` и `dvc` для версионирования датасета Titanic.

## Структура

- `lab4/scripts/manage_dataset.py` - генерация и модификация датасета.
- `lab4/data/titanic.csv` - версия датасета, отслеживаемая через DVC.
- `lab4/requirements.txt` - зависимости для отдельного окружения.

## Команды

```powershell
python -m pip install --user -r lab4\requirements.txt
python -m dvc init
python lab4\scripts\manage_dataset.py create-base
python -m dvc add lab4\data\titanic.csv
git add .gitignore .dvc .dvcignore lab4\data\titanic.csv.dvc lab4\scripts\manage_dataset.py lab4\README.md lab4\requirements.txt
git commit -m "lab4: add initial Titanic dataset"

python lab4\scripts\manage_dataset.py fill-age
python -m dvc add lab4\data\titanic.csv
git add lab4\data\titanic.csv.dvc
git commit -m "lab4: fill missing Age values"

python lab4\scripts\manage_dataset.py encode-sex
python -m dvc add lab4\data\titanic.csv
git add lab4\data\titanic.csv.dvc
git commit -m "lab4: one-hot encode Sex"
```

## Переключение между версиями

После перехода на нужный commit:

```powershell
git checkout <commit_hash>
python -m dvc checkout
```

## Отчет

В отчете нужно зафиксировать:

1. Инициализацию `git` и `dvc`.
2. Настройку `dvc remote`.
3. Три коммита с версиями датасета.
4. Команды `dvc push` и `dvc checkout`.
5. Скриншоты/лог структуры remote-хранилища.
