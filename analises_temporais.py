import streamlit as st
import pandas as pd
import notebook as nb

st.set_page_config(layout='wide')
st.title('Análises Temporais')
st.divider()

# ---------- dados ----------

df = pd.read_csv('df_gh.csv', dtype={'CEP':str, 'CEP_HOSP':str})

# Converte as colunas de data para formato datetime
date_cols = ['DTCONSULT', 
            #  'DTDIAG', 
             'DTTRAT', 
             'DTULTINFO']

for col_data in date_cols:
    df[col_data] = pd.to_datetime(df[col_data])


tipos_grafico = {
    'Número de Consultas': 'DTCONSULT',
    'Inícios de Tratamento':'DTTRAT',
    'Últimas informações':'DTULTINFO'
}

periodos_tempo = {
    'Dias': 'D',
    'Semanas': 'W',
    'Meses': 'ME',
}

topografias = {
    'Todas': ['C18', 'C19', 'C20', 'C34', 'C50', 'C53', 'C61'],
    'Próstata': ['C18', 'C19', 'C20'],
    'Pulmão': ['C34'],
    'Mama': ['C50'],
    'Colo do Útero': ['C53'],
    'Colorretal': ['C61']
    }


estadiamento_clinico = {
    'Todos': ['I', 'II', 'III', 'IV'],
    'I': ['I'],
    'II':['II'],
    'III':['III'],
    'IV':['IV']
}

# ---------- página ----------

col1, col2 = st.columns([1,1])

with col1:
    tipo_grafico = st.pills(
        "Informações", tipos_grafico.keys(), selection_mode='single',
        default='Número de Consultas', 
    )

    periodo_tempo = st.pills(
    "Período temporal", periodos_tempo.keys(), selection_mode='single',
    default='Meses', 
    )

    estadiamento = st.pills(
        label='Estadiamento Clínico',
        options=estadiamento_clinico.keys(),
        selection_mode='single',
        default='Todos'
    )



with col2:
    topo = st.pills(
        "Topografias", topografias.keys(), selection_mode='single',
        default='Todas'
    )

    media_movel = st.slider(
    'Média Móvel', 2, 12, 4, width=400
    )

    hosp = st.multiselect(
        label='Hospitais',
        options=df.DSCINST.value_counts().index,
        placeholder='Selecione os hospitais desejados'
    )


colunas = st.segmented_control(
    label='Colunas',
    options=['Casos Originais', 'Médias Móveis'],
    selection_mode='multi',
    default=['Casos Originais', 'Médias Móveis']
    )

st.divider()

# ---------- gráfico ----------

casos_periodo = nb.analises_temporais_simp(df=df, hosp=hosp, col_tempo=tipos_grafico[tipo_grafico], freq=periodos_tempo[periodo_tempo], ec=estadiamento_clinico[estadiamento], topo=topografias[topo], media_movel=media_movel, normalizacao=True)

col5, col6 = st.columns([5, 1])

with col5:
    st.subheader(f'{tipo_grafico} em {periodo_tempo.lower()} (com média móvel de {media_movel} {periodo_tempo.lower()})')

with col6:
    csv = casos_periodo.to_csv(index=False)
    st.download_button(
        label= 'Baixe os dados em .csv',
        data=csv,
        file_name=f'{tipo_grafico}'
    )

st.write('\n')
st.write('\n')
st.line_chart(data=casos_periodo, x='x', y=colunas, x_label='Tempo', y_label=f'{tipo_grafico} com normalização')


# ---------- Testes ----------
st.divider()
st.title('Testes de Recorrência')