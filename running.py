# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 08:31:58 2021

@author: Malte Fritz
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import sys


def read_data(filename):
    df = pd.read_csv(filename)

    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['month name'] = df['date'].dt.strftime('%B')

    # Zeit in Sekunden, Tempo in km/h und pace in Min / km

    df['time'] = df['h'] * 3600 + df['min'] * 60 + df['sec']
    df['tempo'] = df['distance'] / (df['time'] / 3600)
    df['pace'] = (df['time'] / 60) / df['distance']

    # Pace in echte Minuten umrechnen

    df['pace'] = pd.to_datetime(df['pace'], unit='m')
    df['pace_format'] = df['pace'].dt.strftime('%M:%S')

    sum_dis = (df['distance'].sum())
    df['cum_sum_dis'] = (df['distance'].cumsum())

    return df

#
# month = ['Monat', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
#          'August', 'September', 'Oktober', 'November', 'Dezember']
# dt_format = dt.DateFormatter('%M:%S')
#
# # Excel Datei einlesen
#
# df = pd.read_csv(sys.argv[1], index_col=0, parse_dates=True, dayfirst=True)
# print(df)
#
# # Datum indexen
#
# df['year'] = df.index.year
# df['month'] = df.index.month
# df['day'] = df.index.day
# df['month name'] = df.index.strftime('%B')
#
# # Zeit in Sekunden, Tempo in km/h und pace in Min / km
#
# df['time'] = df['h'] * 3600 + df['min'] * 60 + df['sec']
# df['tempo'] = df['distance'] / (df['time'] / 3600)
# df['pace'] = (df['time'] / 60) / df['distance']
#
# # Pace in echte Minuten umrechnen
#
# df['pace'] = pd.to_datetime(df['pace'], unit='m')
# df['pace_format'] = df['pace'].dt.strftime('%M:%S')
#
# sum_dis = (df['distance'].sum())
# df['cum_sum_dis'] = (df['distance'].cumsum())
#
# """
# To do:
#     Zeiten anders einlesen, damit die Zeiten als Zeiten erkannt werden!
#         check
#
#     Schleife um Plots pro Monat zu erstellen
#         check
#     Plot mit doppelter y-Achse: km und pace + beste Zeit
#         check
#     Plots mit Kurzstrecken-, Mittelstrecken- und Langstreckenläufe
#
#     Rekordtabelle
#     Ausgabe als Excel- und Latechdatei
# """
# #%% Rekorde
#
# df_filtered_sd = df[df['distance'] <= 5]
# rec_sd = df_filtered_sd['tempo'].max()
#
# df_filtered_md = df[df['distance'] > 5]
# df_filtered_md = df_filtered_md[df_filtered_md['distance'] <= 10]
# rec_md = df_filtered_md['tempo'].max()
#
# df_filtered_ld = df[df['distance'] > 10]
# rec_ld = df_filtered_ld['tempo'].max()
#
# #%% Monatsplots
#
# # Plot der kummulierte Distanz pro Monat
#
# for i in range(len(df))[3:4]:
#     monthfilter = df['month'] == i
#     plt.plot(df[monthfilter]['day'], df[monthfilter]['distance'].cumsum(),
#              '--x', color='b', alpha=0.8, linewidth=0.5)
#     plt.xlabel('Tag des Monats')
#     plt.ylabel('Kummulierte Distanz in km')
#     plt.title('Kummulierte Distanz im Monat ' + month[i])
#     plt.grid(linestyle='--')
#     plt.show()
#
# # Plot der Laufgeschwindigkeit im Monat
#
#     # Create figure and plot space
#     fig, ax = plt.subplots()
#
#     # Add x-axis and y-axis
#     ax.scatter(df[monthfilter]['day'],
#            df[monthfilter]['pace'],
#            color='purple')
#
#     # Set title and labels for axes
#     ax.set(xlabel="Date",
#            ylabel="Precipitation (inches)",
#            title="Daily Total Precipitation\nJune - Aug 2005 for Boulder Creek")
#
#     # Define the date format
#     date_form = dt.DateFormatter("%M:%S")
#     ax.yaxis.set_major_formatter(date_form)
#
#     plt.show()
#
#     # ax=plt.gca()
#     # ax.set_xticks(dt_format)
#     # xfmt = dt.DateFormatter('%M:%S')
#     # ax.xaxis.set_major_formatter(xfmt)
#
#     plt.plot(df[monthfilter]['day'], df[monthfilter]['pace_format'], '--o',
#              color='r', alpha=0.6, linewidth=0.5)
#     plt.xlabel('Tag des Monats')
#     plt.ylabel('Geschwindigkeit in Min / km')
#     plt.title('Geschwindigkeiten der Läufe im ' + month[i])
#     plt.grid(linestyle='--')
#     plt.show()
#
# # Plot der
#
#     cm = plt.cm.get_cmap('plasma')
#     sc = plt.scatter(df[monthfilter]['day'], df[monthfilter]['distance'],
#                      linewidth=0.25, c=df[monthfilter]['tempo'], cmap=cm,
#                      alpha=1, edgecolors='black')
#     plt.grid(linestyle='--')
#     # plt.scatter(pop.champion_x[1], pop.champion_x[0], marker='x', linewidth=1,
#     #             c='red')
#     # plt.annotate('Optimum', xy=(pop.champion_x[1], pop.champion_x[0]),
#     #              xytext=(pop.champion_x[1]+3, pop.champion_x[0]+3),
#     #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
#     #                              color='red')
#                 # )
#     plt.ylabel('Distanz in km')
#     plt.xlabel('Tag des Monats')
#     plt.colorbar(sc, label='Geschwindigkeit in km/h')
#     # plt.savefig("scatterplot.svg")
#     plt.show()
#
# #
#
# sc = plt.scatter(df[monthfilter]['distance'], df[monthfilter]['tempo'],
#                  linewidth=0.25)
# plt.grid(linestyle='--')
# plt.ylabel('Geschwindigkeit')
# plt.xlabel('Distanz in km')
#
# plt.show()
#
#
# # monthfilter = df['month'] == 2
# # plt.plot(df[monthfilter]['day'], df[monthfilter]['distance'].cumsum(), '-x')
# # plt.xlabel('Tag des Monats')
# # plt.ylabel('km')
# # plt.title('Kurückgelegte km im Monat ')
# # plt.grid(True)
# # plt.show()
#
# print('Kurzstreckenrekord: ' + '{:.2f}'.format(rec_sd) + ' km/h')
# print('Mittelstreckenrekord: ' + '{:.2f}'.format(rec_md) + ' km/h')
# print('Langstreckenrekord: ' + '{:.2f}'.format(rec_ld) + ' km/h')
# print('{:.2f}'.format(sum_dis) + ' km')
# print(df)
#
# # df.to_csv('Resultate', sep=';')
