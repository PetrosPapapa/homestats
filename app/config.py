import os

from db import MockDB, MySQL

assets_path = os.getcwd() + '/app/assets'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

db=MySQL() 
#db=MockDB()

