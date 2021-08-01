import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
        'outage_start': x['timestamp'].min(),
        'outage_end':  x['timestamp'].max(),
        'outage_duration': x['outage'].sum()}

    return pd.Series(names, index=['outage_start','outage_end','outage_duration'])


df_outages_pre = df[df['outage'] == 1]
df_outages = df_outages_pre.groupby('date', as_index=False).apply(my_agg)
df_outages['outage_time_h'] = df_outages['outage_duration'] // 60
df_outages['outage_time_m'] = df_outages['outage_duration'] % 60
df_outages['actual_outage_time'] = dt.timedelta(minutes=10)

print(df.head())
print(df_outages_pre.head())
print(df_outages.head())

# '''declare chart'''
# fig = px.line(df,x="timestamp", y="outage")
# # fig = px.timeline(df,x_start="timestamp", x_end="timestamp", y="working")

# # fig.show()

# '''declare layout elements'''
# LOGO = "https://toppng.com/uploads/preview/internet-comments-internet-11563646434apfsgdhqj7.png"

# #Navbar Layout
# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#             html.A(
#                 # Use row and col to control vertical alignment of logo / brand
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Img(src=LOGO, height="30px")),
#                         dbc.Col(dbc.NavbarBrand("InternetUp - A tool to check ISP connectivity", className="ml-2")),
#                     ],
#                     align="center",
#                     no_gutters=True,
#                 ),
#                 href="#",
#             )
#         ]
#     ),
#     color="dark",
#     dark=True,
#     className="mb-5",
# )

# # Graph Layout
# graph = dcc.Graph(
#     id = "line-graph",
#     figure = fig
# )

# '''Initiate Layout'''
# app.layout = html.Div(
#     [navbar, graph]
# )

# # app.layout = html.Div([
# #     dcc.Graph(figure=fig)
# # ])


# if __name__ == '__main__':
#     app.run_server(port='8083')
