import os
import re
import csv
import glob
import json
import pandas as pd
import dask.dataframe as dd

os.chdir('/home/timothyelder/mag')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

faculty_df_complete = pd.read_csv('data/faculty_df_complete.csv')

pattern = r'(.+\,)(.+)' # regex for matching the first name and last name
aux_pattern = '(\S+)(.+)' # extra pattern for when the above doesn't match

faculty_names = faculty_df_complete['faculty_name'].to_list()

for idx,i in enumerate(faculty_names):
    i = re.sub(r';|:', ',', i)
    # match regex to the file_name string
    if re.search(pattern, i) == None:
        match = re.search(aux_pattern, i)
        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1)
        new_name = re.sub('\.', '', new_name, count=1)
        new_name = re.sub('\‘', '', new_name, count=1)
        new_name = new_name.lower()
        new_name = new_name.strip()

        faculty_names[idx] = new_name

    else:
        # match regex to the file_name string
        match = re.search(pattern, i)

        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1)
        new_name = re.sub('\.', '', new_name, count=1)
        new_name = re.sub('\‘', '', new_name, count=1)
        new_name = new_name.lower()
        new_name = new_name.strip()
        
        faculty_names[idx] = new_name

faculty_df_complete['faculty_name'] = faculty_names

# concatenating individual matched dataframes
match_path = r'/home/timothyelder/mag/data/matches'
all_files = glob.glob(match_path + "/*.csv")
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files) # generate a list of files to concatenate

df_merged = pd.concat(df_from_each_file, ignore_index=True) # Concatenate pandas dataframes

df_merged = df_merged[df_merged['best_match_score'] >= .50]

names = df_merged['network_name'].to_list()

for idx, i in enumerate(names):
    i = re.sub('\.','', i)
    names[idx] = i

df_merged['network_name'] = names

# Load authors dataframe from MAG
authors_df = dd.read_csv(path + 'Authors.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ['AuthorId', 'Rank',
               'NormalizedName', 'DisplayName',
               'LastKnownAffiliationId', 'PaperCount',
               'PaperFamilyCount', 'CitationCount', 'CreatedDate']

authors_df = authors_df.rename(columns=dict(zip(authors_df.columns, new_columns)))

# Filter authors dataframe for authors that appear in network data.
filtered_authors = authors_df[authors_df['NormalizedName'].isin(faculty_df_complete.faculty_name)].compute()

df_merged = df_merged.drop(columns=['Unnamed: 0', 'best_match_score', '__id_left', '__id_right'])

more_filtered_authors = authors_df[authors_df['AuthorId'].isin(df_merged.AuthorId)].compute()

print(len(filtered_authors))
print(len(more_filtered_authors))
print(len(filtered_authors)+len(more_filtered_authors))

filtered_authors = filtered_authors.append(more_filtered_authors)

df_merged = df_merged[df_merged['NormalizedName'].isin(df_merged.NormalizedName)]

filtered_authors.to_csv('/home/timothyelder/mag/data/authors.csv', index=False)

df_merged.to_csv('/home/timothyelder/mag/data/key_faculty2authors.csv', index=False)
