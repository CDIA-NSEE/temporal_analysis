import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout='wide', page_title='Modelos de Sobrevida', page_icon='midia/conecta-logo.png')

st.title('Predição com Modelos de Sobrevida')
st.divider()

# ---------- constantes ----------

MAX_INDIVIDUOS = 4

# ---------- sessões de estado e funções ----------

if 'individuos' not in st.session_state:
    st.session_state['individuos'] = [0]

def load_form(idx):

    if idx >= MAX_INDIVIDUOS:
        st.error(f"O número máximo de indivíduos é {MAX_INDIVIDUOS}.")
        return None
    
    with st.expander(f"Indivíduo {idx+1}", expanded=True):
        a, b = st.columns([0.9, 0.1])

        with a:
            nome = st.text_input(
                "Nome",
                key=f"nome_{idx}"
            )

            idade = st.number_input(
                "Idade",
                min_value=0,
                max_value=120,
                key=f"idade_{idx}"
            )

            score = st.slider(
                "Score",
                0, 100,
                key=f"score_{idx}"
            )
        with b:
            delete = st.button(
            ':red[:material/delete:]',
            type='tertiary',
            key=f"delete_{idx}"
        ),

        return {
            "nome": nome,
            "idade": idade,
            "score": score
        }

# ---------- interface ----------

with st.popover(':orange[:material/add_circle: Adicionar Indivíduos para Comparação]', type='tertiary'):
    if st.button('Adicionar indivíduo manualmente', type='tertiary'):
        if len(st.session_state.individuos) < MAX_INDIVIDUOS:
            st.session_state.individuos.append(len(st.session_state.individuos))
        else:
            st.warning(f"O número máximo de indivíduos é {MAX_INDIVIDUOS}.")
    
    if st.button('Adicionar arquivo .csv', type='tertiary'):
        st.write('implementing...')

dados = []
cols = st.columns(MAX_INDIVIDUOS)

for i in range(len(st.session_state.individuos)):
    with cols[i]:
        ind = load_form(i)
        if ind:
            dados.append(ind)

# if len(dados) > 1:
#     st.subheader("Comparação")

#     cols = st.columns(len(dados))

#     for col, dado in zip(cols, dados):
#         with col:
#             st.metric("Idade", dado["idade"])
#             st.metric("Score", dado["score"])

