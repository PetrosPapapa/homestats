import config
import appsecrets as ss

import sys

import dash
from dash import html, dcc

from energy import meter, viz as eviz
from transactions import upload, data as tdata, viz as tviz

if __name__ == '__main__':
    app = dash.Dash(__name__, 
                    external_stylesheets=config.external_stylesheets, 
                    assets_folder=config.assets_path,
                    suppress_callback_exceptions=True
                    )

    args=sys.argv
    if len(args) < 2 or args[1] == "energy":
        (efig, gfig) = eviz.consumption_graphs()

        app.layout=html.Div(children=[
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
    elif args[1] == "upload":
        app.layout=upload.layout
    elif args[1] == "meter":
        app.layout=meter.form
    elif args[1] == "transactions":
        transactions=config.db.getTransactions()
        transactionsByMonth=tdata.transactionsByMonth(transactions)
        app.layout=html.Div(children=[
            html.H1(children='Transactions'),
            
            dcc.Graph(
                id='category_pie',
                figure=tviz.category_pie(transactions)
            ),

            dcc.Graph(
                id='month_bars',
                figure=tviz.month_bars(transactionsByMonth)
            ),
            
        ])
    else:
        app.layout=html.Div("Unknown parameter")

    app.run_server(debug=True, host=ss.host)
