library(tidyverse)
library(network)

setwd("/home/timothyelder/mag")

journal2journal <- read.table("data/journal2journal_mat.txt")

sum(journal2journal)

# removing x from column names so the matrix is totally symmetric
colnames(journal2journal) <- sub("X", "", colnames(journal2journal))

journal2journal <- as.matrix(journal2journal)

journal_net <- as.network(journal2journal, matrix.type = "adjacency", ignore.eval = FALSE, names.eval = "weight", loops = TRUE)

rm(journal2journal)

network.density(journal_net)
