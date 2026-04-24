import base64
import streamlit as st
import pandas as pd
import uuid
import re
from config.constants import SEXO, CATEATEND, COD_TOPOGRAFIAS, FAIXA_ETARIA, HABILIT_HOSP, TOPOGRAFIAS, ESTADIAMENTO_CLINICO, TIPO_DRS, DRS_DICT, ESCOLARIDADE 
from components.components import dicionario_dados
from st_functions import load_artifacts
from notebook import preprocessing
import matplotlib.pyplot as plt
import datetime
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
            
            sexo = st.radio('Sexo', SEXO.keys(), key=f"sexo_{ind_id}")

            ecgrup = st.pills(
                'Estadiamento Clínico',
                    list(ESTADIAMENTO_CLINICO.keys()),
                    selection_mode='single',
                    default='I',
                    key=f"ecgrup_{ind_id}"
            )
            
            topo = st.pills(
                'Topografia',
                    list(TOPOGRAFIAS.keys()),
                    selection_mode='single',
                    default='Próstata',
                    required=True,
                    key=f"topo_{ind_id}"
            )

            cod_topo = st.selectbox(
                label='Código da Topografia',
                options=list(COD_TOPOGRAFIAS[topo]),
                placeholder=f'Código da topografia de {topo.lower()}',
                index=None,
                key=f"cod_topo_{ind_id}"
            )
            
            cateaten = st.selectbox(
                label='Categoria de Atendimento',
                options=list(CATEATEND.keys()),
                placeholder=f'Selecione a categoria de atendimento',
                index=None,
                key=f"cateaten_{ind_id}"
            )

            habilit_hosp = st.selectbox(
                label='Habilitação do Hospital',
                options=list(HABILIT_HOSP.keys()),
                placeholder=f'Selecione a habilitação do hospital',
                index=None,
                key=f"habilit_hosp_{ind_id}"
            )

            instituicao = st.text_input(
                "Código da Instituição",
                placeholder="Formato 999999",
                key=f"institu_{ind_id}"
            )

            if instituicao:
                if not re.fullmatch(r"^\d+$", instituicao):
                    st.toast('Digite um código válido para :orange[Instituição]', icon=":material/warning:")

            escolaridade = st.selectbox(
                label="Escolaridade",
                options=ESCOLARIDADE.keys(),
                placeholder="Selecione a escolaridade",
                index=None,
                key=f"escolaridade_{ind_id}"
            )

            morfo = st.text_input(
                "Código da Morfologia",
                placeholder="Formato 99999",
                key=f"morfo_{ind_id}"
            )

            if morfo:
                if not re.fullmatch(r"\d{5}", morfo):
                    st.toast('Digite um código válido para :orange[Morfologia]', icon=":material/warning:")

            consult = st.date_input(
                "Data de Consulta",
                value="today",
                min_value=datetime.date(2000, 1, 1),
                max_value=None,
                format="DD/MM/YYYY",
                key=f"consult_{ind_id}"
            )

            diag = st.date_input(
                "Data de Diagnóstico",
                value="today",
                min_value=datetime.date(2000, 1, 1),
                max_value=None,
                format="DD/MM/YYYY",
                key=f"diag_{ind_id}"
            )

            trat = st.date_input(
                "Data de Tratamento",
                value="today",
                min_value=datetime.date(2000, 1, 1),
                max_value=None,
                format="DD/MM/YYYY",
                key=f"trat_{ind_id}"
            )

            tratcons = (trat - consult).days if trat and consult else None
            if tratcons is not None:
                tratcons = 3 if tratcons < 0 else 0 if tratcons <= 60 else 1 if tratcons <= 90 else 2
            diagtrat = (trat - diag).days if trat and diag else None
            if diagtrat is not None:
                diagtrat = 3 if diagtrat < 0 else 0 if diagtrat <= 60 else 1 if diagtrat <= 90 else 2
            diagprev = 1 if diag and consult and diag < consult else 0


            faixaetar = st.selectbox(
                label="Faixa Etária",
                options=FAIXA_ETARIA,
                placeholder="Selecione a faixa etária",
                index=None,
                key=f"faixaetar_{ind_id}"
            )

            drs = st.selectbox(
            label='DRS de Residência',
            options=DRS_DICT.keys(),
            placeholder=f'Selecione a DRS desejada',
            index=None,
            key=f"drs_{ind_id}"
            )

            drs_institu = st.selectbox(
            label='DRS de Hospital',
            options=DRS_DICT.keys(),
            placeholder=f'Selecione a DRS desejada',
            index=None,
            key=f"drs_inst_{ind_id}"
            )

            ibge = st.text_input(
                "Código IBGE do município de Residência",
                placeholder="Formato 9999999",
                key=f"ibge_{ind_id}"
            )

            if ibge:
                if not re.fullmatch(r"^\d+$", ibge):
                    st.toast('Digite um código válido para :orange[IBGE]', icon=":material/warning:")
            
            ibge_inst = st.text_input(
                "Código IBGE do município de Residência",
                placeholder="Formato 9999999",
                key=f"ibge_inst{ind_id}"
            )

            if ibge_inst:
                if not re.fullmatch(r"^\d+$", ibge_inst):
                    st.toast('Digite um código válido para :orange[IBGE da Instituição]', icon=":material/warning:")
            
            dist_carro = st.number_input(
                "Distância de carro da residência ao hospital (km)",
                min_value=0,
                max_value=500,
                value=None,
                key=f"dist_carro_{ind_id}"
            )

            tempo_carro = st.number_input(
                "Tempo de carro da residência ao hospital (min)",
                min_value=0,
                max_value=1000,
                value=None,
                key=f"tempo_carro_{ind_id}"
            )

            ivs_infra = st.number_input(
                "Índice de Vulnerabilidade Social do município - Infraestrutura Urbana",
                min_value=0.0,
                max_value=1.0,
                value=None,
                step=0.001,
                format="%.3f",
                key=f"ivs_infra_{ind_id}"

            )

            ivs_capital = st.number_input(
                "Índice de Vulnerabilidade Social do município - Capital Humano",
                min_value=0.0,
                max_value=1.0,
                value=None,
                step=0.001,
                format="%.3f",
                key=f"ivs_capital_{ind_id}"
            )

            ivs_renda = st.number_input(
                "Índice de Vulnerabilidade Social do município - Renda e Trabalho",
                min_value=0.0,
                max_value=1.0,
                value=None,
                step=0.001,
                format="%.3f",
                key=f"ivs_renda_{ind_id}"
            )



        with b:
            if st.button(':red[:material/delete:]', type='tertiary', key=f"delete_{idx}"):
                st.session_state.individuos.remove(ind_id)
                st.rerun()

        features = {
            "INSTITU": instituicao,
            "ESCOLARI": ESCOLARIDADE.get(escolaridade),
            "SEXO": SEXO.get(sexo),
            "IBGE": ibge,
            "CATEATEND": CATEATEND.get(cateaten),
            "DIAGPREV": diagprev,
            "TOPO": cod_topo,
            "MORFO": morfo,
            "ECGRUP": ecgrup,
            "ANODIAG": diag.year, 
            "FAIXAETAR": faixaetar,
            "DRS": DRS_DICT.get(drs),
            "IBGEATEN": ibge_inst,
            "DRS_INST": DRS_DICT.get(drs_institu),
            "HABILIT_HOSP": HABILIT_HOSP.get(habilit_hosp),
            "DISTANCIA_CARRO": dist_carro,
            "TEMPO_CARRO": tempo_carro,
            "TRATCONS_CAT": tratcons,
            "DIAGTRAT_CAT": diagtrat,
            "ivs_infraestrutura_urbana": ivs_infra,
            "ivs_capital_humano": ivs_capital,
            "ivs_renda_e_trabalho": ivs_renda,
            "topo": topo,
        }

        if any(campo in [None, ''] for campo in features.values()):
            return None
        return features

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

    dados = []
    cols = st.columns(MAX_INDIVIDUOS)

    for idx, ind_id in enumerate(st.session_state.individuos):
        with cols[idx]:
            ind = load_form(ind_id, idx)
            if ind:
                dados.append((ind))

    ###############################################

    artifacts = load_artifacts("models\colorretal.pkl")
    model = artifacts["best_model"]
    enc = artifacts["encoder"]
    norm = artifacts["normalizer"]


    ohe_list = ['CATEATEND', 'DIAGPREV', 'ECGRUP', 'TRATCONS_CAT', 'DIAGTRAT_CAT', 'HABILIT_HOSP', 'SEXO']

    te_list = ['INSTITU', 'ESCOLARI', 'IBGE', 'TOPO', 'MORFO', 'FAIXAETAR', 'DRS', 'IBGEATEN', 'DRS_INST', 'DISTANCIA_CARRO', 'TEMPO_CARRO', 'ivs_infraestrutura_urbana', 'ivs_capital_humano', 'ivs_renda_e_trabalho']

    df = pd.DataFrame(dados)

    if st.button('Comparar Sobrevida', type='primary'):
        
        df_processed = preprocessing.test_preprocessing(df, enc, norm, ohe_list, te_list)

        df_processed = df_processed.reindex(columns=artifacts["features"], fill_value=0)

        pred = model.predict(df_processed)
        surv_funcs = model.predict_survival_function(df_processed)

        # Criar figura
        fig, ax = plt.subplots()

        # Plotar cada curva
        for fn in surv_funcs:
            ax.plot(fn.x, fn.y)

        ax.set_title("Função de Sobrevivência")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Probabilidade de Sobrevivência")

        # Mostrar no Streamlit
        st.pyplot(fig)


    #################################################

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

    dicionario_dados(legenda='Cuidado com o preenchimento do arquivo. Se necessário, olhe o **dicionário dos dados**.', planilha=True)

    if arquivo:
        df = pd.read_csv(arquivo)

        # Validação simples
        colunas_esperadas = {"nome", "idade", "score"}
        if not colunas_esperadas.issubset(df.columns):
            st.error("O arquivo não contém as colunas esperadas.")
        else:
            st.success("Arquivo carregado com sucesso!")
            st.dataframe(df)

