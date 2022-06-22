import plotly.express as px
from energy import data

def consumption_graphs():
    (ele, gas) = data.energiesPerMonth()

    efig = px.bar(ele, barmode="group", title="Electricity")
    gfig = px.bar(gas, barmode="group", title="Gas")
    return (efig, gfig)
