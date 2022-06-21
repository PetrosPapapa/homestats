import appsecrets as ss

from transactions.datatable import app
from menu import layout as menu
from dash import html

if __name__ == '__main__':
    app.layout=html.Div([
        menu,
        app.layout
    ])
    app.run_server(debug=True, host=ss.host)
