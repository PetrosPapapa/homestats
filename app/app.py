import config
import appsecrets as ss

import dash
from dash import html

app = dash.Dash(__name__, 
                external_stylesheets=config.external_stylesheets, 
                assets_folder=config.assets_path,
                use_pages=True,
                )

server = app.server 

from menu import layout as menu

app.layout=html.Div([
    menu,
    dash.page_container
])



if __name__ == '__main__':
    app.run_server(debug=True, host=ss.host)
