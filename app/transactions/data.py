import datetime
import pandas as pd
import numpy as np

from config import db
from log import log

def expensesByCategory(transactions):
    expbycat = transactions[['Category','Value']].groupby('Category', as_index=False).sum()
    expbycat = expbycat.loc[~expbycat['Category'].isin(db.getNonExpenseCategories())]
    expbycat['Value'] *= -1
    log.debug("Expenses by category:")
    log.debug(expbycat)
    return expbycat;

def transactionsByMonth(transactions):
    transbymonth = transactions[['Date','Category','Value']]
    transbymonth['Date'] = transbymonth['Date'].apply(lambda x: x.strftime('%Y-%m'))
    return transbymonth;

def expensesByMonth(transByMonth):
    expbymonth = transByMonth.groupby(['Date','Category'], as_index=False).sum().round(2)
    expbymonth = expbymonth.loc[~expbymonth['Category'].isin(db.getNonExpenseCategories())]
    expbymonth['Value'] *= -1

    #expbymonth=expbymonth.set_index(['Date', 'Category']).unstack(1,fill_value=0)
    log.debug("Expenses by month:")
    log.debug(expbymonth)
    return expbymonth;

def balanceByMonth(transByMonth):
    balancebymonth = transByMonth.loc[~transByMonth['Category'].isin(['TRANSFER'])]
    balancebymonth = balancebymonth.groupby(['Date'], as_index=False).sum()

    # drop the most recent month as it will usually be incomplete
    balancebymonth = balancebymonth.drop(balancebymonth.index[len(balancebymonth) - 1])

    balancebymonth["Smooth"] = np.polyval(np.polyfit(
        range(len(balancebymonth['Date'])),
        balancebymonth['Value'].values, 
        5
    ), range(len(balancebymonth['Date'])))

    log.debug("Balance by month:")
    log.debug(balancebymonth)
    return balancebymonth;
