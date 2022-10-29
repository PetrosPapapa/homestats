import sys, os
import re
import csv
import config

def categorize(item, regexes):
    for index, row in regexes.iterrows():
        if re.match(row["regex"], item):
            return row["category"]
    return "UNKNOWN"

if __name__ == '__main__':
    regexes = config.db.getCategoryRegexes()
    print([(i, categorize(i, regexes)) for i in sys.argv[1:]])
