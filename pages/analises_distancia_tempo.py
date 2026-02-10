from numpy import dtype
import streamlit as st
from st_functions import load_data, load_map_pydeck
from streamlit_folium import st_folium
from notebook.dt import caracteristicas_drs, estatisticas_ec, boxplots_ec

st.set_page_config(layout='wide', page_title='Análises de Distâncias e Tempos', page_icon='midia/conecta-logo.png')

st.title('Análises de Distâncias e Tempos')

# ---------- dados ----------

df = load_data(
    file_path=r'datasets/dt_simp.csv', 
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

drs_dict = {
    "Capital": 1,
    "Interior": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
    "DRS 1 - Grande São Paulo": 1,
    "DRS 2 - Araçatuba": 2,
    "DRS 3 - Araraquara": 3,
    "DRS 4 - Baixada Santista": 4,
    "DRS 5 - Barretos": 5,
    "DRS 6 - Bauru": 6,
    "DRS 7 - Campinas": 7,
    "DRS 8 - Franca": 8,
    "DRS 9 - Marília": 9,
    "DRS 10 - Piracicaba": 10,
    "DRS 11 - Presidente Prudente": 11,
    "DRS 12 - Registro": 12,
    "DRS 13 - Ribeirão Preto": 13,
    "DRS 14 - São João da Boa Vista": 14,
    "DRS 15 - São José do Rio Preto": 15,
    "DRS 16 - Sorocaba": 16,
    "DRS 17 - Taubaté": 17
}

# ---------- funções de exibição ----------

def metricas(resultados):
    a, b, c, d, e = st.columns(5)
    with a:
        st.metric(':orange[Total de Pacientes]', f"{resultados['total_pacientes']:,}".replace(',','.'), )
    
    if resultados['metricas']:
        with b:
            st.metric(f":orange[Pacientes que se tratam na {resultados['nome_drs']}]", f"{resultados['mesma_drs']:,}".replace(',','.'))
        with c:
            st.metric(f":blue[Pessoas que vão para a DRS {resultados['principal_drs_saida']}]", f"{resultados['qtd_princ_drs_saida']:,}".replace(',','.'))
        with d:
            st.metric(f":blue[Distância média para a DRS {resultados['principal_drs_saida']}]", f"{resultados['dist_media_principal']:,} km".replace(',','.'))

def metricas_transporte(resultados):
    icone = ':material/directions_car:' if resultados['transp'] == 'CARRO' else ':material/directions_bus:'

    a, b, c, d, e= st.columns(5)
    with a:
        left, right = st.columns([1, 2])
        left.space()
        right.markdown(f"# :orange[{icone}]")
    with b:
        st.metric('Distância média', f"{resultados['dist_media']} km", border=True)
    with c:
        st.metric('Distância mediana', f"{resultados['dist_mediana']} km", border=True)
    with d:
        st.metric('Tempo médio', f"{resultados['tempo_medio']} min", border=True)
    with e:
        st.metric('Tempo mediano', f"{resultados['tempo_mediano']} min", border=True)


# ---------- página ----------

analises, metod = st.tabs(['Análises', 'Metodologia'], default='Análises') 

with analises:
        
    # ---------- formulário ----------

    with st.container(horizontal=True, horizontal_alignment="left"):
        st.write(':blue-badge[Confirmação microscópica] :green-badge[Mais de 19 anos] :orange-badge[Atendidos no SUS]')




    with st.form(key="filtros", enter_to_submit=True, border=True):
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
        t_drs = tipo_drs[d]

        drs = st.selectbox(
            label='DRS',
            options=drs_dict.keys(),
            placeholder=f'Selecione a DRS desejada',
            index=None,
        )
        drs = drs_dict[drs] if drs != None else None

        st.write('\n')

        c1, c2 = st.columns(2)
        with c1:
            with st.container(horizontal=True):
                st.space('stretch')
                submitted = st.form_submit_button("Aplicar Filtros", type='secondary')

        if submitted:
            st.toast('Filtros aplicados com sucesso!', icon=':material/filter_list:', duration='short')


    resultados = caracteristicas_drs(df, topografias[topo], estadiamento_clinico[estadiamento], drs, t_drs, 'CARRO')
    resultados_o = caracteristicas_drs(df, topografias[topo], estadiamento_clinico[estadiamento], drs, t_drs, 'TRANSP')

    # ---------- métricas ----------

    st.divider()

    if drs != None:
        st.header(f"{resultados['nome_drs']}")
        st.badge(f"Principal DRS externa para tratamento: DRS {resultados['principal_drs_saida']}", color='blue', icon=':material/fluid_med:')

    st.space(size='medium')
    metricas(resultados)

    st.divider()

    metricas_transporte(resultados)
    metricas_transporte(resultados_o)

    st.divider()

    # ---------- tabela - estatísticas por estadiamento clínico----------

    st.subheader(f'Descrição por Estadiamento Clínico - {resultados['nome_topo']}, {resultados['nome_drs']}')
    st.write('\n\n')

    est_ec = estatisticas_ec(df, topografias[topo], drs, t_drs, 'DISTANCIA_CARRO')
    st.dataframe(
        est_ec,
        hide_index=True,
    )

    # ---------- boxplots ----------
    st.space('medium')
    st.subheader(f'Boxplots de Distância por Estadiamento Clínico - {resultados['nome_topo']}, {resultados['nome_drs']}')
    boxplots = boxplots_ec(df, topografias[topo], drs, t_drs, 'DISTANCIA_CARRO', 'Estadiamento Clínico')
    st.plotly_chart(boxplots)

    # ---------- mapa ----------

    # st.subheader('Mapa das DRS do Estado de São Paulo')
    # st.write('\n')
    # deck = load_map_pydeck()
    # st.pydeck_chart(deck)
