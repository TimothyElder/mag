library(tidyverse)
library(network)
library(sna)

setwd("/Users/timothyelder/Documents/mag")

journal_df <- read.csv("data/trunc_journal_ranks.csv")

authors <- read.csv("data/authors.csv")

key <- read.csv("data/key_faculty2authors.csv")

key <- key %>% select(faculty_name, network_name, AuthorId, NormalizedName)

authors <- unique(authors)

authors2papers2journals <- read.csv("data/edge_list.csv")
authors2journals <- authors2papers2journals %>% select(JournalId, AuthorId)
papers2journals <- authors2papers2journals %>% select(JournalId, PaperId)

authors <- authors %>%
  select(NormalizedName, AuthorId)

journal_names <- read.csv("data/journals.csv")

journal_df = merge(x = journal_names, y = journal_df, by=c("NormalizedName", "JournalId"), all=TRUE)

journal_df[is.na(journal_df)] <- 0

##### Calcualting mean eigen scores for authors ######

authors_df <- merge(authors2papers2journals, journal_df, by = "JournalId")

authors_df <- authors_df %>%
  group_by(AuthorId) %>%
  summarise(eigen_mean = mean(eigen), prank_mean = mean(prank.vector),
            n = n(), degree_mean = mean(degree), pca_mean = mean(pcoutrot_1), pcsqrt = mean(pcoutrot_sqrt))

authors_df <- merge(authors_df, authors, by = "AuthorId")

df <- merge(x=authors_df, y=key, by=c("NormalizedName", "AuthorId"), all.x=TRUE)

df <- unique(df)


authors_df <- authors_df %>% subset(pca_mean >= .02)

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

pcsrt <- ggplot(authors_df, aes(x = pcsqrt)) +
  geom_density() + ggtitle("Author Mean PCA")

all.g <- ggpubr::ggarrange(eig, prank, deg, articles, pca, pcsrt)

all.g

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
