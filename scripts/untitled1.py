affiliations_df = dd.read_csv(path + 'Affiliations.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ['AffiliationId', 'Rank', 'NormalizedName', 'DisplayName',
               'GridId', 'OfficialPage', 'WikiPage', 'PaperCount', 
               'PaperFamilyCount', 'CitationCount', 'Iso3166Code', 'Latitude', 
               'Longitude', 'CreatedDate']

affiliations_df = affiliations_df.rename(columns=dict(zip(affiliations_df.columns, new_columns)))

affiliations_df.DisplayName.unique

name = affiliations_df.DisplayName

name.unique

cols = list(ddf.columns[2:4])
ddf[cols].compute()


affiliations_df[affiliations_df['DisplayName'] == "Yale University"].compute()

affiliations_df[affiliations_df['DisplayName'] == "University of Chicago"].compute()

affiliations_df[affiliations_df['DisplayName'] == "University of Chicago"].compute()

affiliations_df[affiliations_df['DisplayName'].str.contains('University of Nebraska')].compute()

affiliations_df[affiliations_df['AffiliationId'] == "40347166"].compute()

affiliations_df[affiliations_df['AffiliationId'] == "149910238"].compute()
149910238
40347166


authors_df = dd.read_csv(path + 'Authors.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ['AuthorId', 'Rank', 'NormalizedName',
               'DisplayName', 'LastKnownAffiliationId',
               'PaperCount', 'PaperFamilyCount',
               'CitationCount', 'CreatedDate']

authors_df = authors_df.rename(columns=dict(zip(authors_df.columns, new_columns)))

authors_df[authors_df['NormalizedName'].str.contains('levi martin')]

authors_df[authors_df['NormalizedName'] == 'john levi martin'].compute()

# Papers 2 authors affiliations

authors2papers_df = dd.read_csv(path + 'PaperAuthorAffiliations.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ['PaperId', 'AuthorId',
               'AffiliationId', 'AuthorSequenceNumber',
               'OriginalAuthor', 'OriginalAffiliation']

authors2papers_df = authors2papers_df.rename(columns=dict(zip(authors2papers_df.columns, new_columns)))