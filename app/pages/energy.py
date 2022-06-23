import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output

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

@callback(
    Output('electricity-graph', 'figure'),
    Output('gas-graph', 'figure'),
    Input('meter-output', 'children'),
    prevent_initial_call=True,
)
def update_graphs(value):
    return viz.consumption_graphs()
    
