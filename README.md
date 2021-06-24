# pandas-list-merge
Merge a dirty CSV and JSON list with python pandas library and export it as csv.

Setup:
```
python3 -m venv plm
source ../plm/bin/activate
pip install -r requirements.txt
```

Usage:
```
python3 app.py --csv-file "files/list.csv" --json-file "files/list.json" --csv-merge "files/merged.csv" --log True
```


