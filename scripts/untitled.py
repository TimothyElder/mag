# THIS SCRIPT IS TO BE RUN ON RCC MIDWAY3. SEE /sbatch DIRECTORY

import os
import re
import csv
import glob
import pandas as pd
import dask.dataframe as dd

os.chdir('/home/timothyelder/Documents')

path = '/project/jevans/MAG_0802_2021_snap_shot/'

fields = dd.read_csv(path + 'FieldsOfStudy.txt',
                                           sep="\t", header=None,
                                           error_bad_lines=False,
                                           quoting=csv.QUOTE_NONE,
                                           encoding='utf-8')

new_columns = ["FieldOfStudyId", "Rank", "NormalizedName",
               "DisplayName", "MainType", "Level", "PaperCount",
               "PaperFamilyCount", "CitationCount", "CreatedDate"]

fields = fields.rename(columns=dict(zip(fields.columns, new_columns)))

144024400

PapersFields