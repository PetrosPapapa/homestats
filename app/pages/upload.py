import dash
from transactions import upload

dash.register_page(__name__)

layout=upload.layout
