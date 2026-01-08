import streamlit as st
from streamlit_carousel import carousel

st.set_page_config(layout='wide', page_title='Introdução', page_icon='midia/conecta-logo.png')

st.title('Introdução')

st.subheader('O Projeto ConeCta-SP', divider='blue')

st.write('''
        \t O Projeto **ConeCta-SP** (Controle do Câncer no Estado de São Paulo: do conhecimento à ação) é uma iniciativa sediada na Fundação Oncocentro de São Paulo (FOSP), com financiamento da FAPESP e da Secretaria de Estado da Saúde de São Paulo (SES/SP), reúne diversas instituições de referência em saúde pública, epidemiologia e tecnologia com o propósito de gerar conhecimento robusto e subsidiar ações de prevenção, controle e gestão do câncer no Sistema Único de Saúde (SUS).
         
         No atual contexto de crescente incidência e mortalidade por câncer, o projeto está estruturado em dois eixos complementares de pesquisa e ação. Este site destina-se a divulgar e apresentar os estudos desenvolvidos no âmbito do Eixo 2 – **“Inteligência Artificial na predição de sobrevida de pacientes com câncer no período da epidemia da COVID-19 e anos não epidêmicos”** – realizados a partir da integração de informações do Registro Hospitalar de Câncer do Estado de São Paulo (RHC-SP) com metodologias avançadas de análise, em parceria com o Instituto Mauá de Tecnologia (IMT) e outras instituições acadêmicas e de pesquisa.

''')

st.write('\n\n')
st.subheader('Nossos Objetivos', divider='blue')

st.write('''
         
         As investigações aqui descritas buscam explorar diferentes dimensões do cuidado oncológico, sempre respeitando os limites metodológicos e interpretativos dos dados disponíveis. Dessa forma, é possível não apenas descrever e interpretar padrões observados, mas também fornecer insumos que *possam apoiar decisões de políticas públicas, melhorar a coordenação dos serviços oncológicos e, em última instância, contribuir para a melhora dos resultados em saúde da população paulista*. A produção e a divulgação científica desses estudos objetivam ampliar a compreensão pública e técnica sobre o câncer e fortalecer as estratégias de prevenção e cuidado em saúde no estado.
''')

st.write('\n\n')
st.subheader('Integrantes do Projeto', divider='blue')
st.write('\n\n')

pessoas = [
    dict(
        img='midia/tati.jpg',
        title='Tati',
        text='Tati é da FSP.',
    ),
    dict(
        img='midia/lucas.jpg',
        title='Lucas',
        text='Lucas é do IMT.',
    ),
    dict(
        img='midia/simone.jpg',
        title='Simone',
        text='A Simone é da FSP.',
    )
]

carousel(items=pessoas, slide=True, pause='hover', container_height=350, width=0.5)

st.caption('(podemos fazer desse jeito ou uma galeria lado a lado e dividir por equipes)')