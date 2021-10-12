import os
import re
import csv
import pandas as pd
import dask.dataframe as dd

os.chdir('/home/timothyelder/Documents')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

papers_df = pd.read_csv('/home/timothyelder/Documents/data/papers.csv')

journals_df = dd.read_csv(path + 'Journals.txt', sep="\t", header=None, dtype={5: 'object'},
                                                       error_bad_lines=False, quoting=csv.QUOTE_NONE,
                                                       encoding='utf-8')

new_columns = ['JournalId', 'Rank', 'NormalizedName',
               'DisplayName', 'Issn', 'Publisher',
               'Webpage', 'PaperCount', 'PaperFamilyCount',
               'CitationCount', 'CreatedDate']

journals_df = journals_df.rename(columns=dict(zip(journals_df.columns, new_columns)))

journals_df = journals_df.drop(columns=['Rank', 'DisplayName', 'Issn', 'Publisher',
                          'Webpage', 'PaperCount', 'PaperFamilyCount',
                          'CitationCount', 'CreatedDate'])

filtered_journals = journals_df[journals_df['JournalId'].isin(papers_df.JournalId)].compute()

filtered_journals.to_csv('/home/timothyelder/Documents/data/journals.csv')


print("Script complete...")
