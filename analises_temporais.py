import streamlit as st
import pandas as pd
import notebook as nb
import matplotlib.pyplot as plt
from pyunicorn.timeseries import RecurrencePlot
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(layout='wide')
st.title('Análises Temporais')
st.divider()

# ---------- dados ----------

df = pd.read_csv('df_gh.csv', dtype={'CEP':str, 'CEP_HOSP':str})

# Converte as colunas de data para formato datetime
date_cols = ['DTCONSULT', 
             'DTDIAG', 
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


# --------------- Testes ---------------
st.divider()
st.title('Testes de Recorrência')
st.write('\n')
st.write('\n')

#---------- dados ----------

col7, col8 = st.columns([1, 1])

with col7:
    dim = st.slider(
        'Dim', 1, 5, 2, width=400
    )

with col8:      
    tau = st.slider(
        'Tau', 1, 5, 1, width=400
    )


st.write('\n')
st.write('\n')

#---------- testes de recorrência ----------
scaler = MinMaxScaler()
x = scaler.fit_transform(casos_periodo['Casos Originais'].dropna().values.reshape(-1, 1)).flatten()
x_mm = scaler.fit_transform(casos_periodo['Médias Móveis'].dropna().values.reshape(-1, 1)).flatten()
rp= RecurrencePlot(x, dim=dim, tau=tau, recurrence_rate=0.05)
rp_mm = RecurrencePlot(x_mm, dim=dim, tau=tau, recurrence_rate=0.05)

#----------- gráficos ----------

fig, axes = plt.subplots(1, 2, figsize=(10,5))

axes[0].imshow(rp.recurrence_matrix(), cmap='binary', origin='lower')
axes[0].set_title('Recurrence Plot - Série Original')

axes[1].imshow(rp_mm.recurrence_matrix(), cmap='binary', origin='lower')
axes[1].set_title('Recurrence Plot - Série Suavizada - MM')

for ax in axes:
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Tempo')

plt.tight_layout()
st.pyplot(plt)

#---------- métricas ----------
st.divider()
st.subheader('Métricas')

metrics = pd.DataFrame({
    'Série': ['Original', 'MM'],
    'Recurrence Rate': [rp.recurrence_rate(), rp_mm.recurrence_rate()],
    'Determinism': [rp.determinism(), rp_mm.determinism()],
    'Laminarity': [rp.laminarity(), rp_mm.laminarity()]
})

st.write(metrics)