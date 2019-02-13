import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py
import requests
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

############# Make changes here


url_parameters = dict(
    base_url = "pokeapi.co",
    directory = "api/v2/pokemon",
    pokemon_id = ''
)

def reset_endpoint():
    global endpoint
    endpoint = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)

endpoint  = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)

temp_results = requests.get(endpoint)

temp_results = temp_results.json()
temp_results = requests.get(endpoint + '?offset=0&limit='+str(temp_results['count']))
temp_results = temp_results.json()

name_url = dict()
for i in temp_results['results']:
    name_url[i['name']]=i['url']

# multi_select_options = []
# for i in temp_results['results']:
#     multi_select_options.append(
#     {
#         'label':i['name'].capitalize(),
#         'value':i['name']
#     })

app.layout = html.Div([
        # multi-select dropdown menu
        html.Div([html.Label('Choose Pokemon to compare:'),
            dcc.Dropdown(
                id='pokemon_choices',
                options=[{'label':i['name'].capitalize(), 'value':i['name']} for i in temp_results['results']],
                value=[],
                multi=True
            ),
        ]),
        # Graphs

        html.H1('Comparing Pokemon Statistics!'),
        dcc.Graph(
            id='graph_fig',
            figure=go.Figure()
            # {
            #     'data': [
            #         {'x': ['Dog', 'Cat', 'Lobster'], 'y': [7, 8, 2], 'type': 'bar', 'name': 'Intelligence'},
            #         {'x': ['Dog', 'Cat', 'Lobster'], 'y': [7, 3, 2], 'type': 'bar', 'name': 'Weight'},
            #     ],
            #     'layout': {
            #         'title': "Animal Comparison",
            #         'xaxis':{'title':'Animal'},
            #         'yaxis':{'title':'Completely science-backed numbers with no metric'},
            #     }
            #}
        )

    ]
)

@app.callback(
    dash.dependencies.Output('graph_fig', 'figure'),
    [dash.dependencies.Input('pokemon_choices','value')]
)
def update_graph(input_pokemon_choices):
    if type(input_pokemon_choices)==str:
        input_pokemon_choices = [input_pokemon_choices]

    pokedex = dict()

    #api calls to get the relevent info for each pokemon
    for poke_name in input_pokemon_choices:
        temp_results = requests.get(name_url[x])
        temp_results = temp_results.json()

        temp_poke_df = pd.DataFrame(temp_results['stats'])
        temp_poke_df['stat_name'] = [x['name'].capitalize() for x in temp_poke_df['stat']] #capitalize here
        temp_poke_df.drop(columns=['stat', 'effort'], inplace=True)

        pokedex[x] = {'name':temp_results['name'],'df':temp_poke_df, 'id':temp_results['id']}

    # Converting dict of stats into dataframe
    pd_pokedex = pd.DataFrame()
    for n, v in pokedex.items():
        dat = [list(v['df']['base_stat'])]
        dat[0].append(n.capitalize()) #capitalize here
        cols = list(v['df']['stat_name'])
        cols.append('Name')
        pd_pokedex = pd_pokedex.append(
            pd.DataFrame(
                data=dat, columns=cols
            )
        )


    traces = []
    for col in [x for x in pd_pokedex.columns if x != 'Name']:
        traces.append(
            go.Bar(
                x=pd_pokedex['Name'],
                y=pd_pokedex[col],
                name=col

            )
        )
    layout = go.Layout(
        barmode='group'
    )

    fig=go.Figure(data=traces, layout=layout)
    #py.iplot(fig, filename='grouped-bar')
    return fig




###### Don't change anything here



if __name__ == '__main__':
    app.run_server()
