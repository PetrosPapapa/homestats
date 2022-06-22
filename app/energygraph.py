import appsecrets as ss
import config

import dash
from dash import html, dcc

from energy import viz

if __name__ == '__main__':
    app = dash.Dash(__name__, 
                    external_stylesheets=config.external_stylesheets, 
                    assets_folder=config.assets_path,
                    )

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
    app.run_server(debug=True, host=ss.host)
