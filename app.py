import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


############# Make changes here




# Setting up the initial api url
url_parameters = dict(
    base_url = "pokeapi.co",
    directory = "api/v2/pokemon",
    pokemon_id = ''
)

endpoint  = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)

# Getting a result from the api that includes the number of pokemon
first_request = requests.get(endpoint)
first_results = first_request.json()

# Getting a result containing all of the pokemon's names and api urls
second_request = requests.get(endpoint + '?offset=0&limit='+str(first_results['count']))
second_results = second_request.json()

# Storing the Pokemon names and urls for later use
name_url = dict()
for i in second_results['results']:
    name_url[i['name']]=i['url']

#
app.layout = html.Div([

        html.Div([
            # Big header
            html.H1('Comparing Pokemon Statistics!'),
            # Little bit smaller header
            html.H2('Choose Pokemon to compare:'),

            # multi-select dropdown menu
            dcc.Dropdown(
                id='pokemon_choices',
                options=[{'label':i['name'].capitalize(), 'value':i['name']} for i in second_results['results']],
                value='bulbasaur',
                multi=True
            ),
        ]),
        html.Div([
            # Little bit smaller header
            html.H2('Comparison Graph:'),
            # Graph placement
            dcc .Graph(
                id='graph_fig',
                )
        ])
    ]
)

@app.callback(
    dash.dependencies.Output('graph_fig', 'figure'),
    [dash.dependencies.Input('pokemon_choices','value')])
def update_graph(input_pokemon_choices):
    if type(input_pokemon_choices)==str:
        input_pokemon_choices = [input_pokemon_choices]

    pokedex = dict()

    #api calls to get the relevent info for each pokemon
    for poke_name in input_pokemon_choices:
        temp_request = requests.get(name_url[poke_name])
        temp_results = temp_request.json()

        temp_poke_df = pd.DataFrame(temp_results['stats'])
        temp_poke_df['stat_name'] = [x['name'].capitalize() for x in temp_poke_df['stat']]
        temp_poke_df.drop(columns=['stat', 'effort'], inplace=True)

        pokedex[poke_name] = temp_poke_df

    # Converting dict of stats into dataframe
    pd_pokedex = pd.DataFrame()
    for name, value in pokedex.items():
        dat = [list(value['base_stat'])]
        dat[0].append(name.capitalize())
        cols = list(value['stat_name'])
        cols.append('Name')
        pd_pokedex = pd_pokedex.append(
            pd.DataFrame(
                data=dat, columns=cols
            )
        )


    # List comprehension to create data for the graph
    traces = [
        go.Bar({
            'x':list(pd_pokedex['Name']),
            'y':list(pd_pokedex[col]),
            'name':col
        }) for col in [x for x in pd_pokedex.columns if x != 'Name']
    ]

    layout = {
        'barmode':'group'
    }

    fig={'data':traces, 'layout':go.Layout(layout)}
    return go.Figure(fig)




###### Don't change anything here

if __name__ == '__main__':
    app.run_server()
