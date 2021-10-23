library(tidyverse)
library(network)
library(sna)

#setwd("/home/timothyelder/mag")

journal2journal <- read.csv("data/journal2journal_mat.csv")

papers2journals <- read.csv("data/edge_list.csv")

authors <- read.csv("data/authors.csv")
authors2journals <- read.csv("data/authors2journals.csv")

authors <- authors %>% 
  select(network_name, AuthorId)

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
degree <- degree(journal_net)
prank <- igraph::page_rank(intergraph::asIgraph(journal_net), damping = 0.85)

journal_df <- data.frame(JournalId, eigen, prank$vector, degree)

journal_df <- journal_df[order(-journal_df$eigen),]

journal_df <- select(journal_df, -X)

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

#### Calcualting mean eigen scores for authors #####

another_df <- merge(papers2journals, journal_df, by = "JournalId")

authors_df <- merge(another_df, authors, by = "AuthorId")


authors_df <- authors_df %>% 
  group_by(network_name) %>%
  summarise(eigen_mean = mean(eigen), prank_mean = mean(prank.vector), n = n(), degree_mean = mean(degree))
  
eig <- ggplot(authors_df, aes(x = eigen_mean)) + geom_density() + ggtitle("Author Mean Eigen")

prank <- ggplot(authors_df, aes(x = prank_mean)) + geom_density() + ggtitle("Authors Mean Page Rank")

deg <- ggplot(authors_df, aes(x = degree_mean)) + geom_density() + ggtitle("Author Mean Degree")

articles <- ggplot(authors_df, aes(x = n)) + geom_density() + ggtitle("Author NUmber of Articles")

all.g <- ggpubr::ggarrange(eig, prank, deg, articles)

ggsave("author_scores.pdf", all.g)

#### HISTOGRAMS #####

eig <- ggplot(authors_df, aes(x = eigen_mean)) + geom_histogram() + ggtitle("Author Mean Eigen")

prank <- ggplot(authors_df, aes(x = prank_mean)) + geom_histogram() + ggtitle("Authors Mean Page Rank")

deg <- ggplot(authors_df, aes(x = degree_mean)) + geom_histogram() + ggtitle("Author Mean Degree")

articles <- ggplot(authors_df, aes(x = n)) + geom_histogram() + ggtitle("Author NUmber of Articles")

all.g <- ggpubr::ggarrange(eig, prank, deg, articles)

ggsave("author_scores_hist.pdf", all.g)

ggplot(journal_df, aes(x = eigen)) + geom_density()

ggplot(journal_df, aes(x = prank.vector)) + geom_density()

ggplot(journal_df, aes(x = degree)) + geom_density()
