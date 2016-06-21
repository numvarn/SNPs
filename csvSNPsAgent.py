#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import numpy

class csvSNPsAgent():
    """docstring for csvSNPsAgent"""
    def __init__(self):
        pass

    def readSNPsName(self):
        snpsName = []
        row_count = 0
        with open("../sourceFile/NameONLY13479.csv", "rb") as f:
            rows = csv.reader(f)
            for row in rows:
                if row_count > 0:
                    snpsName.append(row[0])
                row_count += 1

        return snpsName

    def readSNPsData(self, individual_size, number_of_snp):
        genotypes = numpy.zeros((individual_size, number_of_snp), dtype=numpy.int)
        row_count = 0
        with open("../sourceFile/New_data_3008persons_13479SNPs.csv", "rb") as f:
            rows = csv.reader(f)
            for row in rows:
                if row_count > 0:
                    for index in xrange(0, len(row)):
                        genotypes[row_count-1][index] = int(row[index])
                row_count += 1

        return genotypes

    # Write 'Case' and 'Control' to CSV
    # @param outfile is output file path
    # @param AllData[individual][genotypes] is metrix or 2D array
    def writeAllDataToCSV(self, outfile, all_data, number_of_snp):
        with open(outfile, 'a') as csvfile:
            # Write file header
            header = []
            header.append("Y Value")
            for index in range(1, number_of_snp+1):
                header.append("SNP"+str(index))
            newline = ",".join(header)+"\n"
            csvfile.write(newline)

            # Write file content
            for row in all_data:
                newline = ",".join(str(x) for x in row)+"\n"
                csvfile.write(newline)


