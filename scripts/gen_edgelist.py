import pandas as pd

authors2papers_df = pd.read_csv('/home/timothyelder/Documents/data/authors2papers.csv')

authors2papers_df = authors2papers_df.drop(columns=['Unnamed: 0', 'AffiliationId', 'AuthorSequenceNumber',
                                'OriginalAuthor', 'OriginalAffiliation'])

papers_df = pd.read_csv('/home/timothyelder/Documents/data/papers.csv', low_memory=False)

papers_df = papers_df.drop(columns=['Unnamed: 0', 'Rank', 'Doi', 'DocType',
              'PaperTitle', 'OriginalTitle',
              'BookTitle', 'Year', 'Date',
              'OnlineDate', 'Publisher',
              'ConferenceSeriesId', 'CreatedDate',
              'ConferenceInstanceId', 'Volume',
              'Issue', 'FirstPage', 'LastPage',
              'ReferenceCount', 'CitationCount',
              'EstimatedCitation', 'OriginalVenue',
              'FamilyId', 'FamilyRank', 'DocSubTypes'])

papers_df = papers_df.set_index("PaperId")

papers_df = papers_df[papers_df["DocType"] == "Journal"]

authors2papers_df = authors2papers_df.set_index("PaperId")

edge_list_df = papers_df.merge(authors2papers_df, how='left', on='PaperId')

if len(papers_df.index) == len(edge_list_df.index):
    print("script successeful")

edge_list_df.to_csv('/home/timothyelder/Documents/data/edge_list.csv')
