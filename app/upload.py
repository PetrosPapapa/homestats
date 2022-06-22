import appsecrets as ss
import config

import dash
from dash import html

from transactions.upload import layout
#from menu import layout as menu

app = dash.Dash(__name__, 
                external_stylesheets=config.external_stylesheets, 
                assets_folder=config.assets_path,
                )

if __name__ == '__main__':   
    app.layout=html.Div([
 #       menu,
        layout
    ])
    app.run_server(debug=True, host=ss.host)
