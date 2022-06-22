from dash import Dash, html, dcc
import plotly.express as px
from energy import data

def layout():
    (ele, gas) = data.energiesPerMonth()

    efig = px.bar(ele, barmode="group", title="Electricity")
    gfig = px.bar(gas, barmode="group", title="Gas")

    return html.Div(children=[
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
