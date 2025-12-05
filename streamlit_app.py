import streamlit as st

pg = st.navigation([st.Page(page=r'pages\introducao.py', title='Introdução', url_path='introducao', default=False,), st.Page(page=r"pages\analises_temporais.py", title= 'Análises Temporais', url_path=r'pages\introducao.py', default=True), st.Page(page=r"pages\analises_distancia_tempo.py", title='Análises de Distâncias e Tempos', url_path='distancias_tempos')])
pg.run()