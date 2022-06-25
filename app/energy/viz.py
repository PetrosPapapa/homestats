import plotly.express as px
from energy import data

def consumption_graphs():
    (ele, gas) = data.energiesPerMonth()

    efig = px.bar(ele, barmode="group", title="Electricity")
    efig.update_yaxes(minor=dict(ticks="inside", showgrid=True))

    gfig = px.bar(gas, barmode="group", title="Gas")
    gfig.update_yaxes(minor=dict(ticks="inside", showgrid=True))
    return (efig, gfig)
