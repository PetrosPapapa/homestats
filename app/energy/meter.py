from datetime import date, timedelta

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, callback, html
from dash.exceptions import PreventUpdate

def fields():
    lastElectricity = 12345
    lastGas = 4321
    lastDate = date.today() - timedelta(days=96)

    return [
        html.Label("Date", htmlFor="meter-date"),
        dcc.DatePickerSingle(
            id='meter-date',
            max_date_allowed=date.today(),
            #initial_visible_month=date(2017, 8, 5),
            date=lastDate,
            display_format='YYYY-MM-DD',
        ),
      
        html.Label("Electricity", htmlFor="meter-electricity"),
        dcc.Input(
            id="meter-electricity",
            type="number",
            placeholder=lastElectricity,
            # debounce=True,
            min=lastElectricity,
            required=True,
            inputMode='numeric',
        ),

        html.Label("Gas", htmlFor="meter-gas"),
        dcc.Input(
            id="meter-gas",
            type="number",
            placeholder=lastGas,
            # debounce=True,
            min=lastGas,
            required=True,
            inputMode='numeric',
        ),

        html.Button(
            "Submit",
            id="meter-submit",
            n_clicks=0,     
        )
    ]

def form():
    return html.Div([
        html.Form(
            fields(),
            id='meter-form',
            action="javascript:void(0);"
        ),
        html.Div("HAA!", id="meter-output")
    ])

@callback(
    Output('meter-output', 'children'),
    Output('meter-form', 'children'),
    Input('meter-submit', 'n_clicks'),
    State('meter-date', 'date'),
    State('meter-electricity', 'value'),
    State('meter-gas', 'value'),
    prevent_initial_call=True,
)
def update_output(n_clicks, date, electricity, gas):
    if electricity is not None and gas is not None:
        return 'Date {} Electricity {} Gas {}'.format(
            date,
            electricity,
            gas
        ), fields()
    
    else:
        raise PreventUpdate
