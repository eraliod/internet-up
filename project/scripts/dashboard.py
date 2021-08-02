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

'''Initiate app'''
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

'''Import Data'''
df = pd.read_csv('log.csv')

df['outage'] = np.where(df['connection'] == 'connected', 0, 1)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date

def my_agg(x):
    names = {
        'outage_start': x['timestamp'].min().strftime('%H:%M'),
        'outage_end':  x['timestamp'].max().strftime('%H:%M'),
        'outage_minutes': x['outage'].sum()}

    return pd.Series(names, index=['outage_start','outage_end','outage_minutes'])

df_outages = df[df['outage'] == 1].groupby('date', as_index=False).apply(my_agg)

# there must be a different way
df_outages['outage_duration'] = df_outages['outage_minutes'].apply(lambda x: str(x//60)+':'+str(x%60) if len(str(x%60)) == 2 else str(x//60)+':0'+str(x%60))


# # stuff I tried and didn't work
# # df_outages['actual_outage_time'] = df_outages['outage_duration'].apply( lambda x: dt.datetime.fromtimestamp(x*60).strftime('%H:%M'))
# # df_outages['actual_outage_time'] = pd.to_timedelta(df_outages['outage_duration'],'m')
# # df_outages['formatted_outage_time'] = df_outages['actual_outage_time'].apply( lambda x: x.strftime('%H:%M'))

# # print(df.head())
# # print(df_outages.head())

'''declare chart'''
fig = px.line(df.groupby('date', as_index=False).apply(my_agg),x="date", y="outage_minutes")

# '''declare table'''
fig_table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in df_outages.columns], 
    data=df_outages.to_dict('records')
)


# # fig.show()

app.layout = dash_table.DataTable(
    data=df_outages.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df_outages.columns]
)

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

fig.update_layout(
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

'''Initiate Layout'''
app.layout = html.Div(
    [navbar, graph, fig_table]
)

if __name__ == '__main__':
    app.run_server(port='8083') #debug=True
