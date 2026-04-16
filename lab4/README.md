# lab4

`DVC remote`: `C:\Users\likip\dvc_remote\Auto_MO_Group_3_lab4`

## Commands

```powershell
python -m pip install --user -r lab4\requirements.txt
python -m dvc init
python -m dvc remote add -d lab4_local C:\Users\likip\dvc_remote\Auto_MO_Group_3_lab4
```

```powershell
python lab4\scripts\manage_dataset.py create-base
python -m dvc add lab4\data\titanic.csv
python -m dvc push
git commit -am "lab4: add initial Titanic dataset"

python lab4\scripts\manage_dataset.py fill-age
python -m dvc add lab4\data\titanic.csv
python -m dvc push
git commit -am "lab4: fill missing Age values"

python lab4\scripts\manage_dataset.py encode-sex
python -m dvc add lab4\data\titanic.csv
python -m dvc push
git commit -am "lab4: one-hot encode Sex"
```

## Versions

- `9fcff7a` - base dataset
- `911fb69` - filled `Age`
- `d625136` - one-hot `Sex`

## Checkout

```powershell
git checkout <commit>
python -m dvc checkout
```
