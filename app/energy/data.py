from config import db
import datetime
import pandas as pd

def energiesPerMonth():
    readings=db.getEnergyData()
    columns = ['year', 'month', 'electricity', 'gas']
    data = []
    prow = []
    
    for index, row in readings.iterrows():
        if (index > 0):
            start_date = prow["date"] + datetime.timedelta(days=1)
            end_date = row["date"]
            daterange = pd.date_range(start_date, end_date)
            days = (end_date - start_date).days + 1
            while (row["electricity"] < prow["electricity"]):
                row["electricity"] = row["electricity"] + 100000
            ele = (row["electricity"] - prow["electricity"]) / days
            gas = (row["gas"] - prow["gas"]) / days
            for single_date in daterange:
                data.append(dict([
                    ("year", single_date.strftime('%Y')),
                    ("month", single_date.strftime('%m')),
                    ("electricity", ele),
                    ("gas", gas)
                ]))
        prow = row
    
    perday = pd.DataFrame(columns=columns, data=data)

    epermonth = perday.drop('gas', 1)
    epermonth = epermonth.groupby(['month', 'year']).sum()
    epermonth = epermonth.reset_index().pivot('month', 'year', 'electricity')

    gpermonth = perday.drop('electricity', 1)
    gpermonth = gpermonth.groupby(['month', 'year']).sum()
    gpermonth = gpermonth.reset_index().pivot('month', 'year', 'gas')

    return (epermonth, gpermonth)
