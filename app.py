import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

############# Make changes here

app.layout = html.Div(children=[
    html.H1('Plotly Dash - the best way to visualize your data!'),
    dcc.Graph(
        id='this_is_an_id',
        figure={
            'data': [
                {'x': ['Dash', 'Powerpoint', 'Lascaux cave paintings'], 'y': [8, 2, 3], 'type': 'bar', 'name': 'Intelligence'},
                {'x': ['Dash', 'Powerpoint', 'Lascaux cave paintings'], 'y': [7, 1, 5], 'type': 'bar', 'name': 'Beauty'},
            ],
            'layout': {
                'title': "Because friends don't let friends use Microsoft Powerpoint",
                'xaxis':{'title':'Choice of data visualization'},
                'yaxis':{'title':'Approval rating by average data scientist'},
            }
        }
    )]
)


###### Don't change anything here

app = dash.Dash()
server = app.server


if __name__ == '__main__':
    app.run_server()
