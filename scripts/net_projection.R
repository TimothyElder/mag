library("network")

setwd('/home/timothyelder/mag')

papers2journals <- read.csv("data/edge_list.csv")

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
  file = "/home/timothyelder/mag/data/journal2journal_mat.csv")

write.table(bi_mat,
  file = "/home/timothyelder/mag/data/author2journal_mat.csv")
