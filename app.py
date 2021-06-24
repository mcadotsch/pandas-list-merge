import pandas as pd
import json
from argparse import ArgumentParser
from pandas import json_normalize

log_console: bool = False

def log(str: str):
  if(log_console):
    print("*****************************************************")
    print(str)

def get_validated_df_csv(file: str):
  #TODO file exception handling
  df_csv = pd.DataFrame(pd.read_csv(file, sep=';', delimiter=None))

  # align key column naming
  df_csv = df_csv.rename(columns={'family name':'lastname'})
  df_csv = df_csv.rename(columns={'name':'firstname'})

  # create id to be able to remove duplicates
  df_csv["id"] = df_csv["firstname"].map(str)+"."+df_csv["lastname"].map(str)
  df_csv = df_csv.drop_duplicates(subset=['id'])

  log(df_csv)

  return df_csv

def get_validated_df_json(file: str):
  #TODO file exception handling 
  with open(file) as data:
    raw_json = json.load(data)

  # normalize json
  df_json = json_normalize(raw_json['Students'])

  # align key column naming
  df_json = df_json.rename(columns={'f_name':'lastname'})
  df_json = df_json.rename(columns={'name':'firstname'})

  # create id to be able to remove duplicates
  df_json["id"] = df_json["firstname"].map(str)+"."+df_json["lastname"].map(str)
  df_json = df_json.drop_duplicates(subset=['id'])

  log(df_json)

  return df_json

def merge(df_csv, df_json, filter_col, filter_value):
  if(filter_col and filter_value):
    data = df_json.merge(df_csv,how='outer').where(df_json[filter_col] == filter_value).dropna(how='all')
  else:
    data = df_json.merge(df_csv,how='outer').dropna(how='all')

  # remove id column after merge
  data = data.drop(["id"],axis=1)

  log(data)

  return data

def main(csv_file: str, json_file: str, merge_file: str):
  # get proper data
  data_csv = get_validated_df_csv(csv_file)
  data_json = get_validated_df_json(json_file)

  # merge it with an optional filter
  data = merge(data_csv, data_json, "class", "2a")

  # export to a csv somewhere on the filesystem
  data.to_csv(merge_file)

if __name__ == '__main__':
    p = ArgumentParser()
 
    p.add_argument("--csv-file", required=True, type=str, help="Path to csv file")
    p.add_argument("--json-file", required=True, type=str, help="Path to json file")
    p.add_argument("--csv-merge", required=True, type=str, help="Path to merged csv file")
    p.add_argument("--log", required=False, type=bool, help="Log to console")

    args = p.parse_args()

    log_console = args.log==True
 
    main(args.csv_file, args.json_file, args.csv_merge)