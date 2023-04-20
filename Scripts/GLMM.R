# Load the necessary packages
library(lme4)
library(lmerTest)
library(ggplot2)

# Load the data
data <- read.csv("~/Library/CloudStorage/OneDrive-UniversityofOklahoma/Shared_Dongyu/wetland_soil_project/Data/GLMM_1.csv")

# Create a new column to specify the treatment type for each observation
treatment <- rep(c("N", "S", "O", "B"), length.out = nrow(data))
data$treatment <- factor(treatment)

# Create a new column to specify the replicate number for each observation
replicate <- rep(1:3, each = 4, length.out = nrow(data))
data$replicate <- factor(replicate)

# Convert the data to long format for analysis
library(tidyr)
data_long <- pivot_longer(data, cols = -c(species, treatment, replicate), names_to = "treatment_replicate", values_to = "response")

# Extract treatment and replicate information from the treatment_replicate column
data_long$treatment <- gsub("_.*", "", data_long$treatment_replicate)
data_long$replicate <- gsub(".*_", "", data_long$treatment_replicate)

# Convert replicate to a factor variable
data_long$replicate <- factor(data_long$replicate)

# Define the control and treatment levels
control_level <- "N"
treatment_levels <- c("S", "O", "B")

# Update the treatment and control levels in the data
data_long$treatment <- factor(data_long$treatment, levels = c(control_level, treatment_levels))

# Fit the GLMM model with treatment as the fixed effect and replicate as the random effect
model <- glmer(response ~ treatment + (1 | replicate), data = data_long, family = poisson())

# View the summary of the model
summary(model)

# Perform an ANOVA test to compare the model with and without the fixed effect
model_null <- glmer(response ~ (1 | replicate), data = data_long, family = poisson())
anova(model_null, model)

# Get the estimated means for each treatment and replicate
treatments <- unique(data_long$treatment)
replicates <- unique(data_long$replicate)
means <- data.frame(treatment = character(), replicate = integer(), fit = numeric())
for (i in 1:length(treatments)) {
  for (j in 1:length(replicates)) {
    means <- rbind(means, data.frame(treatment = treatments[i], replicate = replicates[j], fit = predict(model, newdata = data.frame(treatment = treatments[i], replicate = replicates[j]), type = "response")))
  }
}

# Write the estimated means to a CSV file
write.csv(means, file = "estimated_means.csv", row.names = FALSE)

# Extract fixed effect coefficients and standard errors
coef_fixed <- fixef(model)
se_fixed <- sqrt(diag(vcov(model)))

# Create a data frame to store the coefficient estimates and standard errors
result <- data.frame(
  "Estimate" = coef_fixed,
  "Std. Error" = se_fixed,
  "z value" = coef_fixed / se_fixed,
  "Pr(>|z|)" = 2 * (1 - pnorm(abs(coef_fixed / se_fixed))),
  "coef_fixed" = coef_fixed
)

# Print the result
print(result)
