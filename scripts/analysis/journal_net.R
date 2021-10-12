library(tidyverse)
library(statnet)

setwd("/Users/timothyelder/Documents/mag")

journal2journal <- read.table("data/journal2journal_mat.txt")

sum(journal2journal)

journal_net <- as.network(journal2journal, directed = FALSE, bipartite = FALSE, loops = TRUE, multiple = TRUE)

rm(journal2journal)
