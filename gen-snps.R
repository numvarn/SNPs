# Code by Phisan Sookkhee and Sirikanlaya Sookkhee

# Funciton for generate only one new genotype
# @param genotype : matrix for store genotype data from CSV file
# @param dis_snp_pos : position of SNPs for predict 'Case' or 'Control'
# @return new_genotype
generateGenotype <- function(genotypes, dis_snp_pos) {
     # Generate new genotype from real data
     # @gen: Step 1 - random 2 samples form genotypes
     set.seed(as.numeric(Sys.time()))
     sample_total <- nrow(genotypes)
     samples_index <- sample(1:sample_total, 2, replace = T)

     # @gen: Step 2 - calculate x_spec
     x_spec <- as.numeric(genotypes[samples_index[1], dis_snp_pos]
                          + genotypes[samples_index[2], dis_snp_pos])

     # @gen: Step 3 - Find probabiliy value using logistic regression
     alpha <- 0.0
     gene_effect <- 0.0

     exp_value <- exp(alpha + (gene_effect * x_spec))
     prob <- exp_value / (1 + exp_value)

     # @gen: Step 4 - Using uniform random to cutoff \
     #                new genotype is 'Case' or 'Control'
     cutoff_value <- runif(1, 0, 1)
     if (cutoff_value < prob) {
          disease <- 1
     }else {
          disease <- 0
     }

     # @gen: Step 5 - create new Individual by add vector A and vector B together
     tmp_genotype <-
          genotypes[samples_index[1],] + genotypes[samples_index[2],]
     tmp_genotype <- as.list(tmp_genotype)

     # @gen: step 6 - insert disease or Y value into fist index of list
     new_genotype <- append(tmp_genotype, disease, 0)

     # @gen : step 7 - return only one new genotype
     return(new_genotype)
}

#--------------------------------------------------------------------
# Main Program

# Config values
setwd("~/ResearchCode/SNPsR")
snpsName_path <- "sourceFile/NameONLY13479.csv"
genotype_path <- "sourceFile/New_data_3008persons_13479SNPs.csv"
outfile <- paste("result/", format(Sys.time(), "%b-%d-%Y-%X"), ".csv", sep = "")

dis_snp = 'rs3789038'
number_of_population <- 1000
number_of_case <- number_of_population / 2

# Read input data from CSV files
snpsName_data <- read.csv(snpsName_path, header = TRUE)
genotypes_data <- read.csv(genotype_path, header = TRUE)

# Get number of SNPs from genotype data frame
snps_total <- ncol(genotypes_data)

# Convert snpsName data frame to vector
# And find SNPs position
snpsName <- snpsName_data[,1]
dis_snp_pos <- match(dis_snp, snpsName)

# Convert genotype data frame to matrix
genotypes <- data.matrix(genotypes_data)

# Create matrix for store 'Case' and 'Control'
# 1 - 500 : is a Case
# 501 - 1000 is a Control
all_data <- matrix(0, nrow = number_of_population, ncol = snps_total + 1)
case_index  <- 0
control_index <- number_of_case

while (case_index < number_of_case || control_index < number_of_population) {

     all_data_index <- -1

     # Call function generateGenotype
     # generateGenotype return new genotype as a List
     new_genotype <- generateGenotype(genotypes, dis_snp_pos)

     # Classify genotypes between 'Case' and 'Control' by using Y value
     # y_value = 1 is 'Case'
     # y_value = 0 is 'Control'
     y_value <- new_genotype[[1]]

     if (y_value == 1 && case_index < number_of_case) {
          case_index <- case_index + 1
          all_data_index <- case_index
     } else if (y_value == 0 &&
                control_index < number_of_population) {
          control_index <- control_index + 1
          all_data_index <- control_index
     }

     # Store new gentoype with Y value into all_data
     # and classify it is 'Case' or 'Control'
     if (all_data_index != -1) {
          for (i in 1:(snps_total + 1)) {
               all_data[all_data_index, i] <- new_genotype[[i]]
          }
     }
}

# Set header to first row of result matrix
colnames(all_data) <- c("Y value", paste("SNP", 1:snps_total))

# Write all data to CSV
write.csv(all_data, file = outfile, row.names = FALSE)
