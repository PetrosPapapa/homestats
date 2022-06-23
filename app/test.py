import sys

import appsecrets as ss
import config

import dash
from dash import html, dcc

from energy import viz, meter
from transactions import upload

if __name__ == '__main__':
    app = dash.Dash(__name__, 
                    external_stylesheets=config.external_stylesheets, 
                    assets_folder=config.assets_path,
                    suppress_callback_exceptions=True
                    )

    args=sys.argv
    if len(args) < 2 or args[1] == "energy":
        (efig, gfig) = viz.consumption_graphs()

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
    else:
        app.layout=html.Div("Unknown parameter")

    app.run_server(debug=True, host=ss.host)
