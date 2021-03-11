# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset

from running import read_data

# loading external resources
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
options = dict(
    # external_stylesheets=external_stylesheets
)

df = read_data('template.csv')

datestepper = {
    'Y': 'years',
    'M': 'month',
    'W': 'weeks',
    'D': 'days'
}

stepper = 'W'

df.sort_values(by='date', ascending=True, inplace=True)

print(df)

# list of years/months/weeks/days
start = df['date'].iloc[0]
end = df['date'].iloc[-1]

periods = (end - start) // np.timedelta64(1, stepper) + 3

datelist = pd.date_range(start=start - DateOffset(**{datestepper[stepper]: 1}), periods=periods, freq=stepper)
marks = len(datelist)
print(datelist, marks)
tags = {} #dictionary relating marks on slider to tags. tags are shown as "Apr', "May', etc
datevalues = {} #dictionary relating mark to date value
x = 0
for date in datelist:
    tags[x + 1] = datelist[x].strftime('%d.%m.%Y')
    datevalues[x + 1] = date
    x += 1

print(datevalues)

print(df['date'][0])
print(df['date'][len(df['date']) - 1])

app = dash.Dash(__name__, **options)

app.layout = html.Div(
    children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''Dash: A web application framework for Python.'''),
        dcc.Dropdown(
            id='data-select',
            options=[{'label': i, 'value': i} for i in ['pace', 'tempo', 'distance', 'cumulated']],
            multi=False),
        dcc.Graph(id='scatter-plot'),
        dcc.RangeSlider(
            id='date-slider',
            updatemode='mouseup',
            count=1,
            min=1,
            max=marks,
            step=1,
            value=[marks, marks],
            marks=tags,
            pushable=1
        )
    ]
)


@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [Input(component_id='data-select', component_property='value'),
     Input(component_id='date-slider', component_property='value')])
def update_chart(data_select, date_range):
    start = datevalues[date_range[0]]
    end = datevalues[date_range[1]]
    filter = (df['date'] > start) & (df['date'] < end)
    if data_select == 'cumulated':
        df['cumulated'] = df[filter]['distance'].cumsum()
    fig = px.scatter(df[filter], x='date', y=data_select)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
