import csv
import argparse
import os
from ddlgenerator.ddlgenerator import Table
import logging

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

# read in data within file
with open(args.inputFile) as csvfile:
    ls = []
    filereader = csv.DictReader(csvfile, delimiter = args.delim, quotechar = args.quotechar)
    for row in filereader:
        ls.append(row)

# notify how many rows and columns we;ve got
print("--read " + str(len(ls)) + " rows from " + str(len(ls[0])) + " columns in " + args.inputFile)

# generate sql using ddlgenerator
table = Table(ls, args.tablename) 
sql = table.sql(args.dialect, inserts = args.addinserts)

# write or print out the sql file
if args.outputfile is None:
    print(sql)
else:
    f = open(args.outputfile, "w+")
    f.write(sql)
    f.close()

# if log file is empty then can delete
if os.stat(args.logfile).st_size == 0:
    os.remove(args.logfile)
else:
    print("**log file has content**")
