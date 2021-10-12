library(tidyverse)
library(network)

# Return Named Edge List
name_edgelist <- function(graph_object) {

  # Return an edgelst from the gaph object
  # that is named rather than using nodeIDs

  names <- graph_object %v% "vertex.names"

  numbers <- 1:network.size(graph_object)

  df <- as.data.frame(cbind(names, numbers))

  n <- as.data.frame(as.edgelist(graph_object))

  n$V1 <- plyr::mapvalues(n$V1,
                          from = numbers,
                          to = names)

  n$V2 <- plyr::mapvalues(n$V2,
                          from=numbers,
                          to=names)

  n <- n %>%
    rename("PaperId" = "V1",
           "JournalId" = "V2")
  return(n)
}

papers2journals <- read.csv("/home/timothyelder/Documents/data/edge_list.csv")

# Drop first column which is nothing
papers2journals <- papers2journals[,2:3]

# Convert to dataframe
papers2journals <- as.data.frame(papers2journals)

# Create binary network from papers2journals edgelist
bi_net <- network(papers2journals, bipartite = TRUE)

# return edgelist from binary network
el <- as.edgelist(bi_net)

bi_net <- network(papers2journals, bipartite = TRUE)

get.adjacency(bi_net)

bi_mat <- as.matrix(bi_net)

journal2journal_mat <- t(bi_mat) %*% bi_mat

journal_net <- as.network(journal2journal_mat, directed = FALSE)

rm(journal2journal_mat)

write.table(journal2journal_mat, file = "journal2journal.txt")

write.table(papers2journals_mat, file= "test.txt")
