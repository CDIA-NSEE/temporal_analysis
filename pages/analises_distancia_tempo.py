import streamlit as st
from st_functions import load_data

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

drs = st.multiselect(
    label='DRS',
    options=sorted(df[tipo_drs[d]].unique()),
    placeholder=f'Selecione as {d} desejadas',
)
