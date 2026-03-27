import base64
import streamlit as st
import pandas as pd
import uuid
import re
from config.constants import TOPOGRAFIAS, ESTADIAMENTO_CLINICO, TIPO_DRS, DRS_DICT
from components.components import dicionario_dados
# from streamlit_folium import st_folium

st.set_page_config(layout='wide', page_title='Modelos de Sobrevida', page_icon='midia/conecta-logo.png')

st.markdown(
    '# Predição com Modelos de Sobrevida',
    #text_alignment='center'
)
st.divider()

# ---------- constantes ----------

MAX_INDIVIDUOS = 4

# ---------- sessões de estado e funções ----------

if 'individuos' not in st.session_state:
    st.session_state.individuos = [str(uuid.uuid4())]

if 'visibilidade_container' not in st.session_state:
    st.session_state.visibilidade_container = True

if 'visibilidade_manual' not in st.session_state:
    st.session_state.visibilidade_manual = False

if 'visibilidade_csv' not in st.session_state:
    st.session_state.visibilidade_csv = False

def load_form(ind_id, idx):

    if idx >= MAX_INDIVIDUOS:
        st.error(f"O número máximo de indivíduos é {MAX_INDIVIDUOS}.")
        return None
    
    with st.expander(f"Indivíduo {idx+1}", expanded=True):
        a, b = st.columns([0.9, 0.1])

        with a:
            
            sexo = st.radio('Sexo', ['Masculino', 'Feminino'], key=f"sexo_{ind_id}")
            
            topo = st.pills(
                'Topografia',
                    list(TOPOGRAFIAS.keys()),
                    selection_mode='single',
                    default='Próstata',
                    key=f"topo_{ind_id}"
            )

            idade = st.number_input(
                "Idade",
                min_value=0,
                max_value=110,
                key=f"idade_{ind_id}"
            )

            instituicao = st.text_input(
                "Código da Instituição",
                placeholder="Formato 999999",
                key=f"institu_{ind_id}"
            )

            if instituicao:
                if not re.fullmatch(r"\d{6}", instituicao):
                    st.toast('Digite um código válido', icon=":material/warning:")
            
            # escolaridade = 


        with b:
            if st.button(':red[:material/delete:]', type='tertiary', key=f"delete_{idx}"):
                st.session_state.individuos.remove(ind_id)
                st.rerun()

        return {
            "sexo": sexo,
            "idade": idade,
        }

# ---------- interface ----------

if st.session_state.visibilidade_container:

    with st.container(horizontal_alignment='left'):

        with st.popover(':orange[:material/add_circle: Adicionar Indivíduos para Comparação]', type='tertiary'):
            if st.button('Adicionar indivíduo manualmente (até 04 indivíduos)', type='tertiary'):
                 st.session_state.visibilidade_container = False
                 st.session_state.visibilidade_manual = True
                 st.rerun()
            
            if st.button('Adicionar arquivo .csv', type='tertiary'):
                st.session_state.visibilidade_container = False
                st.session_state.visibilidade_csv = True
                st.rerun()

# ---------- formulário manual ----------

if st.session_state.visibilidade_manual:

    a, b = st.columns([0.01, 0.99])

    # boão de voltar e botão de adicionar indivíduos
    with a:
        if st.button(':material/chevron_backward:', type='tertiary'):
            st.session_state.visibilidade_manual = False
            st.session_state.visibilidade_container = True
            st.rerun()
    
    with b:
        if st.button(':orange[:material/add_circle: Adicionar novo indivíduo]', type='secondary') and len(st.session_state.individuos) < MAX_INDIVIDUOS:
            st.session_state.individuos.append(str(uuid.uuid4()))
        else:
            if len(st.session_state.individuos) == MAX_INDIVIDUOS:
                st.toast(f"O número máximo de indivíduos é {MAX_INDIVIDUOS}.", icon=':material/warning:', duration=2)

    dicionario_dados(legenda='**Dicionário dos dados**')

    dados = []
    cols = st.columns(MAX_INDIVIDUOS)

    for idx, ind_id in enumerate(st.session_state.individuos):
        with cols[idx]:
            ind = load_form(ind_id, idx)
            if ind:
                dados.append((ind_id, idx))

# ---------- upload do arquivo. csv ----------

if st.session_state.visibilidade_csv:

    modelo = pd.DataFrame({'INSTITU': [22128], 'ESCOLARI': [2],  'IBGE': [3556107], 'TOPO': ['C18'], 'MORFO': [81403], 'ANODIAG': [2022], 'FAIXAETAR': ['70+'],
       'DRS': [15], 'IBGEATEN': [3549805], 'DRS_INST': [15], 'DISTANCIA_CARRO': [96.1], 'TEMPO_CARRO': [70],
       'ivs_infraestrutura_urbana': [0.0], 'ivs_capital_humano': [0.249],
       'ivs_renda_e_trabalho': [0.205]})
    
    
    csv = modelo.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="comparacao_sobrevida.csv">aqui</a>'

    
    a, b = st.columns([0.01, 0.99])

    with a:
        if st.button(':material/chevron_backward:', type='tertiary'):
            st.session_state.visibilidade_csv = False
            st.session_state.visibilidade_container = True
            st.rerun()
    
    with b:
        with st.container(horizontal_alignment='center'):
            st.markdown(f" :blue-background[ :blue[:material/info:] **Baixe o modelo de arquivo .csv {href} e faça o upload do arquivo preenchido.** ]", unsafe_allow_html=True)

    st.space(size='small')

    arquivo = st.file_uploader(
        "Envie o arquivo .csv preenchido:",
        type=["csv"]
    )
    st.space(size='small')

    dicionario_dados(legenda='Cuidado com o preenchimento do arquivo. Se necessário, olhe o **dicionário dos dados**.')

    if arquivo:
        df = pd.read_csv(arquivo)

        # Validação simples
        colunas_esperadas = {"nome", "idade", "score"}
        if not colunas_esperadas.issubset(df.columns):
            st.error("O arquivo não contém as colunas esperadas.")
        else:
            st.success("Arquivo carregado com sucesso!")
            st.dataframe(df)

