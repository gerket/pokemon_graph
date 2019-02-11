import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


app = dash.Dash()
server = app.server

############# Make changes here

app.layout = html.Div(children=[
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
    )]
)


###### Don't change anything here



if __name__ == '__main__':
    app.run_server()
