import os
import logging

from db import MockDB, MySQL
import dash

assets_path = os.getcwd() + '/app/assets'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder=assets_path)

db=MySQL() 
#db=MockDB()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
