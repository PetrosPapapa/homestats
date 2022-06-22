import appsecrets as ss

from config import app
from dash import html

from energy import viz

server=app.server

if __name__ == '__main__':
    app.layout=html.Div([
        viz.layout()
    ])
    app.run_server(debug=True, host=ss.host)
