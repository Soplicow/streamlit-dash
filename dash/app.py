import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#343a40",  # Dark background
    "color": "white",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#212529",  # Dark background for content
    "color": "white",
}
sidebar = html.Div(
    [
        html.H2("Apps", className="display-4"),
        html.Hr(),
        html.P("A collection of example Dash projects", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Archive", href="/archive", active="exact"),
                dbc.NavLink("Exchange rates", href="/exchange-rate", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(dash.page_container, style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)