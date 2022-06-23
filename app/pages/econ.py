import dash
from dash import html, dcc

import config
from transactions import data, viz 

dash.register_page(__name__, order=2)

def layout():
    transactions=config.db.getTransactions()
    transactionsByMonth=data.transactionsByMonth(transactions)
    
    return html.Div(children=[
  
        html.H1('Expenses by month'),       
        dcc.Graph(
            id='month_bars',
            className='month_bars',
            figure=viz.month_bars(transactionsByMonth)
        ),
        
        html.H1('Balance per month'),
        dcc.Graph(
            id='month_balance',
            figure=viz.month_balance_graph(transactionsByMonth)
        ),
        
        html.H1('Cumulative balance per month'),
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

