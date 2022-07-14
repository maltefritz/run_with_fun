# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 09:11:32 2022

@author: Malte Fritz
"""

import streamlit as st
import json
import numpy as np

# %% Initialisation
with open('src\\exercises.json', 'r') as file:
    exercises = json.load(file)

st.set_page_config(
    layout='wide',
    page_title='MFSports',
    page_icon='src\\Logo.png'
    )

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

if app == 'Fitnessplan':
    st.title('Erstelle einen Fitnessplan')
    i = 0
    while i < nos:
        with st.expander(f'Trainingseinheit {i+1}', expanded=False):
            st.text_input('Name der Trainingseinheit', key=f'Name {i}')
            st.write('Wähle deine Übungen aus')

            j = 0
            while j < noe:
                units = st.selectbox(
                    f'Übung {j+1}', exercises.keys(),
                    index=len(exercises.keys())-1, key=f'exercises {i}{j}'
                    )
                j = j + 1

        i = i + 1
