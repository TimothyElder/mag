import os
import re
import csv
import pandas as pd
import dask.dataframe as dd

path = '/project/jevans/MAG_0802_2021_snap_shot/'

os.chdir('/home/timothyelder/mag')

# Load authors dataframe from MAG
authors_df = dd.read_csv(path + 'Authors.txt', header = None, delimiter="\t", quoting=csv.QUOTE_NONE, encoding='utf-8')

authors_df = authors_df.repartition(npartitions=100)

o = authors_df.to_csv("/home/timothyelder/mag/data/authors_csvs/part_*.csv", index=False)


