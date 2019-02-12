import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

############# Make changes here


url_parameters = dict(
    base_url = "pokeapi.co",
    directory = "api/v2/pokemon",
    pokemon_id = 58
)

def reset_endpoint():
    global endpoint
    endpoint = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)

endpoint  = "http://{base_url}/{directory}/{pokemon_id}".format(**url_parameters)

url_parameters['pokemon_id']=''
reset_endpoint()

temp_results = requests.get(endpoint)

temp_results = temp_results.json()
temp_results = requests.get(endpoint + '?offset=0&limit='+str(temp_results['count']))
temp_results = temp_results.json()

name_url = dict()
for i in temp_results['results']:
    name_url[i['name']]=i['url']

multi_select_options = []
for i in temp_results['results']:
    multi_select_options.append(
    {
        'label':i['name'],
        'value':i['name']
    })


app.layout = html.Div(
    children=[
        html.Label('Choose Pokemon to compare:'),
        dcc.Dropdown(
            options=multi_select_options,
            value=['MTL', 'SF'],
            multi=True
        ),

        html.H1('This is a better title!'),
        dcc.Graph(
            id='this_is_an_id',
            figure={
                'data': [
                    {'x': ['Dog', 'Cat', 'Lobster'], 'y': [7, 8, 2], 'type': 'bar', 'name': 'Intelligence'},
                    {'x': ['Dog', 'Cat', 'Lobster'], 'y': [7, 3, 2], 'type': 'bar', 'name': 'Weight'},
                ],
                'layout': {
                    'title': "Animal Comparison",
                    'xaxis':{'title':'Animal'},
                    'yaxis':{'title':'Completely science-backed numbers with no metric'},
                }
            }
        )
    ]
)


###### Don't change anything here



if __name__ == '__main__':
    app.run_server()
