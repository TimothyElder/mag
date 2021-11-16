import re 
import os 
import json
import scipy
import dask.array as da
import networkx as nx
import pandas as pd 
from scipy import sparse
import numpy as np

os.chdir('/home/timothyelder/mag')

authors_df = pd.read_csv("data/authors.csv", low_memory=False) 
authors2papers_df = pd.read_csv("data/authors2papers.csv")
papers_df = pd.read_csv("data/papers.csv")
papers2journals = pd.read_csv("data/edge_list.csv", dtype = {"PaperId": int, "AuthorId": int, "JournalId": int})

authors2journals = papers2journals.drop(columns="PaperId") # droping paperids to get authors2journals edgelist
authors2journals = authors2journals.drop_duplicates() # dropping duplicates to save memory

B = nx.Graph()
B.add_nodes_from(authors2journals.JournalId, bipartite=0)
B.add_nodes_from(authors2journals.AuthorId, bipartite=1)
B.add_edges_from(
    [(row['JournalId'], row['AuthorId']) for idx, row in authors2journals.iterrows()])
nx.is_bipartite(B)

top_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
bottom_nodes = set(B) - top_nodes

M = nx.algorithms.bipartite.matrix.biadjacency_matrix(B, row_order=bottom_nodes)

mat = M.transpose() @ M

df = pd.DataFrame(mat, columns=top_nodes, index=top_nodes)

df.to_csv("/home/timothyelder/mag/data.csv")