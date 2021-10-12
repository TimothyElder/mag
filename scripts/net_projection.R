library("network")

# Return Named Edge List
name_edgelist <- function(graph_object){

  # Return an edgelst from the gaph object
  # that is named rather than using nodeIDs

  names <- graph_object %v% "vertex.names"

  numbers <- 1:network.size(graph_object)

  df <- as.data.frame(cbind(names, numbers))

  n <- as.data.frame(as.edgelist(graph_object))

  n$V1 <- plyr::mapvalues(n$V1,
                          from = numbers,
                          to = names,
                          warn_missing = FALSE)

  n$V2 <- plyr::mapvalues(n$V2,
                          from=numbers,
                          to=names,
                          warn_missing = FALSE)

  n <- n %>%
    rename("PaperId" = "V1",
           "JournalId" = "V2")
  return(n)
}

papers2journals <- read.csv("/home/timothyelder/mag/data/edge_list.csv")

papers2journals <- na.omit(papers2journals)

papers2journals <- papers2journals[,2:3]

papers2journals <- papers2journals[c(2, 1)]

papers2journals <- papers2journals[!duplicated(papers2journals), ]

papers2journals <- as.data.frame(papers2journals)

bi_net <- network(papers2journals, bipartite = TRUE)

bi_mat <- as.matrix(bi_net)

journal2journal_mat <- t(bi_mat) %*% bi_mat

journal_net <- as.network(journal2journal_mat, directed = FALSE)

write.table(journal2journal_mat,
  file = "/home/timothyelder/mag/data/journal2journal_mat.txt")

write.table(bi_mat,
  file = "/home/timothyelder/mag/data/author2journal_mat.csv")
