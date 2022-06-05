import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import appsecrets as ss

engine = create_engine(f'mysql+pymysql://{ss.db["username"]}:{ss.db["password"]}]@{ss.db["host"]}:{ss.db["port"]}/{ss.db["database"]}', pool_recycle=3600) #, echo=True)
Base = declarative_base(engine)


########################################################################
class Energy(Base):
    """"""
    __tablename__ = 'energy'
    __table_args__ = {'autoload': True}
# ----------------------------------------------------------------------


def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def getData():
    session = loadSession()
    qry = session.query(Energy).filter(Energy.address == ss.energy["address"]).order_by(Energy.date.asc())
    readings = pd.read_sql(qry.statement, engine)

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


external_stylesheets = []  # 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

(ele, gas) = getData()

efig = px.bar(ele, barmode="group", title="Electricity")
gfig = px.bar(gas, barmode="group", title="Gas")

app.layout = html.Div(children=[
    html.H1(children='Energy Consumption'),

    dcc.Graph(
        id='electricity-graph',
        figure=efig
    ),

    dcc.Graph(
        id='gas-graph',
        figure=gfig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host=ss.host)
