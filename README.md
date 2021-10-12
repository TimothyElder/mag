# mag

### Disambiguating Scholars in Microsoft Academic Graph

This repo is a part of the broader [`soc_of_soc`](https://github.com/TimothyElder/soc_of_soc) project. In this portion we complete several steps toward analyzing the individual academic productivity using the [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) corpus. The primary objective here is linking the network data to the publication data. The code in this repo does the following things:

1. Performing fuzzy matching between the names of faculty members from the network data and the names of authors in the Microsoft Academic Graph using the [fuzzymatcher](https://github.com/RobinL/fuzzymatcher) library. This generates a large number of candidate matches.

2. Filtering the full Microsoft Academic Graph corpus down to only include the probable matches using [Dask](https://dask.org/).

3. Generating a network of journals in the corpus that are linked by shared authors. We use this network to help filter out non-sociologists from the dataset. The idea is that we can take eigenvector centrality scores of the journals and then score authors by how much they publish in high centrality (and therefore more likely to be sociology journals)
