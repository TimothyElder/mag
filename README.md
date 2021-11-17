# mag

squeue --user=timothyelder --start --iterate=10_seconds

### Measuring Scholarly Productibity of Sociologists Using Microsoft Academic Graph

This repo is a part of the broader [`soc_of_soc`](https://github.com/TimothyElder/soc_of_soc) project. With the scripts in this repository we complete several steps toward analyzing the individual academic productivity using the [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) corpus. The primary objective here is linking the network data to the publication data through probabilistic matching and some network analysis of journals. 

The code in this repo does the following things:

1. Fuzzy matching between the names of faculty members from the network data and the names of authors in the Microsoft Academic Graph using the [fuzzymatcher](https://github.com/RobinL/fuzzymatcher) library. This generates a large number of candidate matches.

2. Filtering the full Microsoft Academic Graph corpus down to only include the probable matches using [Dask](https://dask.org/).

3. Generating a network of journals in the corpus that are linked by shared authors. We use this network to help filter out non-sociologists from the dataset. The idea is that we can take eigenvector centrality scores of the journals and then score authors by how much they publish in high centrality (and therefore more likely to be sociology journals)


#### Data

This code requires data that lives in several different spots:

##### Network Data from *ASA Guide to Graduate Department*

The data from the ASA Guide to Graduate Department lives locally on my computer but is uploaded to two other locations. The Midway3 servers of the Reserach Computing Center of the University of Chicago and the Cronus Server of Social Science Computing Services, also at UChicago.

##### Microsoft Academic Graph Data

The Microsoft Academic Graph (MAG) lives on the Midway3 Servers and all the scripts related to parsing that data should be run on midway3, typically using `sbatch` scripts which describe the partitions, nodes and cores to use.

here is a table to show what scripts should be run where and in what order, as well as a short description.

|       Script          | Type     |  Where To Run |                                Description                              | Output |
|:----------------------|----------|:--------------|:------------------------------------------------------------------------|--------
| `fuzzy_matches.py`    | Data     |    Midway3    | Performs fuzzy matching produces many csvs     |       `/matches`        |
| `get_author_candidates.py`    | Data     |    Midway3    | filters the MAG corpus to get authors from fuzzy matching and saves key of faculty to author names from fuzzy matching     |       `key_faculty2authors.csv, authors.csv`        |
| `filter_mag_corpus.py`| Data     |    Midway3    | Filters out the complete MAG data down to the names we feed it |  `authors2papers.csv, papers.csv`   |
| `filter_journals.py`  | Data     |    Midway3    | Does the same but now for journals |    `journals.csv`     |
| `filtered_cited`      | Data     |    Midway3    | Filters papers to get only the ones citing our authors papers |   `citing.csv`     |
| `net_project.py`      | Data     |    Midway3    | Projects the two-mode network to a one-mode, journal to journal network |  `journal2journal_mat.csv`, `authors2journals_mat.csv`      |
| `journal_net.R`       | Analysis |     Local     | Performs first analyses on the journal to journal network |   None    |
