import datetime
import pandas as pd

from config import db
from log import log

def expensesByCategory(transactions):
    expbycat = transactions[['Category','Value']].groupby('Category',as_index=False).sum()
    expbycat = expbycat.loc[~expbycat['Category'].isin(db.getNonExpenseCategories())]
    expbycat['Value'] *= -1
    log.debug(expbycat)
    return expbycat;
