import dash
from dash import html
from dash_extensions import Lottie

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H2('Dash app is running! 😎'),
    Lottie(
        options=dict(
            loop=True, autoplay=True, 
            style=dict(width="40%", margin="auto"),
        ),
        url="https://assets6.lottiefiles.com/packages/lf20_rwwvwgka.json"
    )
])