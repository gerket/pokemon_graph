# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objs as go
# import requests
# import pandas as pd
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server
#
# ############# Make changes here
#
#
# url_parameters = dict(
#     base_url = "pokeapi.co",
#     directory = "api/v2/pokemon",
#     pokemon_id = ''
# )
#
# def reset_endpoint():
#     global endpoint
#     endpoint = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)
#
# endpoint  = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)
#
# temp_results = requests.get(endpoint)
#
# temp_results = temp_results.json()
# temp_results = requests.get(endpoint + '?offset=0&limit='+str(temp_results['count']))
# temp_results = temp_results.json()
#
# name_url = dict()
# for i in temp_results['results']:
#     name_url[i['name']]=i['url']
#
# # multi_select_options = []
# # for i in temp_results['results']:
# #     multi_select_options.append(
# #     {
# #         'label':i['name'].capitalize(),
# #         'value':i['name']
# #     })
#
# app.layout = html.Div([
#         # multi-select dropdown menu
#         html.Div([
#             html.H1('Comparing Pokemon Statistics!'),
#             html.H2('Choose Pokemon to compare:'),
#             dcc.Dropdown(
#                 id='pokemon_choices',
#                 options=[{'label':i['name'].capitalize(), 'value':i['name']} for i in temp_results['results']],
#                 value='bulbasaur',
#                 multi=True
#             ),
#         ]),
#         # Graphs
#         html.H2('Comparison Graphs:'),
#         dcc.Graph(
#             id='graph_fig',
#             #figure=go.Figure()
#             # figure={
#             #     'data': [
#             #         {'x': ['Dog', 'Cat', 'Lobster'], 'y': [7, 8, 2], 'type': 'bar', 'name': 'Intelligence'},
#             #         {'x': ['Dog', 'Cat', 'Lobster'], 'y': [7, 3, 2], 'type': 'bar', 'name': 'Weight'},
#             #     ],
#             #     'layout': {
#             #         'title': "Animal Comparison",
#             #         'xaxis':{'title':'Animal'},
#             #         'yaxis':{'title':'Completely science-backed numbers with no metric'},
#             #     }
#             # }
#         )
#
#     ]
# )
#
# @app.callback(
#     dash.dependencies.Output('graph_fig', 'figure'),
#     [dash.dependencies.Input('pokemon_choices','value')])
# def update_graph(input_pokemon_choices):
#     if type(input_pokemon_choices)==str:
#         input_pokemon_choices = [input_pokemon_choices]
#
#     # if input_pokemon_choices == []:
#     #     return {
#     #         ‘data’: [
#     #             {   ‘x’: 'None',
#     #                 ‘y’: 0,
#     #                 ‘type’: ‘bar’,
#     #                 ‘name’: 'Test'
#     #             }],
#     #         ‘layout’: { ‘title’: “Health” } }
#     pokedex = dict()
#
#     #api calls to get the relevent info for each pokemon
#     for poke_name in input_pokemon_choices:
#         temp_results = requests.get(name_url[poke_name])
#         temp_results = temp_results.json()
#
#         temp_poke_df = pd.DataFrame(temp_results['stats'])
#         temp_poke_df['stat_name'] = [x['name'].capitalize() for x in temp_poke_df['stat']] #capitalize here
#         temp_poke_df.drop(columns=['stat', 'effort'], inplace=True)
#
#         pokedex[poke_name] = {'name':temp_results['name'],'df':temp_poke_df, 'id':temp_results['id']}
#
#     # Converting dict of stats into dataframe
#     pd_pokedex = pd.DataFrame()
#     for n, v in pokedex.items():
#         dat = [list(v['df']['base_stat'])]
#         dat[0].append(n.capitalize()) #capitalize here
#         cols = list(v['df']['stat_name'])
#         cols.append('Name')
#         pd_pokedex = pd_pokedex.append(
#             pd.DataFrame(
#                 data=dat, columns=cols
#             )
#         )
#
#
#     traces = []
#     for col in [x for x in pd_pokedex.columns if x != 'Name']:
#         traces.append(
#             go.Bar({
#                 'x':list(pd_pokedex['Name']),
#                 'y':list(pd_pokedex[col]),
#                 'name':col
#             })
#         )
#     layout = {
#         'barmode':'group'
#     }
#
#     fig={'data':traces, 'layout':go.Layout(layout)}
#     #return {'data':traces, 'layout':layout}#go.Figure(fig)
#     return {
#         'data':[{'x':list(pd_pokedex['Name']), 'y':list(pd_pokedex['Hp']), 'name':'Hp', 'type':'bar'}],
#         'layout': {'title':'Hp comparison graph'}
#     }
#
#
#
#
# ###### Don't change anything here
#
#
#
# if __name__ == '__main__':
#     app.run_server()

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)
