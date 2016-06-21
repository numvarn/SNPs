#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import numpy
import random
import time
import math
from csvSNPsAgent import csvSNPsAgent

def generateNewSNPs(genotypes, dis_snp_pos):
    x_spec = 0
    prob = 0
    alpha = 0.0
    gene_effect = 0.0
    disease = 0

    random.seed(time.time())
    sample1 = random.randint(0, len(genotypes)-1)
    sample2 = random.randint(0, len(genotypes)-1)

    while sample1 == sample2:
        sample2 = random.randint(0, len(genotypes)-1)

    x_spec = genotypes[sample1][dis_snp_pos] + genotypes[sample2][dis_snp_pos]

    # Find probabiliy value using logistic regression
    exp_value = math.exp(alpha + (gene_effect * x_spec))
    prob = exp_value / (1 + exp_value)

    # Random one number [0...1] by using uniform random
    runif = numpy.random.uniform(0,1,1)

    if runif[0] < prob:
        disease = 1
    else:
        disease = 0

    # Create new genotypes form original data (a + b)
    new_genotypes = [x + y for x, y in zip(genotypes[sample1], genotypes[sample2])]

    return disease, new_genotypes

def main():
    outfile = '../result/'+str(time.time())+'.csv'
    individual_size = 3008
    number_of_snp = 13479
    dis_snp = 'rs3789038'

    number_of_population = 1000
    number_of_case = number_of_population / 2
    all_data = numpy.zeros((number_of_population, number_of_snp + 1), dtype=numpy.int)

    all_data_index = 0
    case_index = 0
    control_index = number_of_case

    # Read Data form CSV file
    csvAgent = csvSNPsAgent()

    snpsName = csvAgent.readSNPsName()
    genotypes = csvAgent.readSNPsData(individual_size, number_of_snp)

    # Find position of snp name 'rs3789038'
    dis_snp_pos = snpsName.index(dis_snp)

    # Iterative generate 'Case' and 'Control' genotypes
    while case_index < number_of_case or control_index < number_of_population:
        disease = 0
        all_data_index = -1
        new_genotypes = []

        # Generate new genotypes form real data
        disease, new_genotypes = generateNewSNPs(genotypes, dis_snp_pos)

        # Combine Y value (label) and new genotypes
        # By add Y value into index 0 of list
        new_genotypes.insert(0, disease)

        # Classify genotypes between 'Case' and 'Control'
        # Disease = 1 is 'Case'
        # Disease = 0 is 'Control'
        if disease == 1 and case_index < number_of_case:
            all_data_index = case_index
            case_index += 1
        elif disease == 0 and control_index < number_of_population:
            all_data_index = control_index
            control_index += 1

        # Stroe new genotype into all_data
        # AllData[individual][genotypes]
        if all_data_index != -1:
            all_data[all_data_index] = new_genotypes

    # Write all_data to CSV file
    csvAgent.writeAllDataToCSV(outfile, all_data, number_of_snp)

if __name__ == '__main__':
    main()






