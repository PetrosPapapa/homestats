import dash
from dash import Dash, html, dcc
from energy import viz, meter

dash.register_page(__name__)

def layout():
    (efig, gfig) = viz.consumption_graphs()

    return html.Div(children=[
        meter.form(),
        html.Hr(),

        dcc.Graph(
            id='electricity-graph',
            figure=efig
        ),
        
        dcc.Graph(
            id='gas-graph',
            figure=gfig
        )
    ])


