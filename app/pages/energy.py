import dash
from dash import Dash, html, dcc
from energy import viz

dash.register_page(__name__)

def layout():
    (efig, gfig) = viz.consumption_graphs()

    return html.Div(children=[
        dcc.Graph(
            id='electricity-graph',
            figure=efig
        ),
        
        dcc.Graph(
            id='gas-graph',
            figure=gfig
        )
    ])


