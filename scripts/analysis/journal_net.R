library(tidyverse)
library(network)
library(sna)

setwd("/home/timothyelder/mag")

# Journal to Journal Matrix
journal2journal <- read.csv("data/journal2journal.csv")

rownames(journal2journal) <- journal2journal$X
journal2journal <- journal2journal %>% select(-X)

# removing x from column names so the matrix is totally symmetric
colnames(journal2journal) <- sub("X", "", colnames(journal2journal))

authors <- read.csv("data/authors.csv")

authors2papers2journals <- read.csv("data/authors2papers.csv")
authors2journals <- authors2papers2journals %>% select(JournalId, AuthorId)

authors <- authors %>%
  select(NormalizedName, AuthorId)

journal_names <- read.csv("data/journals.csv")
journal_names <- journal_names[, 2:3]


journal2journal <- as.matrix(journal2journal)

journal_net <- as.network(journal2journal,
                          matrix.type = "adjacency", ignore.eval = FALSE,
                          names.eval = "weight", loops = TRUE)

pcout <- prcomp(journal2journal)

eigen <- evcent(journal_net)
JournalId <- journal_net %v% "vertex.names"
degree <- degree(journal_net)
prank <- igraph::page_rank(intergraph::asIgraph(journal_net), damping = 0.85)

pcoutrot_2 <- pcout$rotation[, 2]
pcoutrot_1 <- pcout$rotation[, 1]
pcoutrot_1 <- pcoutrot_1 * -1

journal_df <- data.frame(JournalId, eigen, prank$vector,
                          degree, pcoutrot_1, pcoutrot_2)

journal_df <- journal_df[order(journal_df$pcoutrot_1), ]
journal_df <- journal_df[order(-journal_df$pcoutrot_1), ]

journal_df <- merge(journal_df, journal_names, by = "JournalId")

range(journal_df$pcoutrot_1)

journal_df$pcoutrot_1[journal_df$pcoutrot_1 < 0] <- 0

journal_df$pcoutrot_sqrt <- sqrt(journal_df$pcoutrot_1)

write.csv(journal_df, "journal_ranks.csv", row.names = FALSE)

# we really only need the pcoutrot_1
journal_df <- journal_df[order(-journal_df$pcoutrot_1), ]

#### Calcualting mean eigen scores for authors #####

another_df <- merge(papers2journals, journal_df, by = "JournalId")

authors_df <- merge(another_df, authors, by = "AuthorId")

authors_df <- authors_df %>%
  group_by(AuthorId) %>%
  summarise(eigen_mean = mean(eigen), prank_mean = mean(prank.vector),
            n = n(), degree_mean = mean(degree), pca_mean = mean(pcoutrot_1))

eig <- ggplot(authors_df, aes(x = eigen_mean)) +
              geom_density() + ggtitle("Author Mean Eigen")

prank <- ggplot(authors_df, aes(x = prank_mean)) +
                geom_density() + ggtitle("Authors Mean Page Rank")

deg <- ggplot(authors_df, aes(x = degree_mean)) +
              geom_density() + ggtitle("Author Mean Degree")

articles <- ggplot(authors_df, aes(x = n)) +
                    geom_density() + ggtitle("Author NUmber of Articles")

pca <- ggplot(authors_df, aes(x = pca_mean)) +
              geom_density() + ggtitle("Author Mean PCA")

all.g <- ggpubr::ggarrange(eig, prank, deg, articles, pca)

ggsave("figures/author_scores.pdf", all.g)

#### HISTOGRAMS #####

eig <- ggplot(authors_df, aes(x = eigen_mean)) +
              geom_histogram() + ggtitle("Author Mean Eigen")

prank <- ggplot(authors_df, aes(x = prank_mean)) +
                geom_histogram() + ggtitle("Authors Mean Page Rank")

deg <- ggplot(authors_df, aes(x = degree_mean)) +
              geom_histogram() + ggtitle("Author Mean Degree")

articles <- ggplot(authors_df, aes(x = n)) +
                   geom_histogram() + ggtitle("Author Number of Articles")

pca <- ggplot(authors_df, aes(x = pca_mean)) + geom_histogram() + ggtitle("Author Mean PCA")

all.g <- ggpubr::ggarrange(eig, prank, deg, articles, pca)

ggsave("figures/author_scores_hist.pdf", all.g)

#### Journals ######

ggplot(journal_df, aes(x = eigen)) + geom_density()

ggplot(journal_df, aes(x = prank.vector)) + geom_density()

ggplot(journal_df, aes(x = degree)) + geom_density()

ggplot(journal_df, aes(x = pcoutrot_1)) + geom_density()
