import os
import logging

from db import MockDB, MySQL

assets_path = os.getcwd() + '/app/assets'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#db=MySQL() 
db=MockDB()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
