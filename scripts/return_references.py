import os
import re
import pandas as pd
import csv
import dask.dataframe as dd

# This script returns what papers the focal author's
# papers write, rather then which papers cite our 
# focal authors papers. This script produces a filtered 
# dataframe that is not as useful as I originally thought. 

os.chdir('/home/timothyelder/Documents')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

filtered_authors2papers = pd.read_csv('data/filtered_authors2papers.csv')

references_df = dd.read_csv(path + 'PaperReferences.txt', sep="\t",
                          header=None, error_bad_lines=False)

new_columns =['PaperId', 'PaperReferenceId']

references_df = references_df.rename(columns=dict(zip(references_df.columns, new_columns)))

filtered_references_df  = references_df[references_df['PaperId'].isin(filtered_authors2papers['PaperId'])].compute()

filtered_references_df.to_csv('/home/timothyelder/Documents/data/filtered_references.csv')

print("Script complete...")
