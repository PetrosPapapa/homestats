import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.dash_table.Format import Format, Group, Scheme, Symbol

import pandas as pd

import appsecrets as ss

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

class InvalidTransactionFile(Exception):
    pass


def parse_csv(content):
    df = pd.read_csv(
        content, 
        parse_dates=['Date'], 
        dayfirst=True,
        index_col=False,
        na_values=[''],
        skipinitialspace=True
    )

    # Check columns are as expected
    expected_columns = ["Date", "Type", "Description", "Value", "Balance", "Account Name", "Account Number"]
    actual_columns = list(df.columns.values)
    if (expected_columns != actual_columns):
        raise InvalidTransactionFile("Invalid columns: " + str(actual_columns) + " - need: " + str(expected_columns) )

    # Strip "balance" rows
    df = df[df["Type"].notna()]
    
    return df

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = parse_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            raise InvalidTransactionFile("Not a csv file")
    except Exception as e:
        err = "Error [" + filename + "]: " + str(e)
        print(err)
        return html.Div([
            err
        ])

    return html.Div([
        html.H4(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.H6(str(df.shape[0]) + " rows"),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns= #[{'name': i, 'id': i} for i in ['Date', 'Account Name', 'Type', 'Description', 'Value']],
            [
                dict(id='Date', name='Date'),
                dict(id='Account Name', name='Account Name'),
                dict(id='Type', name='Type'),
                dict(id='Description', name='Description'),
                dict(id='Value', name='Value', type='numeric', format=Format(
                    scheme=Scheme.fixed, 
                    precision=2,
                    group=Group.yes,
                    groups=3,
                    group_delimiter=',',
                    decimal_delimiter='.',
                    symbol=Symbol.yes, 
                    symbol_prefix=u'£')
                     )
            ],
            style_cell_conditional=[
                {"if": {"column_id": c}, "textAlign": "left"} for c in ['Description', 'Type', 'Account Name']
            ]
        ),

        html.Hr(),  # horizontal line
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True, host=ss.host)
