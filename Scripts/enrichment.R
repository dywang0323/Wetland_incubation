# Load necessary libraries
library(dplyr)
library(tidyr)
library(clusterProfiler)

# Load data
data <- read.csv("~/Library/CloudStorage/OneDrive-UniversityofOklahoma/Shared_Dongyu/wetland_soil_project/Data/enrichment.csv", header = TRUE)

# Reshape the data to long format
data_long <- data %>%
  pivot_longer(cols = -KO.Number, names_to = c("Treatment", ".value"), names_sep = "_")

# Run enrichment analysis
result <- enrichKEGG(gene = data_long$KO.Number, organism = "ko", pvalueCutoff = 0.05)

# Visualize the result as a dotplot
dotplot(result)
