# Import required libraries
import pandas as pd
#import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
spacex_df = pd.read_csv(url)
print(spacex_df.columns)

# Read the airline data into pandas dataframe
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},

                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),


                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',5000: '5000', 10000:'10000'},
                                                value=[min_payload, max_payload],
                                                tooltip={"placement": "bottom", "always_visible": True}),


                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):

    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().reset_index()
    filtered_df.columns = ['class','values']
    filtered_df['class'] = filtered_df['class'].map({0:'Failure',1:'Success'})

    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
        names='Launch Site',
        title='Number of Launches'.title())
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    else:
        fig = px.pie(filtered_df, values='values',
             names='class',
             title='successful launches'.title(),
             color='class',
             color_discrete_map={'Success':'royalblue',
                                 'Failure' : 'red'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, mass_value):
    print(mass_value)
    filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site) &
                            (spacex_df['Payload Mass (kg)']>=mass_value[0]) &
                            (spacex_df['Payload Mass (kg)']<=mass_value[1])]
    filtered_df['class'] = filtered_df['class'].map({0: 'Failure', 1: 'Success'})

    if entered_site == 'ALL':
        
        fig = px.scatter(spacex_df[(spacex_df['Payload Mass (kg)']>=mass_value[0]) &
                            (spacex_df['Payload Mass (kg)']<=mass_value[1])],
                         y='class',
                         x='Payload Mass (kg)',
                         color="Booster Version Category"
                    )
        return fig
    else:
        fig = px.scatter(filtered_df, y='class',
                     x='Payload Mass (kg)',
                    color="Booster Version Category"
                    )
    return fig


if __name__ == '__main__':
    app.run_server()
