from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
import difflib
import dask.dataframe as dd
import dask.multiprocessing
import dask.threaded


master= pd.DataFrame({'original':['this is a nice sentence',
'this is another one',
'stackoverflow is nice']})


slave= pd.DataFrame({'name':['hello world',
'congratulations',
'this is a nice sentence ',
'this is another one',
'stackoverflow is nice'],'my_value': [2,1,2,3,1]})

def fuzzy_score(str1, str2):
    return fuzz.token_set_ratio(str1, str2)

def helper(orig_string, slave_df):
    #use fuzzywuzzy to see how close original and name are
    slave_df['score'] = slave_df.name.apply(lambda x: fuzzy_score(x,orig_string))
    #return my_value corresponding to the highest score
    return slave_df.loc[slave_df.score.idxmax(),'my_value']
    #return slave_df[slave_df.score >90]

master['my_value'] = master.original.apply(lambda x: helper(x,slave))

dmaster = dd.from_pandas(master, npartitions=4)
dmaster['my_value'] = dmaster['my_value'] = master.original.apply(lambda x: helper(x,slave))
dmaster.compute()


##### Customizing code for my data

from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
import difflib
import dask.dataframe as dd
import dask.multiprocessing
import dask.threaded


first_df = pd.DataFrame({'original':['this is a nice sentence',
'this is another one',
'stackoverflow is nice']})


second_df = pd.DataFrame({'name':['hello world',
'congratulations',
'this is a nice sentence ',
'this is another one',
'stackoverflow is nice'],'my_value': [2,1,2,3,1]})

# this returns a score evaluating the match between two strings
def fuzzy_score(str1, str2):
    return fuzz.token_set_ratio(str1, str2)

# when used with a list comprehension
def helper(orig_string, other_df):
    #use fuzzywuzzy to see how close original and name are
    other_df['score'] = other_df.name.apply(lambda x: fuzzy_score(x,orig_string))
    #return my_value corresponding to the highest score
    return other_df.loc[other_df['score']>7]

#first_df['my_value'] = first_df.original.apply(lambda x: helper(x,second_df))

d_first_df = dd.from_pandas(first_df, npartitions=4)
d_first_df['my_value'] = d_first_df['my_value'] = first_df.original.apply(lambda x: helper(x,second_df))
d_first_df.compute()

#### Now writing specifically for the mag data

#drop everything but the facult_name after NORMALIZING it
faculty_df_complete = pd.DataFrame({'original':['this is a nice sentence',
'this is another one',
'stackoverflow is nice']})

#drop everything but the normalized name (name) and the authorid (my_value)
authors_df = pd.DataFrame({'name':['hello world',
                                    'congratulations',
                                    'this is a nice sentence ',
                                    'this is another one',
                                    'stackoverflow is nice'],
                           'my_value': [2,1,2,3,1]})



def fuzzy_score(str1, str2):
    return fuzz.token_set_ratio(str1, str2)

def helper(orig_string, other_df):
    #use fuzzywuzzy to see how close original and name are
    other_df['score'] = other_df.name.apply(lambda x: fuzzy_score(x,orig_string))
    #return my_value corresponding to the highest score
    return other_df[other_df.score >= 90]

first_df['my_value'] = first_df.original.apply(lambda x: helper(x,second_df))

dd_authors_df = dd.from_pandas(authors_df, npartitions=100) # 100 partitions

dd_authors_df['my_value'] = faculty_names.original.apply(lambda x: helper(x,authors_df))

dd_authors_df.compute()


# Some tests

fuzzy_score('this is a nice sentence', 'stackoverflow is nice')
helper('this is a nice sentence', second_df)
