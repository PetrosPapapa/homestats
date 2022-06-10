import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State, MATCH
from dash import dcc, html, dash_table
from dash.dash_table.Format import Format, Group, Scheme, Symbol
from dash.exceptions import PreventUpdate

import pandas as pd

import appsecrets as ss
from transactions import categorize

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

expected_columns = ["Date", "Type", "Description", "Value", "Balance", "Account Name", "Account Number"]
categories = ["UNKNOWN", "A", "B", "C"]

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
    actual_columns = list(df.columns.values)
    if (expected_columns != actual_columns):
        raise InvalidTransactionFile("Invalid columns: " + str(actual_columns) + " - need: " + str(expected_columns) )

    # Strip "balance" rows
    df = df[df["Type"].notna()]

    # Format date
    df["Date"] = df["Date"].dt.date # see https://community.plotly.com/t/datatable-datetime-format/31091/8
    
    # Sort by date
    # df = df.sort_values(by=["Date"], ascending=True)

    # Add category
    df['Category'] = "UNKNOWN"

    return df

def parse_contents(index, contents, filename):
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
        html.H6(str(df.shape[0]) + " rows"),

        html.Button('Select All', id={'type': 'select-all-button', 'index': index}, n_clicks=0),
        html.Button('Deselect All', id={'type': 'deselect-all-button', 'index': index}, n_clicks=0),
        dcc.Dropdown(
            id={'type': "category_dropdown", 'index': index},
            options=[{"label": st, "value": st} for st in categories],
            placeholder="-Set the Category-",
        ),

        dash_table.DataTable(
            id={'type': 'transaction_table', 'index': index},
            data=df.to_dict('records'),
            columns= #[{'name': i, 'id': i} for i in ['Date', 'Account Name', 'Type', 'Description', 'Value']],
            [
                dict(id='Date', name='Date', type='datetime'),
                dict(id='Account Name', name='Account Name', hideable=True),
                dict(id='Account Number', name='Account Number'),
                dict(id='Type', name='Type', hideable=True),
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
                     ),
                dict(id='Balance', name='Balance', hideable=True),
                dict(id='Category', name='Category', editable=True, presentation= 'dropdown')
            ],

            style_cell_conditional=[
                {"if": {"column_id": c}, "textAlign": "left"} for c in ['Description', 'Type', 'Account Name', 'Account Number']
            ] + [
                {"if": {"column_id": c}, "textAlign": "center"} for c in ['Category']
            ],

            sort_action='native',
            sort_by=[dict(column_id='Date', direction='asc')],
            hidden_columns=['Account Name', 'Balance'],
            filter_action='native',
            row_selectable="multi",

            dropdown={
                'Category': {
                    'options': [
                        {'label': i, 'value': i} for i in categories
                    ],
                    'clearable': False
                }
            }
        ),
        html.Hr(),  # horizontal line
        html.Div(categorize("barbar"))
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(i, c, n) for i, c, n in
            zip(list(range(0,len(list_of_contents))), list_of_contents, list_of_names)]
        return children


# see https://stackoverflow.com/questions/61905396/dash-datatable-with-select-all-checkbox
# but updated for pattern-matching callback
@app.callback(
    [Output({'type': 'transaction_table', 'index': MATCH}, 'selected_rows')],
    [
        Input({'type': 'select-all-button', 'index': MATCH}, 'n_clicks'),
        Input({'type': 'deselect-all-button', 'index': MATCH}, 'n_clicks')
    ],
    [
        State({'type': 'transaction_table', 'index': MATCH}, 'data'),
        State({'type': 'transaction_table', 'index': MATCH}, 'derived_virtual_data'),
        State({'type': 'transaction_table', 'index': MATCH}, 'derived_virtual_selected_rows')
    ]
)
def select_all(select_n_clicks, deselect_n_clicks, original_rows, filtered_rows, selected_rows):
    ctx = [*dash.callback_context.triggered_prop_ids.values()]
    if not ctx:
        raise PreventUpdate
    ctx_caller = ctx[0]['type']
    if filtered_rows is not None:
        if ctx_caller == 'select-all-button':
            selected_ids = [row for row in filtered_rows]
            return [[i for i, row in enumerate(original_rows) if row in selected_ids]]
        if ctx_caller == 'deselect-all-button':
            return [[]]
        raise PreventUpdate
    else:
        raise PreventUpdate


def update_category(category, selected, rowid, row):
    if rowid in selected:
        row.update({'Category': category})
        return row
    else:
        return row

@app.callback(
    Output({'type': 'transaction_table', 'index': MATCH}, "data"), 
    Input({'type': "category_dropdown", 'index': MATCH}, "value"),
    State({'type': 'transaction_table', 'index': MATCH}, 'derived_virtual_selected_rows'),
    State({'type': 'transaction_table', 'index': MATCH}, 'data')
)
def set_category(category, selected, original):
    if selected is None:
        raise PreventUpdate
    if not category:
        raise PreventUpdate
    return [update_category(category, selected, i, r) for i,r in enumerate(original)]


if __name__ == '__main__':
    app.run_server(debug=True, host=ss.host)
