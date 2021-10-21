import os
import re
import pandas as pd
import csv
import dask.dataframe as dd

# With this script I want to return all papers in the 
# PaperReferenceId column of the PaperReferences table
# this is because I can count the number of times the
# PaperId of our focal authors appears in that column 
# over time to see the number of times their works are 
# cited. 

os.chdir('/home/timothyelder/Documents')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

filtered_authors2papers = pd.read_csv('data/filtered_authors2papers.csv')

references_df = dd.read_csv(path + 'PaperReferences.txt', sep="\t",
                          header=None, error_bad_lines=False)

new_columns =['PaperId', 'PaperReferenceId']

references_df = references_df.rename(columns=dict(zip(references_df.columns, new_columns)))

filtered_references_df = references_df[references_df['PaperReferenceId'].isin(filtered_authors2papers['PaperId'])].compute()

filtered_references_df.to_csv('/home/timothyelder/Documents/data/filtered_cited.csv')

print("Script complete...")
