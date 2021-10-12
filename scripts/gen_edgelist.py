import pandas as pd

authors2papers_df = pd.read_csv('/home/timothyelder/mag/data/authors2papers.csv')

authors2papers_df.drop(columns=['AffiliationId', 'AuthorSequenceNumber',
                                'OriginalAuthor', 'OriginalAffiliation'])

papers_df = pd.read_csv('/home/timothyelder/mag/data/papers.csv')

papers_df.drop(columns=['Rank', 'Doi', 'DocType',
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

authors2papers_df = authors2papers_df.set_index("PaperId")

edge_list_df = papers_df.merge(authors2papers_df, how='left', on='PaperId')

edge_list_df.to_csv('/home/timothyelder/mag/data/edge_list.csv')

len(papers_df.index) == len(edge_list_df.index)
