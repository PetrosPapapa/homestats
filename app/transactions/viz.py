import plotly.express as px
import plotly.graph_objects as go
from transactions import data

def category_pie(transactions):
    df = data.expensesByCategory(transactions)
    return px.pie(df, 
                  values='Value', 
                  names='Category'
                  )

def month_bars(transByMonth, accounts=[]):
    df = data.expensesByMonth(transByMonth, accounts)
    fig1 = px.bar(df, 
                  y="Value", 
                  x="Date", 
                  color='Category', 
                  orientation='v',
                  text='Value',
                  )

    fig1.update_layout(
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

    fig1.update_yaxes(minor=dict(ticks="inside", showgrid=True))

    dfin = data.incomeByMonth(transByMonth)
    fig1.add_trace(go.Scatter(x=dfin['Date'], y=dfin['Income'],
                    mode='lines+markers',
                    name='Income',
                    line=dict(color="rgba(0, 180, 5, 0.5)"),
                    ))

#    fig.update_layout(legend=dict(
#        orientation="h",
#        yanchor="bottom",
#        y=1.02,
#        xanchor="right",
#        x=1
#    ))

    return fig1


def month_balance_graph(transByMonth):
    df = data.balanceByMonth(transByMonth)
    fig = px.line(df, 
                  x="Date", 
                  y=["Value", "Smooth"], 
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
    fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))
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
    fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))
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
