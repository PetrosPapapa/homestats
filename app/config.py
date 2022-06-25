import sys,os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(__location__)

from db import MockDB, MySQL

assets_path = os.path.join(__location__, 'assets')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

db=MySQL() 
#db=MockDB()

