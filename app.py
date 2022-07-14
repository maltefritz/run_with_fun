# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 09:11:32 2022

@author: Malte Fritz
"""

import streamlit as st
import json
import pandas as pd
import matplotlib.dates as dt

# %% Initialisation
with open('src\\exercises.json', 'r') as file:
    exercises = json.load(file)

st.set_page_config(
    layout='wide',
    page_title='MFSports',
    page_icon='src\\Logo.png'
    )

fp = dict()
# param = dict()

# %% Sidebar
with st.sidebar:
    st.image('src\\Logo.png')

    app = st.selectbox(
        'Wähle deine Anwendung aus',
        ['Laufanalyse', 'Fitnessanalyse', 'Fitnessplan']
        )

    if app == 'Fitnessplan':
        nos = st.number_input(
            'Wähle die Anzahl der Trainingseinheiten', 0, 7
            )
        noe = st.number_input(
            'Wie viele Übungen hat eine Trainingseinheit', 0, 10
            )

if app == 'Laufanalyse':
    st.title('Statistik deiner zurückgelgeten Läufe')

    user_file = st.file_uploader(
        'Ergebnisse der zurückgelegten Läufe einlesen:',
        type='xlsx'
        )

    with st.expander(f'Durchschnittliche Statistik', expanded=True):
        st.write(
            'Distanzen, Dauer, Anzahl Aktivitöten, Pace, Geschwindigkeiten',
            key=f's1'
            )

    with st.expander(f'Alle Statistik', expanded=True):
        st.write(
            'Statistiken: kum. Distanzen(Links), kum. Dauer(Links), '
            + 'Punkte/Balken: Pace(rechts), Geschwindigkeiten(rechts)',
            key=f's2'
            )

    with st.expander(f'Rekorde', expanded=True):
        st.write(
            '3km, 5km, 10km, 21km, 42km',
            key=f's3'
            )

    with st.expander(f'Laufzeitenrechner', expanded=True):
        st.write('Gebe deine Laufdaten ein:')

        col1, col2 = st.columns(2)
        with col1:
            dis = st.number_input(
                'Distanz', min_value=0, step=1, key=f'dis')
        with col2:
            unit = st.selectbox('Einheit', ['km', 'm'])

        col3, col4, col5 = st.columns(3)

        with col3:
            h = st.number_input(
                'Stunden', min_value=0, max_value=24, step=1, key=f'h'
                )
        with col4:
            minu = st.number_input(
                'Minuten', min_value=0, max_value=60, step=1, key=f'min'
                )
        with col5:
            sec = st.number_input(
                'Sekunden', min_value=0, max_value=60, step=1, key=f'sec'
                )

        col6, col7 = st.columns(2)

        with col6:
            if unit == 'km':
                speed = dis / (h + minu/60 + sec/3600)
                st.write(f'Geschwindigkeit:')
                st.write(f'{speed:.2f} km/h')
            elif unit == 'm':
                speed = (dis/1000) / (h + minu/60 + sec/3600)
                st.write(f'Geschwindigkeit:')
                st.write(f'{speed:.2f} km/h')

        # Pace noch entsprechend der richtigen Datetime anpassen
        with col7:
            if unit == 'km':
                pace = (h*60 + minu + sec/60) / dis
                st.write(f'Pace:')
                st.write(f'{pace:.2f} min/km')
            elif unit == 'm':
                pace = (h*60 + minu + sec/60) / (dis / 1000)
                st.write(f'Pace:')
                st.write(f'{pace:.2f} min/km')

elif app == 'Fitnessplan':
    st.title('Erstelle einen Fitnessplan')
    i = 0
    while i < nos:
        with st.expander(f'Trainingseinheit {i+1}', expanded=False):
            fp['session'] = st.text_input(
                'Name der Trainingseinheit', key=f'name{i}'
                )
            st.write('Wähle deine Übungen aus')

            j = 0
            while j < noe:
                muscle = st.multiselect(
                    'Wähle die Muskelgruppe(n) aus, die du trainieren willst',
                    ['Brust', 'Rücken'], key=f'muscle{i}{j}'
                    )
                fp['units'] = st.selectbox(
                    f'Übung {j+1}', exercises.keys(), key=f'exercises{i}{j}'
                    )
                j = j + 1

        i = i + 1

# Download button hinzufügen
