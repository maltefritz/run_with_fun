import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.dates as dt
from datetime import datetime  # time, timedelta


# @st.cache
def get_data(file=''):
    """Import data."""
    return pd.read_excel(
        file, index_col=0
        )


def get_record(df, dis_rec):
    """
    Filters the record of a specified distance.

    Parameters
    ----------
    df : pandas.DataFrame
        Contains the input data including all run data to be analyzed.

    dis_rec : int/float
        Indicates the filtering distance of the record.

    Returns
    -------
    record: pandas.DataFrame
        Contains one row of the given input dataframe.
    """
    record = df[df['distance'] == dis_rec][df[df['distance'] == dis_rec][
        'speed'] == df[df['distance'] == dis_rec]['speed'].max()]
    return record


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

        df['pace_format'] = pd.to_datetime(
            df['pace'], unit='m'
            ).dt.strftime('%M:%S')

        with st.expander(f'Übersicht', expanded=True):
            act_ave = len(df.index)
            dis_ave = df['distance'].mean()
            rt_ave = df['run time'].mean()
            rt_ave = datetime.fromtimestamp(rt_ave).strftime('%M:%S')
            pac_ave = df['pace'].mean()
            pac_ave = datetime.fromtimestamp(pac_ave*60).strftime('%M:%S')
            spe_ave = df['speed'].mean()

            col1, col2 = st.columns(2)
            col1.metric('Anzahl Aktivitäten', f'🏃🏻 {act_ave}')

            col2, col3, col4, col5 = st.columns(4)
            col2.metric('⌀ Distanz', f'🛣️ {dis_ave:.2f} km')
            col3.metric('⌀ Laufzeit', f'⏱️ {rt_ave} min')
            col4.metric('⌀ Tempo', f'🔥 {pac_ave} min/km')
            col5.metric(
                '⌀ Geschwindigkeit', f'🚀 {spe_ave:.2f} km/h'
                )

        with st.expander(f'Zeitraum filtern', expanded=True):

            period = st.date_input(
                'Zeitraum auswählen:', value=(df.index[0], df.index[-1]),
                min_value=df.index[0], max_value=df.index[-1]
                )

        df['run time'] = df['run time'] / 60

        with st.expander(f'Statistik', expanded=True):
            tab1, tab2, tab3, tab4 = st.tabs(
                ['Distanz', 'Laufzeit', 'Tempo', 'Geschwindigkeit']
                )
            # Plots für Distanzen
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    fig1s, ax = plt.subplots(figsize=(16, 9))
                    ax.scatter(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'distance'].cumsum(),
                        linewidth=10
                        )
                    ax.plot(df.loc[period[0]:period[-1], 'distance'].cumsum())
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('kummlierte km')
                    ax.set_ylim(0)
                    ax.grid(linestyle='--')
                    st.pyplot(fig1s)

                with col2:
                    fig1b, ax = plt.subplots(figsize=(16, 9))
                    ax.bar(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'distance'], width=0.5
                        )
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('km')
                    ax.grid(linestyle='--')
                    st.pyplot(fig1b)

            # Plots für Laufzeiten
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    fig2s, ax = plt.subplots(figsize=(16, 9))
                    ax.scatter(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'run time'].cumsum(),
                        linewidth=10
                        )
                    ax.plot(df.loc[period[0]:period[-1], 'run time'].cumsum())
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('kummlierte Minuten')
                    ax.set_ylim(0)
                    ax.grid(linestyle='--')
                    st.pyplot(fig2s)

                with col2:
                    fig2b, ax = plt.subplots(figsize=(16, 9))
                    ax.bar(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'run time'], width=0.5
                        )
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('Minuten')
                    ax.grid(linestyle='--')
                    st.pyplot(fig2b)

            # Plots für Tempi
            df['pace'] = pd.to_datetime(df['pace'], unit='m')
            with tab3:
                col1, col2 = st.columns(2)
                with col1:
                    fig3s, ax = plt.subplots(figsize=(16, 9))
                    ax.scatter(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'pace'], linewidth=10
                        )
                    ax.plot(df.loc[period[0]:period[-1], 'pace'])
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('min/km')
                    ax.grid(linestyle='--')
                    st.pyplot(fig3s)

                with col2:
                    fig3b, ax = plt.subplots(figsize=(16, 9))
                    ax.bar(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'pace'],
                        width=0.5
                        )
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('min/km')
                    ax.grid(linestyle='--')
                    st.pyplot(fig3b)

            # Plots für Geschwindigkeiten
            with tab4:
                col1, col2 = st.columns(2)
                with col1:
                    fig4s, ax = plt.subplots(figsize=(16, 9))
                    ax.scatter(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'speed'], linewidth=10
                        )
                    ax.plot(df.loc[period[0]:period[-1], 'speed'])
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('km/h')
                    ax.grid(linestyle='--')
                    st.pyplot(fig4s)

                with col2:
                    fig4b, ax = plt.subplots(figsize=(16, 9))
                    ax.bar(
                        df.loc[period[0]:period[-1], :].index,
                        df.loc[period[0]:period[-1], 'speed'],
                        width=0.5
                        )
                    ax.set_xlabel('Datum')
                    ax.set_ylabel('km/h')
                    ax.grid(linestyle='--')
                    st.pyplot(fig4b)

        df['run time'] = pd.to_datetime(
            df['run time'], unit='m'
            ).dt.strftime('%H:%M:%S')

        with st.expander(f'Rekorde', expanded=True):
            col1, col2, col3 = st.columns(3)

            col1.metric(
                '🛣️ Weitester Lauf', f'{df["distance"].max():.2f} km'
                )
            col1.metric(
                '⏱️ Längster Lauf', f'{df["run time"].max():} h'
                )
            col1.metric(
                '🔥 Schnellstes ⌀ Tempo', f'{df["pace_format"].min()} min/km'
                )

            df_rec_3 = get_record(df, 3)
            df_rec_5 = get_record(df, 5)
            df_rec_10 = get_record(df, 10)

            if len(df_rec_3) > 0:
                col2.metric(
                    '⚡ Schnellste 3 km',
                    f'{df_rec_3.loc[df_rec_3.index[0], "run time"]} h - '
                    + f'{df_rec_3.loc[df_rec_3.index[0], "pace_format"]} min/km'
                    )
            if len(df_rec_5) > 0:
                col2.metric(
                    '🌪️ Schnellste 5 km',
                    f'{df_rec_5.loc[df_rec_5.index[0], "run time"]} h - '
                    + f'{df_rec_5.loc[df_rec_5.index[0], "pace_format"]} min/km'
                    )
            if len(df_rec_10) > 0:
                col2.metric(
                    '💥 Schnellste 10 km',
                    f'{df_rec_10.loc[df_rec_10.index[0], "run time"]} h - '
                    + f'{df_rec_10.loc[df_rec_10.index[0], "pace_format"]} min/km'
                    )

            df_rec_hm = get_record(df, 21.0975)
            df_rec_m = get_record(df, 42.195)

            if len(df_rec_hm) > 0:
                col3.metric(
                    '🥇 Schnellster Halbmarathon',
                    f'{df_rec_hm.loc[df_rec_hm.index[0], "run time"]} h - '
                    + f'{df_rec_hm.loc[df_rec_hm.index[0], "pace_format"]} min/km'
                    )
            if len(df_rec_m) > 0:
                col3.metric(
                    '🏆 Schnellster Marathon',
                    f'{df_rec_m.loc[df_rec_m.index[0], "run time"]} h - '
                    + f'{df_rec_m.loc[df_rec_m.index[0], "pace_format"]} '
                    + f'min/km'
                    )

    with st.expander(f'Laufzeitenrechner', expanded=False):
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
