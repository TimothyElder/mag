library(tidyverse)
library(network)
library(sna)

setwd("/home/timothyelder/mag")

journal2journal <- read.table("data/journal2journal_mat.txt")

df <- read.csv('data/journals.csv')
df <- df[,2:3]

sum(journal2journal)

# removing x from column names so the matrix is totally symmetric
colnames(journal2journal) <- sub("X", "", colnames(journal2journal))

journal2journal <- as.matrix(journal2journal)

journal_net <- as.network(journal2journal, matrix.type = "adjacency", ignore.eval = FALSE, names.eval = "weight", loops = TRUE)

rm(journal2journal)

network.density(journal_net)

eigen <- evcent(journal_net)
JournalId <- journal_net %v% "vertex.names"
articles <- degree(journal_net)

journal_df <- data.frame(JournalId, eigen, articles)

journal_df <- journal_df[order(-journal_df$eigen),]
journal_df <- merge(journal_df, df, by = "JournalId")

journal_df$eigen[1:10]

journal_df$JournalId[1:10]

# to examine what the co-occurence looks like 
# extract column by name

#ASR 
journal2journal <- as.data.frame(journal2journal)

match <- journal2journal$`157620343`

new_df <- data.frame(match, row.names(journal2journal))

#economics 
match <- journal2journal$`3121261024`

new_df <- data.frame(match, row.names(journal2journal))

# science 
match <- journal2journal$`3880285`

new_df <- data.frame(match, row.names(journal2journal))
