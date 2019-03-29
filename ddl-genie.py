"""
Given a data file in tabular format, automatically guess-generates a matching DDL.

e.g. python3 ddl-genie.py indata.csv -d , -t cohort_data -i

Will output the DDL to console (or specified output file) with/without insert statements

Supports various sql dialects (determined by what sqlalchemy can support)

Wrapper for ddlgenerator module (with minor alteration) https://github.com/catherinedevlin/ddl-generator

"""
import csv
import argparse
import os
from ddlgenerator.ddlgenerator import Table
import logging
import random

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("inputFile", help = "path to data file")
parser.add_argument('-d', '--delim', default = ',', help = "delimiter for file (use tsv for tab)")
parser.add_argument('-q', '--quotechar', default = '"', help = "quote character used in data file")
parser.add_argument('-i', '--addinserts', action = "store_true", help = "add insert statements")
parser.add_argument('-o', '--outputfile', help = "filename for output file")
parser.add_argument('-l', '--dialect', default = 'postgresql', help = "database dialect to be used")
parser.add_argument('-t', '--tablename', help = "name of the table to generate")
parser.add_argument('-g', '--logfile', help = "name of log file to write to")
parser.add_argument('-r', '--maxrows', help = "maximum number of (random) rows to use for ddl generation")
parser.add_argument('-w', '--tableowner', help = "name of the table owner")
#parser.add_argument('-k', '--primarykey', help = "column to make primary key")
args = parser.parse_args()

# assign some variables
try:
    if args.delim == 'tsv':
        args.delim = '\t'
    if args.tablename is None:
        args.tablename = os.path.basename(os.path.splitext(args.inputFile)[0])
    if args.logfile is None:
        args.logfile = os.path.splitext(args.inputFile)[0] + '.log'
except Exception as err:
    print('Error processing arguments' + err)

# set up logging from ddlgenerator to a specific file
logging.basicConfig(filename=args.logfile, filemode = 'w')

# function to get random sample (of length k) from the file
def randomsampler(filename, k, d, q):
    sample = []
    with open(filename, 'rU') as f:
        # get number of lines (excluding header)
        linecount = sum(1 for line in f) - 1
        k = min(k, linecount)
        # go back to top of file
        f.seek(0)
        filereader = csv.DictReader(f, delimiter = d, quotechar = q)
        # generate sorted random set of line numbers
        random_linenos = sorted(random.sample(range(linecount), k), reverse = True)
        # pop off a line
        lineno = random_linenos.pop()
        # work through each line and append to the output list if the line number is in the random set
        for n, line in enumerate(filereader):
            if n == lineno:
                sample.append(line)
                if len(random_linenos) > 0:
                    lineno = random_linenos.pop()
                else:
                    break
        print("--read " + str(len(sample)) + " random rows from " + str(len(sample[0])) + " columns in " + filename)
        return sample

# read in data within file
def readfullfile(filename, d, q):
    with open(filename, 'rU', encoding = 'utf-8-sig') as csvfile:
        filereader = csv.DictReader(csvfile, delimiter = d, quotechar = q)
        out = []
        for row in filereader:
            out.append(row)
        if len(out) > 0:
            print("--read " + str(len(out)) + " rows from " + str(len(out[0])) + " columns in " + filename)
            return out
        else:
            print("--no data to read in " + filename)
            deleteemptyfile(args.logfile)
            exit()

# delete empty file
def deleteemptyfile(filename):
    if os.path.isfile(filename) and os.stat(filename).st_size == 0:
        os.remove(filename)

# read in either full file or random 
if args.maxrows is None:
    ls = readfullfile(args.inputFile, args.delim, args.quotechar)
else:
    ls = randomsampler(args.inputFile, int(args.maxrows), args.delim, args.quotechar)

# generate sql using ddlgenerator
#if args.primarykey is None:
#    table = Table(ls, table_name = args.tablename) 
#else:
#    table = Table(ls, table_name = args.tablename, pk_name = args.primarykey)
table = Table(ls, table_name = args.tablename, table_owner = args.tableowner) 
sql = table.sql(args.dialect, inserts = args.addinserts)

# write or print out the sql file
if args.outputfile is None:
    print(sql)
else:
    f = open(args.outputfile, "w+")
    f.write(sql)
    f.close()

# if log file is empty then can delete
deleteemptyfile(args.logfile)
