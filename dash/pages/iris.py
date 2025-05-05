import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids

dash.register_page(__name__, path='/iris')

algorithms = {
    'Agglomerative': AgglomerativeClustering(n_clusters=3, linkage='ward'),
    'Kmeans': KMeans(n_clusters=3, random_state=42),
    'Kmedoids': KMedoids(n_clusters=3, random_state=42)
}

interactive_plot_card = dbc.Card([
    dbc.CardBody([
        html.H5('Interactive scatter plot with Iris dataset'),
        dcc.Graph(
            id="scatter-plot",
        ),
        html.P("Filter by petal width:"),
        dcc.RangeSlider(
            id='range-slider',
            min=0, max=2.5, step=0.1,
            marks={0: '0', 2.5: '2.5'},
            value=[0, 2.5]
        ),
    ])
])

clustering_plot_card = dbc.Card([
    dbc.CardBody([
        html.H5('Different clustering algorithms applied to Iris dataset'),
        dcc.Graph(
            id="scatter-plot2",
        ),
        html.P("Choose clustering algorithm:"),
        dcc.Dropdown(
            list(algorithms.keys()), 
            list(algorithms.keys())[0], 
            id='cluster-alg-dropdown',
            clearable=False 
        ),
    ])
])

layout = html.Div([
#    html.Div([
#        html.H4('Interactive scatter plot with Iris dataset'),
#        dcc.Graph(
#            id="scatter-plot",
#        ),
#        html.P("Filter by petal width:"),
#        dcc.RangeSlider(
#            id='range-slider',
#            min=0, max=2.5, step=0.1,
#            marks={0: '0', 2.5: '2.5'},
#            value=[0, 2.5]
#        )],
#    ),
#    html.Div([
#        html.H4('Different clustering algorithms applied to iris dataset'),
#        dcc.Graph(
#            id="scatter-plot2",
#        ),
#        html.P("Choose clustering algorithm:"),
#        dcc.Dropdown(
#            list(algorithms.keys()), 
#            list(algorithms.keys())[0], 
#            id='cluster-alg-dropdown',
#            clearable=False 
#        )],
#        style={"flex-wrap": "wrap"}
#    ),
#],
#    style={"display": "flex"}
    html.H2('Iris dataset'),
    dbc.Row([
        dbc.Col(interactive_plot_card, width=6),
        dbc.Col(clustering_plot_card, width=6)
    ])
])


@dash.callback(
    Output("scatter-plot", "figure"),
    Input("range-slider", "value"))
def update_scatter_plot(slider_range):
    df = px.data.iris()
    low, high = slider_range
    mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    fig = px.scatter(
        df[mask], x="sepal_width", y="sepal_length",
        color="species", size='petal_length',
        hover_data=['petal_width']
    )
    return fig

@dash.callback(
    Output("scatter-plot2", "figure"),
    Input("cluster-alg-dropdown", "value"))
def update_scatter_plot2(alg_name):
    df = px.data.iris()
    X = df.drop(columns=['species', 'species_id'])
    model = algorithms[alg_name]
    y_pred = model.fit_predict(X)
    fig = px.scatter(
        df, x="sepal_width", y="sepal_length",
        color=y_pred, size='petal_length',
        hover_data=['petal_width']
    )
    return fig