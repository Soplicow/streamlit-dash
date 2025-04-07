import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "3rem 1rem",
    "background-color": "#343a40",
    "color": "white",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#212529",
    "color": "white",
}

toggle_button = dbc.Button(
    "☰", id="toggle-button", color="secondary",
    style={
        "position": "absolute",
        "top": "10px",
        "left": "10px",
        "zIndex": 1100,
        "margin-bottom": "20px",
        "background-color": "transparent",
    }
)

sidebar = html.Div([
    html.H2("Apps", className="display-4"),
    html.Hr(),
    html.P("A collection of example Dash projects", className="lead"),
    dbc.Nav(
        [
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Archive", href="/archive", active="exact"),
            dbc.NavLink("Exchange rates", href="/exchange-rate", active="exact"),
            dbc.NavLink("Iris", href="/iris", active="exact"),
            dbc.NavLink("Meteorites", href="/meteorites", active="exact"),
        ],
        vertical=True,
        pills=True,
    )],
    style=SIDEBAR_STYLE,
    id="sidebar"
)

content = html.Div(dash.page_container, style=CONTENT_STYLE, id="content")

app.layout = html.Div([dcc.Location(id="url"), toggle_button, sidebar, content])

@app.callback(
    Output("sidebar", "style"),
    Output("content", "style"),
    Input("toggle-button", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks):
    if n_clicks and n_clicks % 2 != 0:
        return (
            {"display": "none"}, 
            {
                "margin-left": "4rem",
                "margin-right": "auto",
                "padding": "2rem 1rem",
                "background-color": "#212529",
                "color": "white",
            }
        )
    else:
        return SIDEBAR_STYLE, CONTENT_STYLE


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)