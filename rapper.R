setwd("/Users/lukelorenz/Desktop/IndependentProjects/2021/Rappa/")
print(getwd())

rapperList <- read.csv("names.csv", quote="")

# rapperList[ncol(rapperList) + 1,] = c("v1","v2")


library("ggplot2")
library(dplyr)
library(tidyr)
library(forcats)
install.packages("ggridges")
library("ggridges")

# test = separate(rapperList, c('Name', "Vocab"))

ggplot(data = rapperList) + 
  geom_density(mapping = aes(x=Vocab, group=Era, fill=Era),alpha=0.6) +
  theme(axis.text.x = element_text(angle = 35, vjust = 1, hjust = 1), strip.text.x = element_text(size = 5)) +
  scale_fill_manual(values=c("#FF1700", "#FF8E00", "#FFE400", "#06FF00"))

ggplot(rapperList, aes(x = Vocab, y = Era)) +
  geom_density_ridges(aes(fill = Era)) +
  scale_fill_manual(values = c("#FF1700", "#FF8E00", "#FFE400", "#06FF00")) +
  theme(legend.position = "none") + 
  scale_y_discrete(limits=rev) +
  xlab("Unique Vocabulary (words) in first 20,000 Words") + ylab("Era")


rapperList %>%
  mutate(Artist = fct_reorder(Artist, Vocab)) %>%
  ggplot( aes(x=Artist, y=Vocab)) +
  geom_bar(stat="identity", fill="#f68060", alpha=.6, width=.4) +
  coord_flip() +
  xlab("") +
  theme_bw() + 
  theme(axis.text.x = element_text(angle = 35, vjust = 1, hjust = 1), strip.text.x = element_text(size = 5),
        axis.text.y= element_text(size = 4, vjust = 1, hjust = 1))

