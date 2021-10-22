import re
import os
import pandas as pd
import fuzzymatcher as fuzz

os.chdir('/home/timothyelder/Documents/')

pattern = r'(.+\,)(.+)' # regex for matching the first name and last name
aux_pattern = '(\S+)(.+)' # extra pattern for when the above doesn't match

faculty_df_complete = pd.read_csv("/home/timothyelder/mag/data/faculty_df_complete.csv")
faculty_names = faculty_df_complete['faculty_name'].to_list()

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

    i = re.sub('.', '', i)

        faculty_names[idx] = new_name

faculty_df_complete['network_name'] = faculty_names

faculty_df_complete = faculty_df_complete.drop(columns=['current_dept', 'year_observed', 'source_dept',
       'phd_year', 'highest_degree', 'interests', 'position', 'phd_age',
       'Degree.source', 'Eig.source', 'Degree.current', 'Eig.current',
       'diff.eig'])


data_dir = 'data/authors_csvs/'
save_dir = 'data/matches/'

for i in os.listdir(data_dir):
    # pass if matched dataframe already in matches director
    if 'matched_' + i in os.listdir(save_dir):
        pass

    else:
        authors_df = pd.read_csv(data_dir + i)

        authors_df = authors_df.drop(columns=['Rank','DisplayName',
                                      'LastKnownAffiliationId',
                                      'PaperCount', 'PaperFamilyCount',
                                      'CitationCount', 'CreatedDate'])

        fuzzy_matches = fuzz.fuzzy_left_join(faculty_df_complete,
                                             authors_df,
                                             left_on = "network_name",
                                             right_on = "NormalizedName")

        fuzzy_matches.to_csv(save_dir + 'matched_' + i)

print("script complete......")
