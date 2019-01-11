import csv
import argparse
import os
from ddlgenerator.ddlgenerator import Table

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("inputFile", help = "path to data file")
parser.add_argument('-d', '--delim', default = ',', help = "delimiter for file (use tsv for tab)")
parser.add_argument('-q', '--quotechar', default = '"', help = "quote character used in data file")
parser.add_argument('-i', '--addinserts', default = False, help = "should insert statements be generated")
parser.add_argument('-o', '--outputfile', help = "filename for output file")
parser.add_argument('-l', '--dialect', default = 'postgresql', help = "database dialect to be used")
parser.add_argument('-t', '--tablename', help = "name of the table to generate")
args = parser.parse_args()


try:
    if args.outputfile is None:
        args.outputfile = os.path.splitext(args.inputFile)[0] + '.sql'
    if args.delim == 'tsv':
        args.delim = '\t'
    if args.tablename is None:
        args.tablename = os.path.basename(os.path.splitext(args.inputFile)[0])

except Exception as err:
    print('Error processing arguments' + err)

ls = []
with open(args.inputFile) as csvfile:
    filereader = csv.reader(csvfile, delimiter = args.delim, quotechar = args.quotechar)
    line_count = 0
    for row in filereader:
        if line_count == 0:
            keys = row
            line_count += 1
        else:
            ls.append(dict(zip(keys, row)))
            line_count += 1
            print("--read line " + str(line_count + 1))

with open('dbo_R_CLL210_Baseline1.txt') as csvfile:
    filereader = csv.DictReader(csvfile, delimiter = '\t')
    for row in filereader:
        ls.append(row)

with open('dbo_R_CLL210_Baseline1.txt') as csvfile:
    filereader = csv.reader(csvfile, delimiter = '\t')
    line_count = 0
    for row in filereader:
        if line_count == 0:
            keys = row
            line_count += 1
        else:
            ls.append(dict(zip(keys, row)))
            line_count += 1
            print("--read line " + str(line_count + 1))

print("--read " + str(len(ls)) + " rows from " + str(len(ls[0])) + " columns in " + args.inputFile)

table = Table(ls, args.tablename) 
sql = table.sql(args.dialect, inserts = args.addinserts)

f = open(args.outputfile, "w+")
f.write(sql)
f.close()
