import os
import re
import csv
import pandas as pd
import dask.dataframe as dd

# load dataframes
papers_df = dd.read_csv('/home/timothyelder/Documents/data/disambig/filtered_papers.csv')

papers2authors_df = dd.read_csv('/home/timothyelder/Documents/data/disambig/filtered_authors2papers.csv')

journals_df = dd.read_csv('/home/timothyelder/Documents/data/disambig/filtered_journals.csv')

dd.papers_df.merge(journals_df, how = 'left',  left_on = 'JournalId', right_on = 'JournalId')

# getting journals

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

filtered_journals = journals_df[journals_df['PaperId'].isin(filtered_papers['JournalId'])].compute()

filtered_journals.to_csv('/home/timothyelder/Documents/data/disambig/filtered_journals.csv')


print("Script complete...")




