import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from pandas.io.pytables import IndexCol
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt
import os

dire = os.getcwd()
print(dire)

'''Initiate app'''
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

'''Import Data'''
# declare functions needed for data transformation
def my_agg(x):
    names = {
        'outage_start': x['timestamp'].min().strftime('%H:%M'),
        'outage_end':  x['timestamp'].max().strftime('%H:%M'),
        'outage_minutes': x['outage'].sum()} #this is where I need to edit to make the last column better *60 or also math.ceil()
    return pd.Series(names, index=['outage_start','outage_end','outage_minutes'])

# declare the ETL of data as a function so it can be updated by the interval callback later
def import_data(x):
    df = pd.read_csv('data/log.csv', dtype=str)
    df['outage'] = np.where(df['connection'] == 'connected', 0, 1)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date

    print(df[df['outage'] == 1].shape[0])
    if df[df['outage'] == 1].shape[0] > 0:
        df_outages = df[df['outage'] == 1].groupby('date', as_index=False).apply(my_agg)

        # there must be a different way
        df_outages['outage_duration'] = df_outages['outage_minutes'].apply(lambda x: str(x//60)+':'+str(x%60) if len(str(x%60)) == 2 else str(x//60)+':0'+str(x%60))
        # df_outages['outage_duration'] = df_outages['outage_minutes']/60
        df_outages.drop(columns=['outage_minutes'], inplace=True)
    else:
        df_outages = pd.DataFrame(columns=['date','outage_start','outage_end','outage_duration'])
        df_outages.loc[0] = ['N/A','N/A','N/A','N/A']

    if x == 'full': 
        return df
    elif x == 'outages':
        return df_outages

df = import_data('full')
df_outages = import_data('outages')

'''declare chart'''
fig = px.line(data_frame=df.groupby('date', as_index=False).apply(my_agg),x="date", y="outage_minutes", title='Outages Over Time')

'''declare table'''
# table = dbc.Table(id='table').from_dataframe(df_outages, striped=True, bordered=True, hover=True) #replaced with dash_table as it was easier to callback the data for changes
table = dash_table.DataTable(
        id='table',
        data=df_outages.to_dict('records'),
        columns=[{'name':i,'id':i} for i in df_outages.columns],
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ])

'''declare layout elements'''
LOGO = "https://toppng.com/uploads/preview/internet-comments-internet-11563646434apfsgdhqj7.png"

#Navbar Layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("InternetUp - A tool to check ISP connectivity", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="#",
            )
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

# Graph Layout
graph = dcc.Graph(
    id = "line-graph",
    figure = fig
)

'''Initiate Layout'''
app.layout = html.Div(
    [html.H5(id='test-output')
    ,navbar
    ,html.Div(graph, className='container')
    ,html.Div(table, className='container')
    ,dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )]
)

'''Define callbacks'''
#timestamp call
@app.callback(Output('test-output','children'),
              Input('interval-component', 'n_intervals'))
def update_test(n):
    now =  dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'Time: {now}'

# line graph call
@app.callback(Output('line-graph','figure'),
              Input('interval-component', 'n_intervals'))
def update_line(n):  
    df = import_data('full')
    return px.line(data_frame=df.groupby('date', as_index=False).apply(my_agg),x="date", y="outage_minutes", title='Outages Over Time').update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        rangeslider_visible=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
        b=150
    ),
    showlegend=False,
    plot_bgcolor='white'
)

# table call
@app.callback(Output('table','data'),
              Input('interval-component', 'n_intervals'))
def update_table(n):  
    df_outages = import_data('outages')
    return df_outages.to_dict('records')
    
if __name__ == '__main__':
    # app.run_server(port='8083') #debug=True
    app.run_server(host='0.0.0.0')
