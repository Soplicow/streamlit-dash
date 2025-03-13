import yfinance as yf
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash()

app.layout = html.Div([
    html.H1("CZK to PLN Exchange Rate"),
    
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=pd.to_datetime("2020-01-01").date(),
        max_date_allowed=pd.to_datetime("today").date(),
        start_date=pd.to_datetime("2024-01-01").date(),
        end_date=pd.to_datetime("today").date(),
    ),
    
    dcc.Graph(id='exchange-rate-chart')
])

# Callback to update graph
@app.callback(
    Output('exchange-rate-chart', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_chart(start_date, end_date):
    # Ensure date format is YYYY-MM-DD
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    
    # Get exchange rates
    czk_usd = yf.Ticker("CZKUSD=X").history(start=start_date, end=end_date)["Close"]
    pln_usd = yf.Ticker("PLNUSD=X").history(start=start_date, end=end_date)["Close"]
    
    # Compute CZK to PLN rate
    czk_pln = czk_usd / pln_usd
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=czk_pln.index, y=czk_pln, mode='lines', name='CZK to PLN'))
    fig.update_layout(title='CZK to PLN Exchange Rate Over Time', xaxis_title='Date', yaxis_title='Exchange Rate')
    
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
