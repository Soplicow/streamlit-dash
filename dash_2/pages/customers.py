import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/customers', name='Customers Overview')

df = pd.read_csv('../datasets/customers.csv')

# ---- Content Cards ----
season_filter = html.Div([
    html.Label('Season: '),
    dbc.Checklist(
        id='season_filter',
        options=['Spring', 'Summer', 'Fall', 'Winter'],
        value=['Spring', 'Summer', 'Fall', 'Winter'],
        inline=True,
        input_checked_style={
                'backgroundColor': '#C5a3D9',
                'borderColor': '#C5a3D9'},
        className='checklist'
    ), 
], className='select_row')

gender_card = dbc.Card([
    dbc.CardBody([
        html.H3('Gender'),
        dbc.Row(
            dcc.Dropdown(
                id='location_dropdown',
                options=[{'label': loc, 'value': loc} for loc in sorted(df['State_name'].unique())],
                value=df['State_name'].unique()[0],
                className='dropdown'
                 ),
            ),
        dcc.Graph(id='gender_pie')
    ])
], className='h-100')

location_card = dbc.Card([
    dbc.CardBody([
        html.H3('Location'),
        html.Label('Select age range: '),
        dcc.RangeSlider(
            id='age_range',
            min=int(df['Age'].min()),
            max=int(df['Age'].max()),
            step=1,
            value=[int(df['Age'].min()), int(df['Age'].max())],
            marks={i: str(i) for i in range(int(df['Age'].min()), int(df['Age'].max()) + 1, 5)},
            tooltip={'placement': 'bottom', 'always_visible': True},
            className='slider'
        ),
        dcc.Graph(id='location_choropleth')
    ])
],)

review_card = dbc.Card(
    dbc.CardBody([
        html.H3('Review Rating vs Amount'),
        dcc.Graph(id='review_line')
    ])
)

age_card = dbc.Card(
    dbc.CardBody([
        html.H3('Age'),
        html.Div([
            html.Label('Select gender: '),
            dbc.RadioItems(
                id='gender_radio',
                options=[{'label': g, 'value': g} for g in df['Gender'].unique()],
                value=df['Gender'].unique()[0],
                inline=True,
                className='radio'
            ), 
        ], className='select-row'),
        dcc.Graph(id='age_hist')
    ]), className='h-100')

# ---- Content Layout ----
layout = dbc.Container([
        html.H2('Customers Overview'),
        dbc.Card(dbc.CardBody(season_filter)),
        html.Br(),
        dbc.Row([
            dbc.Col(gender_card, width=5, className='card_chart'),
            dbc.Col(location_card, width=7, className='card_chart')
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(review_card, width=7, className='card_chart'),
            dbc.Col(age_card, width=5, className='card_chart')
        ])
], fluid=True)

# ---- Callback ----
@dash.callback(
    Output('gender_pie', 'figure'),
    Output('location_choropleth', 'figure'),
    Output('review_line', 'figure'),
    Output('age_hist', 'figure'),
    Input('season_filter', 'value'),
    Input('location_dropdown', 'value'),
    Input('gender_radio', 'value'),
    Input('age_range', 'value')
)
def update_graphs(seasons, selected_location, selected_gender, selected_age_range):
    dff = df[df['Season'].isin(seasons)]

    # Gender Pie
    pie_df = dff[dff['State_name'] == selected_location]
    fig_pie = px.pie(pie_df, names='Gender',
                     color='Gender')
    fig_pie.update_layout(height=400)

    # Age Histogram
    gender_df = dff[dff['Gender'] == selected_gender]
    fig_hist = px.histogram(gender_df, x='Age', nbins=20)
    fig_hist.update_layout(height=400)
    fig_hist.update_traces(marker_color='#C5a3D9', marker_line_width=1, marker_line_color='white')

    #Review Rating Line
    dff['Amount_Bin'] = pd.cut(dff['Amount'], bins=[0, 20, 40, 60, 80, 100], include_lowest=True)
    agg_df = dff.groupby('Amount')['Review_Rating'].mean().reset_index()

    fig_line = px.line(agg_df, x='Amount', y='Review_Rating', markers=True)
    fig_line.update_layout(xaxis_title='Amount (USD)', yaxis_title='Review Rating', height=450)

    df_grouped = dff.groupby('Prev_pur')['Review_Rating'].mean().reset_index()
    fig_line_2 = px.line(df_grouped, x='Prev_pur', y='Review_Rating', markers=True)
    fig_line_2.update_layout(xaxis_title='Count of previous purchases', yaxis_title='Review Rating')
    
    # Choropleth map (grouped and counted by state)
    pastel_colorscale = [[0.0, '#A8DADC'], [1.0, '#C5a3D9']] 
    min_age, max_age = selected_age_range
    age_df = dff[(dff['Age'] >= min_age) & (dff['Age'] <= max_age)]
    age_df = age_df.groupby('State_abbr').size().reset_index(name='Count')
    fig_map = px.choropleth(
        age_df,
        locations='State_abbr',
        locationmode='USA-states',
        scope='usa',
        color='Count',
        color_continuous_scale=pastel_colorscale)
    fig_map.update_layout(height=450)

    return fig_pie, fig_map, fig_line, fig_hist