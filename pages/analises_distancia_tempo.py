import streamlit as st

st.set_page_config(layout='wide', page_title='Análises de Distâncias e Tempos', page_icon='midia\conecta-logo.png')

st.title('Análises de Distâncias e Tempos')
st.divider()

# ---------- dados ----------

df = pd.read_csv(r'datasets\dt_simp.csv', dtype={'CEP':str, 'CEP_HOSP':str})