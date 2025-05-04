import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/purchases", name="Purchases Overview")

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
                "backgroundColor": "#C5a3D9",
                "borderColor": "#C5a3D9"},
        className='checklist'
    ), 
], className='select_row')

item_category_card = dbc.Card([
    dbc.CardBody([
        html.H3("Purchases by Item and Category"),
        html.Div([
            html.Label("Group by:"),
            dbc.RadioItems(
                id='group_by',
                options=[
                    {'label': 'Item', 'value': 'Item'},
                    {'label': 'Category', 'value': 'Category'}],
                    value='Item',
                    inline=True,
                )
        ], className='select-row'),
        html.Br(),
        dcc.Graph(id='orders_bar')
    ])
])

freq_card = dbc.Card([
    dbc.CardBody([
        html.H3("Purchase Frequency by Discount Usage"),
        html.Div([
            html.Label("Select Gender(s):"),
            dbc.Checklist(
                id='gender_filter',
                options=[{'label': g, 'value': g} for g in sorted(df['Gender'].unique())],
                value=df['Gender'].unique().tolist(),
                inline=True,
                input_checked_style={
                    "backgroundColor": "#C5a3D9",
                    "borderColor": "#C5a3D9"},
                className='checklist'
            ),
        ], className='select-row'),
        html.Br(),
        dcc.Graph(id='discount_freq_bar')
    ])
], className='h-100')

payment_card = dbc.Card([
    dbc.CardBody([
        html.H3("Payment Methods by Age"),
        html.Label("Select Age Range:"),
        dcc.RangeSlider(
            id='age_range',
            min=int(df['Age'].min()),
            max=int(df['Age'].max()),
            step=1,
            value=[int(df['Age'].min()), int(df['Age'].max())],
            marks={i: str(i) for i in range(int(df['Age'].min()), int(df['Age'].max()) + 1, 5)},
            tooltip={"placement": "bottom", "always_visible": True},
            className='slider'
        ),
        html.Br(),
        dcc.Loading(dcc.Graph(id='payment_donut'), type='dot', color='#C5a3D9')
    ])
], className='h-100')

# ---- Content Layout ----
layout = dbc.Container([
        html.H2('Purchases Overview'),
        dbc.Card(dbc.CardBody(season_filter)),
        html.Br(),
        dbc.Row(dbc.Col(item_category_card, className='card_chart')),
        html.Br(),
        dbc.Row([
            dbc.Col(payment_card, width=6, className='card_chart'),
            dbc.Col(freq_card, width=6, className='card_chart')
        ]),
],fluid=True)

# ---- Callback ----
@dash.callback(
    Output('orders_bar', 'figure'),
    Output('discount_freq_bar', 'figure'),
    Output('payment_donut', 'figure'),
    Input('season_filter', 'value'),
    Input('group_by', 'value'),
    Input('gender_filter', 'value'),
    Input('age_range', 'value')
)

def update_graphs(selected_seasons, group_by, selected_genders, selected_age_range):
    dff = df[df['Season'].isin(selected_seasons)]

    # Items-Category Barplot
    grouped = dff.groupby([group_by, 'Gender']).size().reset_index(name='OrderCount')

    fig_bar_it_cat = px.bar(grouped, x=group_by, y='OrderCount', color='Gender', barmode='group')
    fig_bar_it_cat.update_layout(xaxis_title=group_by, yaxis_title="Number of Orders", legend_title='Gender')


    # Frequency-Discount Barplot
    dff = df[df['Gender'].isin(selected_genders)]
    freq_counts = dff.groupby(['Frequency', 'Discount']).size().reset_index(name='Count')

    freq_order = ['Weekly','Bi-Weekly', 'Fortnightly', 'Monthly', 'Every 3 Months', 'Quarterly', 'Annually']
    freq_counts['Frequency'] = pd.Categorical(freq_counts['Frequency'], categories=freq_order, ordered=True)
    freq_counts = freq_counts.sort_values('Frequency')

    fig_bar_freq = px.bar(freq_counts,
                 x='Frequency', y='Count', color='Discount',
                 barmode='stack',
                 labels={'Frequency': 'Purchase Frequency', 'Count': 'Number of Customers'})
    
    # Payment Donut
    min_age, max_age = selected_age_range
    dff = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]

    payment_counts = dff['Payment'].value_counts().reset_index()
    payment_counts.columns = ['Payment Method', 'Count']

    fig_don = px.pie(payment_counts,
                 names='Payment Method',
                 values='Count',
                 hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)

    fig_don.update_layout(showlegend=True)

    return fig_bar_it_cat, fig_bar_freq, fig_don