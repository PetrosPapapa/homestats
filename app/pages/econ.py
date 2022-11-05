import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import config
import appsecrets as ss
from transactions import data, viz 

from log import log

dash.register_page(__name__, order=2)

def layout():
    transactions=config.db.getTransactions()
    transactionsByMonth=data.transactionsByMonth(transactions, ss.transactions["firstDayOfMonth"])
    
    accounts = data.accounts(transactions).to_dict('records')

    log.debug(accounts)

    return html.Div(children=[

        html.H2('Select accounts'),       
        dcc.Checklist(
            accounts,
            [idx.get('value') for idx in accounts],
            id='account_checklist',
            style={
                'display': 'flex', 
                'flex-wrap': 'wrap', 
                'align-items': 'center', 
                'justify-content': 'space-evenly',
                'align-content': 'space-between',
                'font-size': '75%'
            },
            inline=True
        ),
        html.Button('Select All', id='select-all-accounts-button', n_clicks=0),
        html.Button('Deselect All', id='deselect-all-accounts-button', n_clicks=0),
        
        html.H2('Expenses by month'),       
        dcc.Graph(
            id='month_bars',
            className='month_bars',
            figure=viz.month_bars(transactionsByMonth)
        ),
        
        html.H2('Balance per month'),
        dcc.Graph(
            id='month_balance',
            figure=viz.month_balance_graph(transactionsByMonth)
        ),
        
        html.H2('Cumulative balance per month'),
        dcc.Graph(
            id='month_cumbalance',
            figure=viz.month_cumulative_graph(transactionsByMonth)
        ),
        
        html.H2('Expenses by category'),
        dcc.Graph(
            id='category_pie',
            className='category_pie',
            figure=viz.category_pie(transactions),
        ),
  ], className="econ")


@callback(
        Output('account_checklist', 'value'),
    [
        Input('select-all-accounts-button', 'n_clicks'),
        Input('deselect-all-accounts-button', 'n_clicks')
    ],
    [
        State('account_checklist', 'options')
    ]
)
def select_all_accounts(select_n_clicks, deselect_n_clicks, options):
    ctx = [*dash.callback_context.triggered_prop_ids.values()]
    if not ctx:
        raise PreventUpdate
    ctx_caller = ctx[0]
    log.debug("Clicked: " + ctx_caller)
    if ctx_caller == 'select-all-accounts-button':
        return [idx.get('value') for idx in options] 
    if ctx_caller == 'deselect-all-accounts-button':
        return []
    raise PreventUpdate
    
@callback(
    Output('month_bars', 'figure'),
    Input('account_checklist', 'value'),
    prevent_initial_call=True
)
def update_selected_accounts(values):
    transactions=config.db.getTransactions()
    transactionsByMonth=data.transactionsByMonth(transactions, ss.transactions["firstDayOfMonth"])
    return viz.month_bars(transactionsByMonth, values)
    
