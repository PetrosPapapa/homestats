import appsecrets as ss

from config import app
from dash import html

from transactions.datatable import layout
from menu import layout as menu


if __name__ == '__main__':
    app.layout=html.Div([
        menu,
        layout
    ])
    app.run_server(debug=True, host=ss.host)
