
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def contagem_temporal_hosp(df, col_tempo, freq):

  temp_indice = df.set_index(col_tempo)

  hospitais_agrupados = temp_indice.resample(freq)['INSTITU'].unique()

  hospitais_progressivo = []
  cont_temp_hosp = []

  for tempo in hospitais_agrupados:
    for hospital in tempo:
      if hospital not in hospitais_progressivo:
        hospitais_progressivo.append(hospital)
    cont_temp_hosp.append(len(hospitais_progressivo))

  cont_temp_hosp = pd.Series(cont_temp_hosp, index=hospitais_agrupados.index, name='hospitais_cumulativos')

  # df_temporal = pd.concat([hospitais_agrupados, cont_temp_hosp], axis=1)
  return cont_temp_hosp


def analises_temporais(df, col_tempo, freq = 'ME', topo = [], media_movel=4, normalizacao=True):

  '''
  df[dataframe]: banco de dados a ser utilizado.
  topo[list]: lista com os cid dos tipos de câncer. se for passada uma lista vazia, o banco todo será analisado.
  freq[str]: unidade de tempo para análise. ['ME', 'W', 'D'].
  col_tempo[Series]: coluna do banco de dados com a data de consulta.
  media_movel[int]: número de períodos para média móvel. [default: 4].
  normalizacao[bool]: normalização pelo número de hospitais na unidade de tempo especificada. [default: True].
  '''

  #ajustes - títulos e legendas
  construcao_titulo = {
      'DTCONSULT': 'Número de consultas',
      'DTTRAT': 'Inícios de tratamentos',
      'DTULTINFO': 'Últimas informações'
  }

  info = construcao_titulo[col_tempo]

  add = 'normalizados' if normalizacao and col_tempo == 'DTTRAT' else 'normalizadas' if normalizacao else ''
  tempo_titulo = 'Dias' if freq == 'D' else 'Semanas' if freq == 'W' else 'Meses'


  #cópia do banco de dados
  df = df.copy()
  #seleção das topografias escolhidas
  if topo: # Check if the list is not empty
    df = df[df['TOPOGRUP'].isin(topo)]
  #selecionando só as consultas/inícios de tratamentos a partir de 2000
  df = df[df[col_tempo] >= '1994-01-01']

  #se a info for a última informação, selecionamos só os pacientes vivos
  if (col_tempo == 'DTULTINFO'):
    df = df[df['ULTINFO'].isin([1])]

  #dividimos a quantidade de casos pela unidade de tempo
  filt_tempo = df.resample(freq, on=col_tempo).size()


  if normalizacao:
    contagem_temporal = contagem_temporal_hosp(df, col_tempo, freq)
    casos_normalizados = []
    for indice in filt_tempo.index:
      contagem_hospitais = contagem_temporal.loc[indice]
      casos_normalizados.append(filt_tempo.loc[indice] / contagem_hospitais)

    filt_tempo = pd.Series(casos_normalizados, index=filt_tempo.index, name='casos_normalizados')


  #gráfico de casos por período de tempo
  plt.figure(figsize=(12,5))
  plt.plot(filt_tempo.index, filt_tempo.values, linewidth=1.5)
  plt.title(f'{info} por {tempo_titulo}')
  plt.xlabel('Data')
  plt.ylabel(f'Número de {info} {add}')
  plt.tight_layout()
  st.pyplot(plt)
  plt.clf()  # limpa a figura


  #gráfico de média móvel
  filt_tempo_mm = filt_tempo.rolling(window=media_movel).mean()
  print('\n')
  plt.figure(figsize=(12,5))
  plt.plot(filt_tempo.index, filt_tempo, alpha=0.4, label=f'{tempo_titulo}')
  plt.plot(filt_tempo_mm.index, filt_tempo_mm, color='red', linewidth=2, label= f'Média móvel ({media_movel} {tempo_titulo})')
  plt.title(f'{info} em {tempo_titulo} (com média móvel de {media_movel} {tempo_titulo})')
  plt.xlabel('Data')
  plt.ylabel(f'Número de {info} {add}')
  plt.legend()
  plt.tight_layout()
  st.pyplot(plt)
  plt.clf()  # limpa a figura


  #teste para aleatótio, caótico ou determinístico

def analises_temporais_simp(df, hosp=[], col_tempo = 'DTCONSULT', freq = 'ME', ec= ['I', 'II', 'III', 'IV'], topo = [], media_movel=4, normalizacao=True):

  #cópia do banco de dados
  df = df.copy()
  #seleção das topografias escolhidas
  if topo: # Check if the list is not empty
    df = df[df['TOPOGRUP'].isin(topo)]
  
  if hosp:
    df = df[df['DSCINST'].isin(hosp)]
  #selecionando só as consultas/inícios de tratamentos a partir de 2000
  df = df[df[col_tempo] >= '1994-01-01']
  df = df[df['ECGRUP'].isin(ec)]

  #se a info for a última informação, selecionamos só os pacientes vivos
  if (col_tempo == 'DTULTINFO'):
    df = df[df['ULTINFO'].isin([1])]

  #dividimos a quantidade de casos pela unidade de tempo
  filt_tempo = df.resample(freq, on=col_tempo).size()


  if normalizacao:
    contagem_temporal = contagem_temporal_hosp(df, col_tempo, freq)
    casos_normalizados = []
    for indice in filt_tempo.index:
      contagem_hospitais = contagem_temporal.loc[indice]
      casos_normalizados.append(filt_tempo.loc[indice] / contagem_hospitais)

    filt_tempo = pd.Series(casos_normalizados, index=filt_tempo.index, name='casos_normalizados')

  filt_tempo_mm = filt_tempo.rolling(window=media_movel).mean()

  #informações para os gráficos
  casos_periodo = {
    'x': filt_tempo.index,
    'Casos Originais': filt_tempo.values,
    'Médias Móveis': filt_tempo_mm
  }
  
  return pd.DataFrame(casos_periodo)