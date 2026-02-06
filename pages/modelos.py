import base64
import streamlit as st
import pandas as pd
import uuid
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

            idade = st.number_input(
                "Idade",
                min_value=0,
                max_value=120,
                key=f"idade_{ind_id}"
            )

            score = st.slider(
                "Score",
                0, 100,
                key=f"score_{idx}"
            )
        with b:
            if st.button(':red[:material/delete:]', type='tertiary', key=f"delete_{idx}"):
                st.session_state.individuos.remove(ind_id)
                st.rerun()

        return {
            "sexo": sexo,
            "idade": idade,
            "score": score
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
                dados.append((ind_id, idx))

# ---------- upload do arquivo. csv ----------

if st.session_state.visibilidade_csv:

    modelo = pd.DataFrame({'INSTITU': [22128], 'ESCOLARI': [2],  'IBGE': [3556107], 'TOPO': ['C18'], 'MORFO': [81403], 'ANODIAG': [2022], 'FAIXAETAR': ['70+'],
       'DRS': [15], 'IBGEATEN': [3549805], 'DRS_INST': [15], 'DISTANCIA_CARRO': [96.1], 'TEMPO_CARRO': [70],
       'ivs_infraestrutura_urbana': [0.0], 'ivs_capital_humano': [0.249],
       'ivs_renda_e_trabalho': [0.205]})
    
    dic_nomes = [

        'INSTITU', 'ESCOLARI',  'IBGE', 'TOPO', 'MORFO',
        'ANODIAG', 'FAIXAETAR', 'DRS', 'IBGEATEN', 'DRS_INST',
        'DISTANCIA_CARRO', 'TEMPO_CARRO', 'ivs_infraestrutura_urbana', 'ivs_capital_humano', 'ivs_renda_e_trabalho'
    
    ]

    dic_tipo = [
        'int64', 'int64', 'int64', 'string', 'int64',
        'int64', 'string', 'int64', 'int64', 'int64',
        'float64', 'int64', 'float64', 'float64', 'float64'
    ]
    
    dic_desc = [

                'Código da Instituição. Código de seis dígitos no formato 999999.',
                'Código para a escolaridade do paciente. Domínio: 1 - Analfabeto, 2 - Ens. Fundamental Incompleto, 3 - Ens. Fundamental Completo, 4 - Ens. Médio, 5 - Ens. Superior, 9 - Ignorado.', 
                'Código do município de residência do paciente, conforme tabela do IBGE. Código de sete dígitos no formato 9999999.',
                'Código da topografia do tumor, conforme CID-O-3, no formato C99',
                'Código da morfologia do tumor, conforme CID-O-3, no formato 99999.',
                'Ano de diagnóstico do câncer, no formato 9999.',
                'Faixa etária do paciente no momento do diagnóstico, no formato. Domínio: \'20-29\', \'30-39\', \'40-49\', \'50-59\', \'60-69\', \'70+\'',
                'Código do Departamento Regional de Saúde (DRS) do paciente.',
                'Código do município de atendimento do paciente, conforme tabela do IBGE. Código de sete dígitos no formato 9999999.',
                'Código do Departamento Regional de Saúde (DRS) da Instituição.',
                'Distância entre o município de residência e o município de atendimento, em quilômetros.',
                'Tempo necessário para deslocamento entre o município de residência e o município de atendimento, em minutos.',
                'Dimensão de Infraestrutua Urbana do Índice de Vulnerabilidade Social (IVS). Formato decimal.',
                'Dimensão de Capital Humano do Índice de Vulnerabilidade Social (IVS). Formato decimal.',
                'Dimensão de Renda e Trabalho do Índice de Vulnerabilidade Social (IVS). Formato decimal.',

    ]



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

    with st.expander('Cuidado com o preenchimento do arquivo. Se necessário, olhe o **dicionário dos dados**.'):
        st.table(pd.DataFrame({
            'Nome da Coluna': dic_nomes,
            'Tipo de Dado': dic_tipo,
            'Descrição': dic_desc
        }).set_index('Nome da Coluna'))

    if arquivo:
        df = pd.read_csv(arquivo)

        # Validação simples
        colunas_esperadas = {"nome", "idade", "score"}
        if not colunas_esperadas.issubset(df.columns):
            st.error("O arquivo não contém as colunas esperadas.")
        else:
            st.success("Arquivo carregado com sucesso!")
            st.dataframe(df)

