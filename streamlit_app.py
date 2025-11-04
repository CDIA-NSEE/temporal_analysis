import streamlit as st

pg = st.navigation([st.Page(page='introducao.py', title='Introdução', default=True), st.Page(page="analises_temporais.py", title= 'Análises Temporais', url_path='analises_temporais'), st.Page(page="analises_distancia_tempo.py", title='Análises de Distâncias e Tempos', url_path='distancias_tempos')])
pg.run()