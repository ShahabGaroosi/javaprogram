import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import jsonpickle
import pickle
from pymongo import MongoClient
from datetime import datetime

from printResult import *
from FXclass import *
PathName = {**{epic:epic for epic in Epic}, **{TechIndMatrix[epic]['Name']:epic for epic in Epic}}

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000*30, # in milliseconds
            n_intervals=0
    )
])

def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th('')]+[html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([html.Td(html.A(dataframe.index[i], href='/'+dataframe.index[i], style={'color': 'white'}))]+[
                html.Td(str(dataframe.iloc[i][col])) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])

@app.callback([Output('live-update-table', 'children')],
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    TechIndMatrix = loadData(DB, Epic, Epic2, Resolution)
    Table = getTable(TechIndMatrix, Epic, Resolution)
    Table = generate_table(Table)
    return [Table]#+[str(TechIndMatrix['RiskRewards'])]


@app.callback([Output('live-update-table2', 'children'),Output('live-update-table3', 'children'),Output('live-update-table4', 'children')],
                [Input('interval-component', 'n_intervals'), Input('url', 'pathname')])
def update_metrics2(n, pathname):
    epic=PathName[pathname[1:]]
    TechIndMatrix = loadData(DB, [epic], Epic2, Resolution)
    Table = getTable(TechIndMatrix, [epic], Resolution).drop('USD')
    Table = Table.append(pd.DataFrame([[str(round((datetime.now()-datetime.strptime(TechIndMatrix[epic][i].lastModified, '%a %b  %d %H:%M:%S %Y')).seconds/60)) for i in Resolution]], ['LastUpd (min)'], Resolution)).fillna('')
    Table = Table.append(pd.DataFrame([[TechIndMatrix[epic][i].Performance for i in Resolution]], ['Perf'], Resolution)).fillna('')
    Table = generate_table(Table)
    Table2 = pd.DataFrame([TechIndMatrix[epic][resolution].RiskRewardRatio for resolution in Resolution], Resolution)
    Table3 = generate_table(Table2[Table2.columns.difference([1,2])])
    Table2 = generate_table(Table2[[1,2]])
    for resolution in Resolution:
        TechIndMatrix[epic][resolution]=TechIndMatrix[epic][resolution].__dict__
    return [Table]+[Table2]+[Table3]#+[str(TechIndMatrix[epic])]#[jsonpickle.encode(TechIndMatrix[epic])]

main_page = html.Div([
    html.Label([html.A(TechIndMatrix[epic]['Name']+',', href='/'+epic, style={'color': 'white'})  for epic in Epic]),
    html.Table(id='live-update-table'),
], style={'backgroundColor': 'rgb(9, 3, 42)', 'color': 'white', 'fontSize': 12})

page_layout = lambda epic: html.Div([
        dcc.Link('Go back to home', href='/', style={'color': 'white'}),
        html.Label([html.A(TechIndMatrix[epic]['Name']+',', href='/'+epic, style={'color': 'white'})  for epic in Epic]),
        html.H1(epic),
        html.Label([html.A(i[1]+',', href=i[0], style={'color': 'white'})  for i in TechIndMatrix[epic]['NewsLinks']]),
        html.Div(id='live-update-table2'),
        html.Div(id='live-update-table3'),
        html.Div(id='live-update-table4'),
        dcc.Link('Go back to home', href='/'),
        ],
        style={'backgroundColor': 'rgb(9, 3, 49)', 'color': 'white', 'fontSize': 12}
    )

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if PathName[pathname[1:]] in Epic:
        return page_layout(PathName[pathname[1:]])
    else:
        return main_page

if __name__ == '__main__':
    app.run_server(debug=True)

