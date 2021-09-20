import os
import pandas as pd
import csv
import dask.dataframe as dd
import re

os.chdir('/home/timothyelder/Documents')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

# Load faculty data from network dataset
faculty_df_complete = pd.read_csv("/home/timothyelder/Documents/data/faculty_df_complete.csv")

faculty_names = faculty_df_complete['faculty_name'].to_list()

# reorient names from "Lastname, Firstname"
# to "firstname lastname" form to match MAG data

pattern = r'(.+\,)(.+)' # regex for matching the first name and last name
aux_pattern = '(\S+)(.+)' # extra pattern for when the above doesn't match

# for index and name in faculty names
for idx,i in enumerate(faculty_names):
    i = re.sub(r';|:', ',', i) # replace semi-colons with commas
    # match regex to the file_name string
    if re.search(pattern, i) == None:
        match = re.search(aux_pattern, i)
        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1) # remove comma
        new_name = new_name.lower() # lower case
        new_name = new_name.strip() # strip whitespace

        faculty_names[idx] = new_name # substitute original name with normalized name

    else:
        # match regex to the file_name string
        match = re.search(pattern, i)

        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1) # remove comma
        new_name = new_name.lower() # lower case
        new_name = new_name.strip() # strip whitespace

        faculty_names[idx] = new_name # substitute original name with normalized name

# Load authors dataframe from MAG
authors_df = dd.read_csv(path + 'Authors.txt', sep="\t",
                         header=None, error_bad_lines=False)

new_columns = ['AuthorId', 'Rank',
               'NormalizedName', 'DisplayName',
               'LastKnownAffiliationId', 'PaperCount',
               'PaperFamilyCount', 'CitationCount', 'CreatedDate']

authors_df = authors_df.rename(columns=dict(zip(authors_df.columns, new_columns)))

# Filter authors dataframe for authors that appear in network data.
filtered_authors = authors_df[authors_df['NormalizedName'].isin(faculty_names)].compute()

filtered_authors = filtered_authors[filtered_authors['PaperCount'] != 1] # Dropping authors with only one publication

filtered_authors.to_csv('/home/timothyelder/Documents/data/filtered_authors.csv')

authors2papers_df = dd.read_csv(path + 'PaperAuthorAffiliations.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False, quoting=csv.QUOTE_NONE, encoding='utf-8')

new_columns = ['PaperId', 'AuthorId',
               'AffiliationId', 'AuthorSequenceNumber',
               'OriginalAuthor', 'OriginalAffiliation']

authors2papers_df = authors2papers_df.rename(columns=dict(zip(authors2papers_df.columns, new_columns)))

filtered_authors2papers = authors2papers_df[authors2papers_df['AuthorId'].isin(filtered_authors['AuthorId'])].compute()

filtered_authors2papers.to_csv('/home/timothyelder/Documents/data/filtered_authors2papers.csv')

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

filtered_papers.to_csv('/home/timothyelder/Documents/data/filtered_papers.csv')

print("Script complete...")
