import dash
from transactions import upload

dash.register_page(__name__, order=4)

layout=upload.layout
