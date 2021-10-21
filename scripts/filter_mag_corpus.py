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

os.chdir('/home/timothyelder/Documents')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

# concatenating individual matched dataframes
match_path = r'/home/timothyelder/mag/data/matches'
all_files = glob.glob(match_path + "/*.csv")
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files) # generate a list of files to concatenate

df_merged = pd.concat(df_from_each_file, ignore_index=True) # Concatenate pandas dataframes

# Saving Merged dataframe
df_merged.to_csv("/home/timothyelder/mag/data/authors.csv", index=False)

faculty_names = df_merged.network_name.to_list()

# for index and name in faculty names
for idx,i in enumerate(faculty_names):
    i = re.sub(r'\.', '', i) # replace semi-colons with commas
    faculty_names[idx] = i # substitute original name with normalized name

df_merged.network_name = faculty_names

# Exact matches
df = df_merged[df_merged['network_name'] == df_merged['NormalizedName']]

# Keeping only matches above .4 match scrore
df_filtered = df.append(df_merged[df_merged['best_match_score'] >= .4])

authors2papers_df = dd.read_csv(path + 'PaperAuthorAffiliations.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ['PaperId', 'AuthorId',
               'AffiliationId', 'AuthorSequenceNumber',
               'OriginalAuthor', 'OriginalAffiliation']

authors2papers_df = authors2papers_df.rename(columns=dict(zip(authors2papers_df.columns, new_columns)))

filtered_authors2papers = authors2papers_df[authors2papers_df['AuthorId'].isin(df_filtered['AuthorId'])].compute()

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
