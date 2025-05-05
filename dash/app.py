import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
import plotly.io as pio

# ---- Global color scheme for graphs ----
pio.templates['pastel_trio'] = pio.templates['plotly_white']
pio.templates['pastel_trio'].layout.colorway = ['#A8DADC', '#C5a3D9', '#F6BD60']
pio.templates.default = 'pastel_trio'
# ----

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True, 
               meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = 'Dashboard'

sidebar = html.Div(
    [
        # ---- title with icon ----
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Img(src=app.get_asset_url('dashboard.png'), height='35px'), width='auto'),
                    dbc.Col(html.H1('Dashboard', style={'fontSize': '35px', 'margin': 0}))
                ], align='center', className='g-2')
            ])
        ], justify='start', align='center', style={'height': '65px'}),
        # ----
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Exchange rates", href="/exchange-rate", active="exact"),
            dbc.NavLink("Iris analysis", href="/iris", active="exact"),
            dbc.NavLink("Meteorite landings", href="/meteorites", active="exact"),
            dbc.NavLink('Customers overview', href='/customers', active='exact'),
            dbc.NavLink('Purchases overview', href='/purchases', active='exact'),
        ], vertical=True,pills=True)
    ], className='sidebar'
)

app.layout = html.Div([
    dcc.Location(id='url', pathname='/'),
    sidebar,
    html.Div(dash.page_container, className='content')
])

if __name__ == "__main__":
    app.run(debug=True)