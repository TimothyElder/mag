import os
import pandas as pd
import csv
import dask.dataframe as dd

import re

# So the journal2journal network returned no
# ties but checking the below dataframe shows
# that there are many unique papers

adjacency.df <- papers2journals %>%
  group_by(JournalId) %>%
  dplyr::summarise(weight = n())

path = '/project/jevans/MAG_0802_2021_snap_shot/'


# This is just a list of the files
# in the MAG directory, need to figure out
# how they fit together.
#['PaperFieldsOfStudy.txt',
# 'FieldsOfStudy.txt',
# 'Papers_Pubyear_date_All.tsv',,
# 'PaperReferences.txt',
# 'Authors.txt',
# 'ConferenceSeries.txt',
# 'FieldOfStudyChildren.txt',
# 'RelatedFieldOfStudy.txt',
# 'ConferenceInstances.txt',
# 'PaperResources.txt',
# 'Affiliations.txt',
# 'PaperExtendedAttributes.txt',
# 'Papers.txt',
# 'PaperAuthorAffiliations.txt',
# 'Journals.txt',


# Don't run this line of code
# but I keep it here for reference
# df = pd.read_csv(path + 'Papers.txt', sep="\t", quoting=csv.QUOTE_NONE)


faculty_df_complete = pd.read_csv("/Users/timothyelder/Documents/soc_of_soc/data/base/faculty_df_complete.csv")
faculty_names = faculty_df_complete['faculty_name'].to_list()


pattern = r'(.+\,)(.+)' # regex for matching the first name and last name
aux_pattern = '(\S+)(.+)' # extra pattern for when the above doesn't match

for idx,i in enumerate(faculty_names):
    i = re.sub(r';|:', ',', i)
    # match regex to the file_name string
    if re.search(pattern, i) == None:
        match = re.search(aux_pattern, i)
        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1)
        new_name = new_name.lower()
        new_name = new_name.strip()

        faculty_names[idx] = new_name

    else:
        # match regex to the file_name string
        match = re.search(pattern, i)

        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1)
        new_name = new_name.lower()
        new_name = new_name.strip()

        faculty_names[idx] = new_name

papers_df = dd.read_csv(path + 'Papers.txt', sep="\t", header=None, dtype={16: 'object',
       17: 'object',
       18: 'float64',
       19: 'float64',
       20: 'float64',
       24: 'object',
       7: 'float64',
       9: 'object'})

papers_df.head()

authors_df = dd.read_csv(path + 'Authors.txt', sep="\t", header=None)

references_df = dd.read_csv(path + 'PaperReferences.txt', sep="\t", header=None)

# slice the first row of the df
papers_df.loc[0].compute()


# so I want to filter the big authors data frame just to get
# the faculty members in our network data here is an example
# df[df.name == 'Alice'].head()

new_columns = ['AuthorId', 'Rank', 'NormalizedName', 'DisplayName', 'LastKnownAffiliationId', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
authors_df = authors_df.rename(columns=dict(zip(authors_df.columns, new_columns)))

authors_df[authors_df['NormalizedName'] == 'peter conrad'].compute()


# this might be helpful for returning all the rows
# that have value in a list
df3 = df.x.isin(range(4)) # example

faculty_names = faculty_names[0:2] #subsetting for a test
new_df = authors_df[authors_df['NormalizedName'].isin(faculty_names)].compute()

this fucking worked

new_df.to_csv('/home/timothyelder/Documents/df.csv')

import multiprocessing

multiprocessing.cpu_count()

authors_df = dd.read_csv(path + 'Authors.txt', sep="\t", header=None)

new_columns = ['AuthorId', 'Rank', 'NormalizedName',
               'DisplayName', 'LastKnownAffiliationId',
               'PaperCount', 'PaperFamilyCount',
               'CitationCount', 'CreatedDate']

authors_df = authors_df.rename(columns=dict(zip(authors_df.columns, new_columns)))

authors_df.head()

authors_df[authors_df['NormalizedName'] == 'jenny trinitapoli'].compute()

affiliation_df = dd.read_csv(path + 'Affiliations.txt', sep="\t", header=None)

new_columns = ['AffiliationId', 'Rank', 'NormalizedName',
               'DisplayName', 'GridId', 'OfficialPage',
               'WikiPage', 'PaperCount', 'PaperFamilyCount',
               'CitationCount', 'Iso3166Code', 'Latitude',
               'Longitude', 'CreatedDate']

affiliation_df = affiliation_df.rename(columns=dict(zip(affiliation_df.columns, new_columns)))

affiliation_df.head()

ids = [40347166, 921990950]
#affiliation_df['AffiliationId'].isin(ids).compute()
affiliation_df[affiliation_df['AffiliationId'].isin([40347166, 921990950])].compute()
# df.fruit.isin(value_list)

scp filter_mag.py timothyelder@midway3.rcc.uchicago.edu:/home/timothyelder/Documents

scp net_projection.R timothyelder@cronusx.uchicago.edu:/home/timothyelder/mag/scripts

scp -r timothyelder@midway3.rcc.uchicago.edu:/home/timothyelder/Documents/scripts /Users/timothyelder/Desktop

scp -r timothyelder@midway3.rcc.uchicago.edu:/home/timothyelder/mag/data/disambig/edge_list.csv /Users/timothyelder/Documents/mag/data

scp -r timothyelder@midway3.rcc.uchicago.edu:/home/timothyelder/mag/data/filtered_cited.csv /Users/timothyelder/Documents/mag

# droppign all rows where the person has only one paper
df_filtered = df[df['PaperCount'] != 1]

pub_counts = pd.read_csv("/Users/timothyelder/Documents/jstor_parse/dataframes/pub_counts.csv")
jstor_metadata = pd.read_csv("/Users/timothyelder/Documents/jstor_parse/dataframes/jstor_metadata.csv")

scp -r timothyelder@cronusx.uchicago.edu:/home/timothyelder/mag/scripts /Users/timothyelder/Documents/mag


scp /home/timothyelder/mag/data/author2journal_mat.txt timothyelder@cronusx.uchicago.edu:/home/timothyelder

# For printing rows that contain a substrng
authors_df[authors_df['NormalizedName'].str.contains('levi martin')]


textfile = open("data/faculty_names.txt", "w")
for element in faculty_names:
    textfile.write(element + "\n")
textfile.close()


with open("data/faculty_names.txt", "w") as f:
    f.write(json.dumps(faculty_names))

#Now read the file back into a Python list object
with open("data/faculty_names.txt", "r") as f:
    faculty_names = json.loads(f.read())


scp faculty_df_complete.csv timothyelder@midway3.rcc.uchicago.edu:/home/timothyelder/mag/data

# for SCP the complete directory to JLMSHARE
scp -r /mag timothyelder@cronusx.uchicago.edu:/labs/jlmartinshare