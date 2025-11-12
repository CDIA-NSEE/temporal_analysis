import streamlit as st

pg = st.navigation([st.Page(page='introducao.py', title='Introdução', url_path='introducao', default=False,), st.Page(page="analises_temporais.py", title= 'Análises Temporais', url_path='analises_temporais', default=True), st.Page(page="analises_distancia_tempo.py", title='Análises de Distâncias e Tempos', url_path='distancias_tempos')])
pg.run()