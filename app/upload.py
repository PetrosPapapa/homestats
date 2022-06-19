import appsecrets as ss

from config import app
from transactions.datatable import layout

if __name__ == '__main__':
    app.layout=layout
    app.run_server(debug=True, host=ss.host)
