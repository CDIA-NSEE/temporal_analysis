import streamlit as st

pg = st.navigation(
    [
        st.Page(page=r'pages/introducao.py', title='Introdução', url_path='introducao', default=True,), 
        st.Page(page=r"pages/analises_temporais.py", title= 'Análises Temporais', url_path='analises_temporais', default=False), 
        st.Page(page=r"pages/analises_distancia_tempo.py", title='Análises de Distâncias e Tempos', url_path='distancias_tempos'), 
        st.Page(page=r"pages/modelos.py", title='Modelos de Sobrevida', url_path='modelos'),
    ])
pg.run()