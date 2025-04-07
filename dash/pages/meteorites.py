import dash
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/meteorites')

path = '../datasets/Meteorite_Landings.csv'
df = pd.read_csv(path)
df = df.dropna(subset=["mass (g)"])
df = df.sort_values("mass (g)", ascending=False).head(1000)

# print(df)

layout = html.Div([
    # html.H1('Table of meteorite data'),
    # dash.dash_table.DataTable(
    #     id='meteorite-table',
    #     columns=[{"name": i, "id": i} for i in df.columns],
    #     data=df.to_dict('records'),
    #     page_size=10,
    #     style_table={'overflowX': 'auto'},
    #     style_cell={
    #         'textAlign': 'left',
    #         'padding': '5px',
    #         'border': '1px solid black',
    #         "background-color": "#212529",
    #         "color": "white",
    #     },
    # ),
    html.H4('Map of meteorite landings'),
    dcc.Graph(
        figure = px.scatter_geo(df, lat="reclat", lon="reclong", size="mass (g)", hover_name="name"),
        id="meteorite-map",
        style={"background-color": "#212529", "color": "white"}
    ),
    html.H4("Filter by Year"),
    dcc.RangeSlider(
        id='year-slider',
        min=int(df['year'].min()),
        max=int(df['year'].max()),
        step=1,
        value=[int(df['year'].min()), int(df['year'].max())],
        marks={int(year): str(int(year)) for year in df['year'].dropna().unique()[::10]},
        tooltip={"placement": "bottom", "always_visible": True},
    ),
])

@dash.callback(
    Output("meteorite-map", "figure"),
    Input("year-slider", "value"))
def update_scatter_plot(year_range):
    low, high = year_range
    filtered_df = df[(df["year"] >= low) & (df["year"] <= high)]

    fig = px.scatter_geo(
        filtered_df,
        lat="reclat",
        lon="reclong",
        size="mass (g)",
        hover_name="name",
        color="year",
        projection="natural earth"
    )

    fig.update_layout(
        plot_bgcolor="#212529",
        paper_bgcolor="#212529",
        font=dict(color="white")
    )

    return fig