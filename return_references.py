import os
import pandas as pd
import csv
import dask.dataframe as dd

import re

path = '/project/jevans/MAG_0802_2021_snap_shot/'

filtered_authors2papers = pd.read_csv('filtered_authors2papers.csv')

references_df = dd.read_csv(path + 'PaperReferences.txt', sep="\t",
                          header=None, error_bad_lines=False)

new_columns =['PaperId', 'PaperReferenceId']

references_df = references_df.rename(columns=dict(zip(references_df.columns, new_columns)))

filtered_references_df  = references_df[references_df['PaperId'].isin(filtered_authors2papers['PaperId'])].compute()

filtered_references_df.to_csv('/home/timothyelder/Documents/filtered_references_df.csv')

print("Script complete...")
