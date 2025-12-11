import streamlit as st
from st_functions import load_data, load_map, load_map_pydeck
from streamlit_folium import st_folium
from notebook.dt import características_drs

st.set_page_config(layout='wide', page_title='Análises de Distâncias e Tempos', page_icon='midia\conecta-logo.png')

st.title('Análises de Distâncias e Tempos')
st.divider()

# ---------- dados ----------

df = load_data(
    file_path=r'datasets\dt_simp.csv', 
    dtype={'CEP':str, 'CEP_HOSP':str},
    date_cols=['DTCONSULT', 'DTDIAG', 'DTTRAT', 'DTULTINFO'],
)

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

tipo_drs = {
    'DRS de Residência': 'DRS',
    'DRS de Hospital': 'DRS_INST',
}

# ---------- página ----------

estadiamento = st.pills(
        label='Estadiamento Clínico',
        options=estadiamento_clinico.keys(),
        selection_mode='single',
        default='Todos'
    )

topo = st.pills(
    "Topografias", topografias.keys(), selection_mode='single',
    default='Todas'
)

d = st.radio(
    label='DRS de Residência ou de Hospital',
    options=tipo_drs.keys(),
    horizontal=True,
    label_visibility='collapsed',
    index = 0,
)

drs = st.selectbox(
    label='DRS',
    options=sorted(df[tipo_drs[d]].unique()),
    placeholder=f'Selecione a {d} desejada',
    index=None,
)

resultados = características_drs(df, topografias[topo], estadiamento_clinico[estadiamento], drs, 'CARRO')
resultados_o = características_drs(df, topografias[topo], estadiamento_clinico[estadiamento], drs, 'TRANSP')

# ---------- mapa ----------

deck = load_map_pydeck()
st.pydeck_chart(deck)

# ---------- métricas ----------
st.divider()


if drs != None:
    st.header(f"DRS {drs}")
    st.badge(f"Principal DRS externa para tratamento: DRS {resultados['Principal DRS de Saida']}", color='blue', icon=':material/fluid_med:')

st.write('\n')
st.write('\n')
st.write('\n')

c, d, e, f, g = st.columns(5)
with c:
    st.metric(':orange[Total de Pacientes]', f"{resultados['Total de Pacientes']:,}".replace(',','.'), )
with d:
    if drs != None:
        st.metric(f":orange[Pacientes que se tratam na DRS {drs}]", f"{resultados['Pacientes na Mesma DRS']:,}".replace(',','.'))
with e:
    if drs != None:
        st.metric(f":blue[Pessoas que vão para a DRS {resultados['Principal DRS de Saida']}]", f"{resultados['Pacientes na Mesma DRS']:,}".replace(',','.'))
with f:
    if drs != None:
        st.metric(f":blue[Distância média para a DRS {resultados['Principal DRS de Saida']}]", f"{resultados['Distância Média de Saída (km)']:,}".replace(',','.'))

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    left, right = st.columns([1, 2])
    left.space()
    right.markdown("# :orange[:material/directions_car:]")
with col2:
    st.metric('Distância média', f"{resultados['Distância Média (km)']} km", border=True)
with col3:
    st.metric('Distância mediana', f"{resultados['Distância Mediana (km)']} km", border=True)
with col4:
    st.metric('Tempo médio', f"{resultados['Tempo Médio (min)']} min", border=True)
with col5:
    st.metric('Tempo mediano', f"{resultados['Tempo Mediano (min)']} min", border=True)


col11, col12, col13, col14, col15 = st.columns(5)
with col11:
    left, right = st.columns([1, 2])
    left.space()
    right.markdown("# :orange[:material/directions_bus:]")
with col12:
    st.metric('Distância média', f"{resultados_o['Distância Média (km)']} km", border=True)
with col13:
    st.metric('Distância mediana', f"{resultados_o['Distância Mediana (km)']} km", border=True)
with col14:
    st.metric('Tempo médio', f"{resultados_o['Tempo Médio (min)']} min", border=True)
with col15:
    st.metric('Tempo mediano', f"{resultados_o['Tempo Mediano (min)']} min", border=True)

st.divider()

