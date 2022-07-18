import datetime

import dash
from dash.dependencies import Input, Output, State, MATCH
from dash import dcc, callback, html, dash_table
from dash.dash_table.Format import Format, Group, Scheme, Symbol
from dash.exceptions import PreventUpdate

import pandas as pd

from transactions import categorize
from transactions.parser import parse_file

from config import db

layout = html.Div([
    html.Div(
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '70px',
                'lineHeight': '70px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        id='upload-data-container'),
    html.Div(id='output-data-upload'),
])
    

def parse_contents(index, contents, filename):
    try:
        df = parse_file(filename, contents)
    except Exception as e:
        err = "Error [" + filename + "]: " + str(e)
        print(err)
        return html.Div([
            err
        ])
    
    categories = db.getCategories()
    unknowns = len(df[df['Category']=='UNKNOWN'])
        
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
                dict(id='Category', name='Category', editable=True) #, presentation= 'dropdown')
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
            # cell_selectable=False, # we can't even c/p if this is false

            #            dropdown={
            #                'Category': {
            #                    'options': [
            #                        {'label': i, 'value': i} for i in categories
            #                    ],
            #                    'clearable': False
            #                }
            #            }
        ),
        html.Hr(),  # horizontal line
        html.Button('SUBMIT', id={'type': 'transactions_submit', 'index': index}, n_clicks=0, disabled=(unknowns > 0)),
        html.Div('Unknowns remaining: {}'.format(unknowns), id={'type': 'unknown-counter', 'index': index}),
    ], id={'type': 'transaction_table_container', 'index': index})

@callback(
    Output('output-data-upload', 'children'),
    Output('upload-data-container', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'), 
    prevent_initial_call=True
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(i, c, n) for i, c, n in
            zip(list(range(0,len(list_of_contents))), list_of_contents, list_of_names)]
        return children, ""
    
    
# see https://stackoverflow.com/questions/61905396/dash-datatable-with-select-all-checkbox
# but updated for pattern-matching callback
@callback(
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
    
@callback(
    Output({'type': 'transaction_table', 'index': MATCH}, "data"), 
    Input({'type': "category_dropdown", 'index': MATCH}, "value"),
    State({'type': 'transaction_table', 'index': MATCH}, 'selected_rows'),
    State({'type': 'transaction_table', 'index': MATCH}, 'data')
)
def set_category(category, selected, original):
    if selected is None:
        raise PreventUpdate
    if not category:
        raise PreventUpdate
    return [update_category(category, selected, i, r) for i,r in enumerate(original)]

@callback(
    Output({'type': 'transactions_submit', 'index': MATCH}, "disabled"), 
    Output({'type': 'unknown-counter', 'index': MATCH}, "children"), 
    Input({'type': 'transaction_table', 'index': MATCH}, "data"), 
)
def enable_submit(data):
    count=[d['Category'] for d in data].count('UNKNOWN')
    if count > 0:
        return True, 'Unknowns remaining: {}'.format(count);
    else:
        return False, "";

@callback(
    Output({'type': 'transaction_table_container', 'index': MATCH}, 'children'),
    Input({'type': 'transactions_submit', 'index': MATCH}, "n_clicks"), 
    State({'type': 'transaction_table', 'index': MATCH}, 'data'),
    prevent_initial_call=True,
)
def do_submit(clicks, data):
    db.insertTransactions(pd.DataFrame(data))
    return 'Transactions submitted.'
