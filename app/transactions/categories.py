import sys, os
import re
import csv
import config

reader = csv.reader(open(os.path.join(config.__location__,'transactions/categories.csv'),'r'), delimiter=',', quotechar="\"")
reader_rows = [(row[0], row[1]) for row in reader if len(row)==2]

def categorize_from_rows(item, rows):
    for (cat, regex) in rows:
        if re.match(regex, item):
            return cat
    return "UNKNOWN"

def categorize(item):
    return categorize_from_rows(item, reader_rows)

if __name__ == '__main__':
    print([(i, categorize(i)) for i in sys.argv[1:]])
