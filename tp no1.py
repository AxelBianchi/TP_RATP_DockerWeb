import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, dependencies

df = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv',sep=';')
ndf = df.sort_values(by=['Trafic'],ascending=False).head(10)
top_villes = df.groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).head(5).reset_index()

#_______________________________________________________________________________________________________________________
emp_df = pd.read_csv('emplacement-des-gares-idf.csv',sep=';')
emp2_df = pd.read_csv('emplacement-des-gares-idf.csv',sep=';')
emp_sort_x = emp_df.groupby('exploitant').groups.keys()
emp_sort_y = emp_df.groupby('exploitant').size().sort_values(ascending=False)
#_______________________________________________________________________________________________________________________
lgn_sort_x = emp_df.groupby('ligne').groups.keys()
lgn_sort_y = emp_df.groupby('ligne').size().sort_values(ascending=False)
#_______________________________________________________________________________________________________________________
emp_df[['lat', 'lng']] = emp_df['Geo Point'].str.split(',', expand=True)
emp_df['lat'] = emp_df['lat'].str.strip().astype(float)
emp_df['lng'] = emp_df['lng'].str.strip().astype(float)
#______________________________________________________________________________

app = Dash(__name__)
app.layout = (html.Div(children=[
    html.H1("Données de la RATP et IDF",style={'textAlign':'center','textDecoration':'underline','color': 'black','background':'white'}),
    html.H2('Données de la RATP',style={'textAlign' : 'center','background':'blue','color': 'white'}),
    html.Hr(),
    #Pour implémenter le filtre pour sélectionner en fonction des réseaux
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': category, 'value': category} for category in df['Réseau'].unique()],
            value=None,
            placeholder='Selectionne un réseau',
            style={
                'font-size': '16px',
                'padding': '12px 16px',
                'background-color': '#FFFFFF',
                'color': '#000000',
                'border': '2px solid #000000',
                'border-radius': '5px',
                'box-shadow': '2px 2px 4px rgba(0, 0, 0, 0.2)',
                'width': '100%',
                'max-width': '500px',
                'margin': '0 auto',
                'z-index': '9999',
            }
        ),
#==================1e div : RATP========================================================================================

    html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[
        # bar chart : Top 10 des stations en fonction du trafic
        dcc.Graph(
            id='RATP bar chart trafic',
            figure=px.bar(
                ndf,
                x='Station',
                y='Trafic',
                title='Top 10 des stations en fonction du trafic',
                labels={'Trafic': 'Nombre de passages'}
            )
        ),
        dcc.Graph(
            id='RATP pie chart trafic',
            figure=px.pie(
                top_villes,
                names='Ville',
                values='Trafic',
                title='Top 5 des villes en fonction du trafic',
                labels={'Trafic': 'Nombre de passages'}
            )
        ),
    ]),

    html.Hr(),
#==================2e div : Ile de france===============================================================================
    html.H2('Données Ile de France',style={'textAlign' : 'center','background':'blue','color': 'white'}),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.Br(),
        dcc.Dropdown(
            id='category-filter2',
            options=[{'label': exploitant, 'value': exploitant} for exploitant in emp_df['exploitant'].unique()],
            value=None,
            placeholder='Selectionne un exploitant',
            style={
                'font-size': '16px',
                'padding': '12px 16px',
                'background-color': '#FFFFFF',
                'color': '#000000',
                'border': '2px solid #000000',
                'border-radius': '5px',
                'box-shadow': '2px 2px 4px rgba(0, 0, 0, 0.2)',
                'width': '100%',
                'max-width': '500px',
                'margin': '0 auto',
                'z-index': '9999',
            }
        ),
    html.Div(style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}, children=[
        # Nombre d exploitant en fonction du nombre de stations
        dcc.Graph(
            id='IDF par exploitant',
            figure=px.bar(emp_df, x=emp_sort_x, y=emp_sort_y, title="Nombre de stations par exploitant",
                          labels={'x': 'Exploitant', 'y': 'Nombre de stations'})
            , style={'background-color': 'transparent'}
        ),
        # Nombre de lignes par ville
        dcc.Graph(
            id='IDF par ligne',
            figure=px.bar(emp_df, x=lgn_sort_x, y=lgn_sort_y, title="Nombre de lignes",
                          labels={'x': 'Exploitant', 'y': 'Nombre de lignes'})
        ),
    ]),
    html.Hr(),
    html.H2('Carte des stations',style={'textAlign' : 'center','background':'black','color': 'white'}),
    html.Hr(),
    html.Div(style={'display': 'middle'},children=[
        dcc.Graph(
            id="map-graph",
            figure=px.scatter_mapbox(emp_df, lat='lat',lon='lng',zoom=10,color="exploitant").update_layout(mapbox_style='open-street-map')
        )
    ])
],style={'background-image': 'url(https://i.redd.it/9btupkgefd541.jpg)'}))

#==============callbacks======================================================
@app.callback(
    dependencies.Output('RATP bar chart trafic', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_bar_chart(category, filtered_ndf=None):
    if category is None:
        filtered_ndf = ndf
    else:
        filtered_ndf = ndf[ndf['Réseau'] == category]
    return px.bar(filtered_ndf,x='Station',y='Trafic',title='Bar chart du trafic par Station')

@app.callback(
    dependencies.Output('RATP pie chart trafic', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_pie_chart(selected_category):
    if selected_category is None:
        filtered_df = top_villes
    else:
        filtered_df = df[df['Réseau'] == selected_category].groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).head(5).reset_index()

    return px.pie(filtered_df, names='Ville', values='Trafic', title='Pie chart')

#=============2e callbacks===============================================================
@app.callback(
    dependencies.Output('IDF par exploitant', 'figure'),
    [dependencies.Input('category-filter2', 'value')]
)
def update_bar_chart_emp(exploitant,filtered_emp=emp_df):
    if exploitant is None:
        filtered_emp = emp_df
    else:
        filtered_emp = emp_df[emp_df['exploitant'] == exploitant]
    emp_sort_x = filtered_emp.groupby('exploitant').groups.keys()
    emp_sort_y = filtered_emp.groupby('exploitant').size().sort_values(ascending=False)
    return px.bar(filtered_emp, x=emp_sort_x, y=emp_sort_y, title="Nombre de lignes par exploitant",labels={'x': 'exploitant', 'y': 'Nombre de lignes '})

@app.callback(
    dependencies.Output('IDF par ligne', 'figure'),
    [dependencies.Input('category-filter2', 'value')]
)
def update_bar_chart_lgn(exploitant):
    if exploitant is None:
        filtered_emp = emp2_df.reset_index()
    else:
        filtered_emp = emp2_df[emp_df['exploitant'] == exploitant]
    lgn_sort_x = filtered_emp.groupby('ligne').groups.keys()
    lgn_sort_y = filtered_emp.groupby('ligne').size().sort_values(ascending=False)
    return  px.bar(filtered_emp, x=lgn_sort_x, y=lgn_sort_y, title="Nombre de lignes par lignes", labels={'x': 'lignes', 'y': 'Nombre de lignes '})


if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=8050, debug=True)
    """localhost:8050 permet d'acceder à la page web"""








