# Load the necessary packages
library(lme4)
library(lmerTest)
library(ggplot2)


# Load the data
data <- read.csv("~/Library/CloudStorage/OneDrive-UniversityofOklahoma/Shared_Dongyu/wetland_soil_project/Data/GLMM_1.csv")

# Create a new column to specify the treatment type for each observation
treatment <- rep(c("N", "S", "B", "O"), each = 3*length(unique(data$species)))

data$treatment <- factor(treatment)

# Create a new column to specify the replicate number for each observation
replicate <- rep(1:3, each = length(unique(data$species)), times = 4)
data$replicate <- factor(replicate)

# Convert the data to long format for analysis
library(tidyr)
data_long <- pivot_longer(data, cols = -c(species, treatment, replicate), names_to = "replicate_num", values_to = "response")

# Fit the GLMM model with treatment as the fixed effect and replicate as the random effect
model <- glmer(response ~ treatment + (1 | replicate), data = data_long, family = poisson())

# View the summary of the model
summary(model)

# Perform an ANOVA test to compare the model with and without the fixed effect
model_null <- glmer(response ~ (1 | replicate), data = data_long, family = poisson())
anova(model_null, model)

# Get the estimated means for each treatment and replicate
treatments <- unique(data$treatment)
replicates <- unique(data$replicate)
means <- data.frame(treatment = character(), replicate = integer(), fit = numeric())
for (i in 1:length(treatments)) {
  for (j in 1:length(replicates)) {
    means <- rbind(means, data.frame(treatment = treatments[i], replicate = replicates[j], fit = predict(model, newdata = data.frame(treatment = treatments[i], replicate = replicates[j]), type = "response")))
  }
}

# Plot the estimated means
ggplot(means, aes(x=treatment, y=fit, fill=factor(replicate))) + 
  geom_bar(stat="identity", position=position_dodge()) + 
  ylab("Estimated Mean") + xlab("Treatment")
