# With this script, we take in all the fuzzy matches CSVs from
# the /matches directory, merging them all and then filtering
# the complete mag corpus to include the authors, papers, and
# journals from our probable matches.

# THIS SCRIPT IS TO BE RUN ON RCC MIDWAY3. SEE /sbatch DIRECTORY

import os
import re
import csv
import glob
import pandas as pd
import dask.dataframe as dd

os.chdir('/home/timothyelder/mag')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

# Filter authors dataframe for authors that appear in network data.
filtered_authors = pd.read_csv("data/authors.csv")

authors2papers_df = dd.read_csv(path + 'PaperAuthorAffiliations.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ['PaperId', 'AuthorId',
               'AffiliationId', 'AuthorSequenceNumber',
               'OriginalAuthor', 'OriginalAffiliation']

authors2papers_df = authors2papers_df.rename(columns=dict(zip(authors2papers_df.columns, new_columns)))

filtered_authors2papers = authors2papers_df[authors2papers_df['AuthorId'].isin(filtered_authors['AuthorId'])].compute()

filtered_authors2papers.to_csv('/home/timothyelder/mag/data/authors2papers.csv', index=False)

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

filtered_papers = papers_df[papers_df['PaperId'].isin(filtered_authors2papers['PaperId'])].compute()

filtered_papers.to_csv('/home/timothyelder/mag/data/papers.csv', index=False)

print("Script complete...")
