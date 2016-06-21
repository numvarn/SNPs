#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

def main():
    infile = './1466437236.41.csv'
    with open(infile, "rb") as f:
        rows = csv.reader(f)
        control = 0
        case = 0
        row_count = 0
        for row in rows:
            if row_count > 0:
                if int(row[0]) == 1:
                    case += 1
                elif int(row[0]) == 0:
                    control += 1
            row_count += 1

        print "Case : ", case
        print "Control : ", control

if __name__ == '__main__':
    main()
