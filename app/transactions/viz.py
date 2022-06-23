import plotly.express as px
from transactions import data

def category_pie(transactions):
    df = data.expensesByCategory(transactions)
    return px.pie(df, 
                  values='Value', 
                  names='Category', 
                  title='Expenses by category'
                  )

def month_bars(transByMonth):
    df = data.expensesByMonth(transByMonth)
    fig = px.bar(df, 
                  x="Value", 
                  y="Date", 
                  color='Category', 
                  orientation='h',
#                  hover_data=["tip", "size"],
                  height=1000,
                  title='Expenses by month',
                  text='Value',
                  )
#    fig.update_layout(
#        xaxis=dict(
#            rangeselector=dict(
#                buttons=list([
#                    dict(count=1,
#                         label="1m",
#                         step="month",
#                         stepmode="backward"),
#                    dict(count=6,
#                         label="6m",
#                         step="month",
#                         stepmode="backward"),
#                    dict(count=1,
#                         label="YTD",
#                         step="year",
#                         stepmode="todate"),
#                    dict(count=1,
#                         label="1y",
#                         step="year",
#                         stepmode="backward"),
#                    dict(step="all")
#                ])
#            ),
#            rangeslider=dict(
#                visible=True
#            ),
#            type="date"
#        )
#    )
    return fig


