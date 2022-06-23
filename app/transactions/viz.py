import plotly.express as px
from transactions import data

def category_pie(transactions):
    df = data.expensesByCategory(transactions)
    return px.pie(df, 
                  values='Value', 
                  names='Category', 
                  title='Expenses by category'
                  )


