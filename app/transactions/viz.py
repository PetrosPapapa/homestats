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
                  y="Value", 
                  x="Date", 
                  color='Category', 
                  orientation='v',
#                  hover_data=["tip", "size"],
                  height=1000,
                  title='Expenses by month',
                  text='Value',
                  )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(count=2,
                         label="2y",
                         step="year",
                         stepmode="backward"),
                    dict(count=3,
                         label="3y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_yaxes(minor=dict(ticks="inside", showgrid=True))

    return fig


def month_balance_graph(transByMonth):
    df = data.balanceByMonth(transByMonth)
    fig = px.line(df, 
                  x="Date", 
                  y=["Value", "Smooth"], 
                  title='Balance per month',
                  color_discrete_map={"Smooth": 'green'},
                  height=700,
                  )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(count=2,
                         label="2y",
                         step="year",
                         stepmode="backward"),
                    dict(count=3,
                         label="3y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_yaxes(minor=dict(ticks="inside", showgrid=True))
    fig.update_traces(patch={"line": {"dash": 'dash'}}, selector={"legendgroup": "Smooth"}) 

    mean = round(df['Value'].mean(), 2)
    fig.add_hline(y=mean,
                  line_color='rgba(0, 0, 100, 0.5)',
                  annotation_text=str(mean)
                  )

    fig.add_hline(y=0,
                  line_color="black",
                  line_width=3,
                  )

    return fig;

def month_cumulative_graph(transByMonth):
    df = data.cumBalanceByMonth(transByMonth)
    fig = px.line(df, 
                  x="Date", 
                  y=["Value", "Smooth"], 
                  title='Cumulative balance per month',
                  color_discrete_map={"Smooth": 'green'},
                  height=700,
                  )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(count=2,
                         label="2y",
                         step="year",
                         stepmode="backward"),
                    dict(count=3,
                         label="3y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_yaxes(minor=dict(ticks="inside", showgrid=True))
    fig.update_traces(patch={"line": {"dash": 'dash'}}, selector={"legendgroup": "Smooth"}) 

    mean = round(df['Value'].mean(), 2)
    fig.add_hline(y=mean,
                  line_color='rgba(0, 0, 100, 0.5)',
                  annotation_text=str(mean)
                  )

    fig.add_hline(y=0,
                  line_color="black",
                  line_width=3,
                  )

    return fig;
