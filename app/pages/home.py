import dash
from dash import Dash, html, dcc
from energy import viz

dash.register_page(__name__, path="/")

layout=html.H1("Welcome to the homestats page!", style={ "text-align": "center"})
