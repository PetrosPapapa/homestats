import os

from transactions.db import MockTransactionDB, MySQLTransactionDB
import dash

assets_path = os.getcwd() +'/app/assets'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder=assets_path)

#db=MySQLTransactionDB() 
db=MockTransactionDB()

