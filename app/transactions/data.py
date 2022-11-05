from datetime import timedelta
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

def accounts(transactions):
    accts = transactions[['Account Name','Account Number']].drop_duplicates() 
    result = pd.DataFrame({
        "label": accts['Account Name'] + ' - ' + accts['Account Number'],
        "value": accts['Account Number']
    }).reset_index(drop=True)
    return result;

def transactionsByMonth(transactions, firstDayOfMonth=17):
    transbymonth = transactions[['Date','Category','Value','Account Number']]
    transbymonth['Date'] = transbymonth['Date'].apply(lambda x: (x - timedelta(days=firstDayOfMonth-1)).strftime('%Y-%m'))
    return transbymonth;

def expensesByMonth(transByMonth, accounts=[]):
    if not accounts:
        trans = transByMonth
    else:
        trans = transByMonth[transByMonth['Account Number'].isin(accounts)]
    expbymonth = trans.groupby(['Date','Category'], as_index=False).sum().round(2)
    expbymonth = expbymonth.loc[~expbymonth['Category'].isin(db.getNonExpenseCategories())]
    expbymonth['Value'] *= -1

    #expbymonth=expbymonth.set_index(['Date', 'Category']).unstack(1,fill_value=0)
    log.debug("Expenses by month:")
    log.debug(expbymonth)
    return expbymonth;

def incomeByMonth(transByMonth):
    inbymonth = transByMonth.loc[transByMonth['Category'].isin(["INCOME"])]
    inbymonth = inbymonth.groupby(['Date'], as_index=False).sum().round(2)
    inbymonth = inbymonth.rename(columns={"Value": "Income"})

    #expbymonth=expbymonth.set_index(['Date', 'Category']).unstack(1,fill_value=0)
    log.debug("Income by month:")
    log.debug(inbymonth)
    return inbymonth;

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

def cumBalanceByMonth(transByMonth):
    cumbalancebymonth = transByMonth.loc[~transByMonth['Category'].isin(['TRANSFER'])]
    cumbalancebymonth = cumbalancebymonth.groupby(['Date']).sum().cumsum().reset_index()

    # drop the most recent month as it will usually be incomplete
    cumbalancebymonth = cumbalancebymonth.drop(cumbalancebymonth.index[len(cumbalancebymonth) - 1])

    cumbalancebymonth["Smooth"] = np.polyval(np.polyfit(
        range(len(cumbalancebymonth['Date'])),
        cumbalancebymonth['Value'].values, 
        5
    ), range(len(cumbalancebymonth['Date'])))


    log.debug("Cumulative balance by month:")
    log.debug(cumbalancebymonth)
    return cumbalancebymonth;
