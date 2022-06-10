import sys
import re
import csv

reader = csv.reader(open('app/transactions/categories.csv','r'), delimiter=',', quotechar="\"")
reader_rows = [(row[0], row[1]) for row in reader]

def categorize_from_rows(item, rows):
    for (cat, regex) in rows:
        if re.match(regex, item):
            return cat
    return "UNKNOWN"

def categorize(item):
    return categorize_from_rows(item, reader_rows)

if __name__ == '__main__':
    print([(i, categorize(i)) for i in sys.argv[1:]])
