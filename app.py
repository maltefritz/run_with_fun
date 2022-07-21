import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.dates as dt
# from datetime import datetime, time, timedelta


# @st.cache
def get_data(file=''):
    """Import data."""
    return pd.read_excel(
        file, index_col=0
        )


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
    st.image('src\\Logo.png', use_column_width='always')

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

# %% Laufanalyse
if app == 'Laufanalyse':
    st.title('Statistik deiner zurückgelgeten Läufe')

    user_file = st.file_uploader(
        'Ergebnisse der zurückgelegten Läufe einlesen:',
        type='xlsx'
        )

    if user_file is None:
        st.info('Bitte fügen Sie eine Datei ein.')

    else:
        df = get_data(user_file)

        with st.expander(f'Durchschnittliche Statistik', expanded=True):
            act_ave = len(df.index)
            dis_ave = df['distance'].sum()/len(df.index)
            rt_ave = df['run time'].sum()/len(df.index)
            pac_ave = df['pace'].sum()/len(df.index)
            spe_ave = df['speed'].sum()/len(df.index)

            st.write(f'🏃🏻 Anzahl Aktivitäten: {act_ave}')
            st.write(f'🛣️ Durchschnittliche Distanz: {dis_ave:.2f} km')
            st.write(f'⏱️ Durchschnittliche Laufzeit: {rt_ave:.2f} min')
            st.write(f'🔥 Durchschnittliches Tempo: {pac_ave:.2f} min/km')
            st.write(
                f'🚀 Durchschnittliche Geschwindigkeit: {spe_ave:.2f} km/h'
                )

        with st.expander(f'Alle Statistik', expanded=True):
            # Zeitraum auswählbar machen
            # 2 Spalten
            # 2 kum Plots + 2 Balken

            period = st.date_input(
                'Zeitraum auswählen:', value=(df.index[0], df.index[-1]),
                min_value=df.index[0], max_value=df.index[-1]
                )

            tab1, tab2, tab3, tab4 = st.tabs(['dis', 'dau', 'Tem', 'Spe'])
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader('Distanz')

                    fig1s, ax = plt.subplots(figsize=(16, 9))
                    ax.scatter(
                        df.index,
                        df.loc[period[0]:period[-1], 'distance'].cumsum(),
                        linewidths=10
                        )
                    ax.plot(df.loc[period[0]:period[-1], 'distance'].cumsum())
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('kummlierte km')
                    ax.grid(linestyle='--')
                    st.pyplot(fig1s)

                    st.subheader('Dauer')

                with col2:
                    st.subheader('🛣️')
                    fig1b, ax = plt.subplots(figsize=(16, 9))
                    ax.bar(
                        df.index, df.loc[period[0]:period[-1], 'distance'],
                        width=0.5
                        )
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('km')
                    ax.grid(linestyle='--')
                    st.pyplot(fig1b)

            #     fig2s, ax = plt.subplots(figsize=(16, 9))
            #     ax.scatter(
            #         df.index,
            #         df.loc[period[0]:period[-1], 'run time'].cumsum(),
            #         linewidths=10
            #         )
            #     ax.plot(df.loc[period[0]:period[-1], 'run time'].cumsum())
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel('kummlierte Stunden')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig2s)

            #     st.subheader('Tempo')

            #     fig3s, ax = plt.subplots(figsize=(16, 9))
            #     ax.scatter(
            #         df.index,
            #         df.loc[period[0]:period[-1], 'pace'], linewidths=10
            #         )
            #     ax.plot(df.loc[period[0]:period[-1], 'pace'])
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel('$min/km$')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig3s)

            #     st.subheader('Geschwindigkeit')

            #     fig4s, ax = plt.subplots(figsize=(16, 9))
            #     ax.scatter(
            #         df.index,
            #         df.loc[period[0]:period[-1], 'speed'], linewidths=10
            #         )
            #     ax.plot(df.loc[period[0]:period[-1], 'speed'])
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel('km/h')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig4s)

            # with col2:
            #     st.subheader('🛣️')
            #     fig1b, ax = plt.subplots(figsize=(16, 9))
            #     ax.bar(
            #         df.index, df.loc[period[0]:period[-1], 'distance'],
            #         width=0.5
            #         )
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel('km')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig1b)

            #     st.subheader('⏱️')
            #     fig2b, ax = plt.subplots(figsize=(16, 9))
            #     ax.bar(
            #         df.index, df.loc[period[0]:period[-1], 'run time'],
            #         width=0.5
            #         )
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel('Stunden')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig2b)

            #     st.subheader('🔥')
            #     fig3b, ax = plt.subplots(figsize=(16, 9))
            #     ax.bar(
            #         df.index, df.loc[period[0]:period[-1], 'pace'], width=0.5
            #         )
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel(r'$min/km$')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig3b)

            #     st.subheader('🚀')
            #     fig4b, ax = plt.subplots(figsize=(16, 9))
            #     ax.bar(
            #         df.index, df.loc[period[0]:period[-1], 'speed'], width=0.5
            #         )
            #     ax.set_xlabel('Datum')
            #     ax.set_ylabel(r'$km/h$')
            #     ax.grid(linestyle='--')
            #     st.pyplot(fig4b)

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
                'Distanz', min_value=0, step=1, value=1, key=f'dis')
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
                'Sekunden', min_value=0, max_value=60, step=1, value=1,
                key=f'sec'
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

# %% Fitnessanalyse

# %% Fitnessplan
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
                muscle = st.selectbox(
                    'Wähle die Muskelgruppe aus, die du trainieren willst',
                    set([ex['Muskelgruppe'] for ex in exercises.values()]),
                    key=f'muscle{i}{j}'
                    )

                fp['units'] = st.selectbox(
                    f'Übung {j+1}',
                    [ex for ex in exercises if exercises[ex]['Muskelgruppe'] == muscle],
                    key=f'exercises{i}{j}'
                    )
                j = j + 1

        i = i + 1

# Download button hinzufügen
