library(tidyverse)
library(network)
library(sna)

setwd("/home/timothyelder/mag")

# Journal to Journal Matrix
journal2journal <- read.table("data/journal2journal_mat.txt")

# removing x from column names so the matrix is totally symmetric
colnames(journal2journal) <- sub("X", "", colnames(journal2journal))

authors <- read.csv("data/authors.csv")

authors2papers2journals <- read.csv("data/edge_list.csv")
authors2journals <- authors2papers2journals %>% select(JournalId, AuthorId)
papers2journals <- authors2papers2journals %>% select(JournalId, PaperId)

authors <- authors %>%
  select(NormalizedName, AuthorId)

journal_names <- read.csv("data/journals.csv")

journal2journal <- as.matrix(journal2journal)

journal_net <- as.network(journal2journal,
                          matrix.type = "adjacency", ignore.eval = FALSE,
                          names.eval = "weight", loops = TRUE)

pcout <- prcomp(journal2journal)

eigen <- evcent(journal_net)
JournalId <- journal_net %v% "vertex.names"
degree <- degree(journal_net)
prank <- igraph::page_rank(intergraph::asIgraph(journal_net), damping = 0.85)

pcoutrot_1 <- pcout$rotation[, 1]
pcoutrot_1 <- pcoutrot_1 * -1

journal_df <- data.frame(JournalId, eigen, prank$vector, degree, pcoutrot_1)

journal_df <- merge(journal_df, journal_names, by = "JournalId")

journal_df$pcoutrot_1[journal_df$pcoutrot_1 < 0] <- 0

journal_df$pcoutrot_sqrt <- sqrt(journal_df$pcoutrot_1)

write.csv(journal_df, "data/trunc_journal_ranks.csv", row.names = FALSE)