library(vegan)
library(magrittr)
library(ggplot2)
library(tidyverse)

Taxa <- read.csv("/Volumes/Nascell/Figures_soil_incubation/Taxa.csv")
Taxa %>%
  group_by(Group) %>%
  summarize(sobs = specnumber(Value),
            shannon = diversity(Value, index = "shannon"),
            simpson = diversity(Value, index = "simpson"),
            pielou =shannon/log2(length(Value)),
            invsimpson = 1/simpson,
            n=sum(Value)) %>%
pivot_longer(cols=c(sobs, shannon, invsimpson, simpson),
            names_to ="metric") %>%
  ggplot(aes(x=n, y=value)) + 
  geom_point() +
  geom_smooth() +
  facet_wrap(~metric, nrow=4, scales="free_y")
