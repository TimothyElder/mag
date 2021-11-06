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

os.chdir('/home/timothyelder/mag')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

filtered_authors2papers = pd.read_csv('data/authors2papers.csv')

references_df = dd.read_csv(path + 'PaperReferences.txt', sep="\t",
                          header=None, error_bad_lines=False)

new_columns =['PaperId', 'PaperReferenceId']

references_df = references_df.rename(columns=dict(zip(references_df.columns, new_columns)))

filtered_references_df = references_df[references_df['PaperReferenceId'].isin(filtered_authors2papers['PaperId'])].compute()

filtered_references_df.to_csv('/home/timothyelder/mag/data/citing.csv', index=False)

# need to add to this script: get the paper information that now appeaars in the PaperId column of 
# he filtered_references_df dataframe, then save that as citing_papers.csv

papers_df = dd.read_csv(path + 'Papers.txt',
                        sep="\t", header=None, dtype={16: 'object', 17: 'object',
                                                      18: 'float64', 19: 'float64',
                                                      20: 'float64', 24: 'object',
                                                       7: 'float64', 9: 'object',
                                                       8: 'string', 14: 'float64'},
                                                       error_bad_lines=False, quoting=csv.QUOTE_NONE,
                                                       encoding='utf-8')

new_columns =['PaperId', 'Rank', 'Doi', 'DocType',
              'PaperTitle', 'OriginalTitle',
              'BookTitle', 'Year', 'Date',
              'OnlineDate', 'Publisher',
              'JournalId', 'ConferenceSeriesId',
              'ConferenceInstanceId', 'Volume',
              'Issue', 'FirstPage', 'LastPage',
              'ReferenceCount', 'CitationCount',
              'EstimatedCitation', 'OriginalVenue',
              'FamilyId', 'FamilyRank', 'DocSubTypes',
              'CreatedDate']

papers_df = papers_df.rename(columns=dict(zip(papers_df.columns, new_columns)))

filtered_papers = papers_df[papers_df['PaperId'].isin(filtered_references_df['PaperId'])].compute()

filtered_papers.to_csv('/home/timothyelder/mag/data/citing_papers.csv', index=False)

print("Script complete...")
