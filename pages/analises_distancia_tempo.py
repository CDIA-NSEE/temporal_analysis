from numpy import dtype
import streamlit as st
from st_functions import filter_data, load_data, load_map_pydeck
from streamlit_folium import st_folium
from notebook.dt import caracteristicas_drs, estatisticas_ec, boxplots_ec
from config.constants import TOPOGRAFIAS, ESTADIAMENTO_CLINICO, TIPO_DRS, DRS_DICT 

st.set_page_config(layout='wide', page_title='Análises de Distâncias e Tempos', page_icon='midia/conecta-logo.png')

st.title('Análises de Distâncias e Tempos')

# ---------- dados ----------

#o dataset utilizado para as análises desta página se encontra disponível no notebook 'Modelos para cada tipo.ipynb', na pasta 'Cenários' (Banco de dados único simplificado - distâncias e tempos).
df = load_data(
    file_path=r'datasets/dt_simp.csv', 
    dtype={'CEP':str, 'CEP_HOSP':str},
    date_cols=['DTCONSULT', 'DTDIAG', 'DTTRAT', 'DTULTINFO'],
)

topografias = {
    'Todas': ['C18', 'C19', 'C20', 'C34', 'C50', 'C53', 'C61'],
    **TOPOGRAFIAS
    }

estadiamento_clinico = {
    'Todos': ['I', 'II', 'III', 'IV'],
    **ESTADIAMENTO_CLINICO
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
        st.write(':small[Pacientes com] :blue-badge[Confirmação microscópica] :green-badge[Mais de 19 anos] :orange-badge[Atendidos no SUS] :violet-badge[Atendimento em CACONs ou UNACONs]')

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
            options=TIPO_DRS.keys(),
            horizontal=True,
            label_visibility='collapsed',
            index = 0,
        )
        t_drs = TIPO_DRS[d]

        drs = st.selectbox(
            label='DRS',
            options=DRS_DICT.keys(),
            placeholder=f'Selecione a DRS desejada',
            index=None,
        )
        drs = DRS_DICT[drs] if drs != None else None

        st.write('\n')

        c1, c2 = st.columns(2)
        with c1:
            with st.container(horizontal=True):
                st.space('stretch')
                submitted = st.form_submit_button("Aplicar Filtros", type='secondary')

        if submitted:
            st.toast('Filtros aplicados com sucesso!', icon=':material/filter_list:', duration='short')


    fdf = filter_data(df, topografias[topo], estadiamento_clinico[estadiamento], drs, t_drs)
    resultados = caracteristicas_drs(fdf, drs, t_drs, 'CARRO')
    resultados_o = caracteristicas_drs(fdf, drs, t_drs, 'TRANSP')

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

    titulo_ec = 'Todos os Estadiamentos Clínicos' if estadiamento == 'Todos' else f'Estadiamento Clínico {estadiamento}'

    titulo_topo = 'Todas as Topografias' if topo == 'Todas' else f'{topo}'
    
    st.subheader(f'Descrição por {titulo_ec}, {titulo_topo}, {resultados['nome_drs']}')
    st.write('\n\n')

    est_ec = estatisticas_ec(fdf, 'DISTANCIA_CARRO')
    st.dataframe(
        est_ec,
        hide_index=True,
    )

    # ---------- boxplots ----------
    st.space('medium')
    st.subheader(f'Boxplots de Distância por {titulo_ec}, {titulo_topo}, {resultados['nome_drs']}')
    boxplots = boxplots_ec(fdf, estadiamento_clinico[estadiamento], 'DISTANCIA_CARRO', 'Estadiamento Clínico')
    st.plotly_chart(boxplots)

    # ---------- mapa ----------

    # st.subheader('Mapa das DRS do Estado de São Paulo')
    # st.write('\n')
    # deck = load_map_pydeck()
    # st.pydeck_chart(deck)

with metod:
   st.markdown('O banco de dados utilizado para as análises desta página foi manipulado da seguinte forma:')

   # seleções gerais
   st.subheader(':blue[Seleções Clínicas]', divider='blue')
   st.markdown('##### **:blue[Gerais]**')
   st.markdown(' - Retirada de morfologias com final *2* ou *9*;')
   st.write('Pacientes com:')
   with st.container(horizontal=True):
       st.space('small')
       st.markdown(' - Confirmação microscópica; \n - Mais de 19 anos; \n - Atendidos no SUS; \n - Atendimento em CACONs ou UNACONs;')

   # selecões específicas
   st.markdown('##### **:blue[Específicas]**')

   with st.expander('Próstata', expanded=False):
       st.markdown(' - Topografia *C61*')
    
   with st.expander('Pulmão', expanded=False):
       st.markdown(' - Topografia *C34* \n - Pacientes sem recebimento de hormonioterapia')

   with st.expander('Mama', expanded=False):
       st.markdown(' - Topografia *C50* \n - Pacientes do sexo feminino')

   with st.expander('Colorretal', expanded=False):
       st.markdown(' - Topografia *C18*, *C19* ou *C20* \n - Morfologia *81403*')
    
   with st.expander('Colo do Útero', expanded=False):
       st.markdown(' - Topografia *C53*')

   # manipulação dos dados de distâncias e tempos
   st.space('small')
   st.subheader(':orange[Manipulação dos dados de Distâncias e Tempos]', divider='orange')
   st.markdown('As informações relativas aos CEPs dos pacientes, ainda que anonimizadas, foram obtidas mediante aprovação do Comitê de Ética da Faculdade de Saúde Pública da Universidade de São Paulo (FSP-USP). As distâncias entre os CEPs residenciais e hospitalares para todos os CEPs válidos foram calculadas através da [API Distance Matrix](https://developers.google.com/maps/documentation/distance-matrix/overview?hl=pt-br), do *Google Maps Platform*, utilizando o método de transporte `\'driving\'` como padrão. Os pacientes cujo trajeto não pode ser encontrado pela API foram retirados da base de dados.')




