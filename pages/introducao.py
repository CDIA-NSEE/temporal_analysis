import streamlit as st
from streamlit_carousel import carousel

st.set_page_config(layout='wide', page_title='Introdução', page_icon='midia/conecta-logo.png')

st.title('Introdução')

# ---------- dados ----------
integrantes = {

    "imt": {

        "Lucas Buk Cardoso": {
            "descrição": "Lucas Buk Cardoso é da Mauá",
            "foto": "midia/lucas.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/lucasbukcardoso/",
        },

        "Yasmin Pacheco Gil Bonilha": {
            "descrição": "Yasmin Pacheco Gil Bonilha é da Mauá",
            "foto": "midia/yasmin.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/yasminbonilha/",
        },

        "Vanderlei Cunha Parro": {
            "descrição": "Vanderlei Cunha Parro é da Mauá",
            "foto": "midia/vanderlei.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/vparro/",
        },
    
    },

    "fsp": {

        "Tatiana Natasha Toporcov":{
            "descrição":"Professora Associada da FSP-USP, coordenadora do projeto ConeCta-SP, com vasta experiência em epidemiologia do câncer e saúde pública.",
            "foto":"midia/tatiana.jpg",
            "orcid":"https://orcid.org/0000-0002-8929-5137",
            "lattes":"https://bv.fapesp.br/pt/pesquisador/50437/tatiana-natasha-toporcov/",
            "linkedin": "https://www.linkedin.com/in/tatiana-toporcov-6b94b3a/",
        },

        "Fernando Maia": {
            "descrição": "Médico Sanitarista, doutor em Saúde Coletiva e pós-doutourando no projeto ConeCta-SP.",
            "foto": "midia/fernando.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/fernando-maia-/",
        },

        "Simone Aldrey Angelo": {
            "descrição": "Pesquisadora do projeto ConeCta-SP na área de Ciência de Dados e Inteligência Artificial aplicada à saúde.",
            "foto": "midia/simone.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/simoneangelo/",
        },

    },

    "fosp": {

        "Adeylson Guimarães Ribeiro": {
            "descrição": "Subdiretor de Informação e Epidemiologia da FOSP.",
            "foto": "midia/adeylson.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/adeylson-ribeiro-phd-13169514/",
        },

    },

    "ac": {

        "Maria Paula Curado": {
            "descrição": "Chefe do Grupo de Epidemiologia e Estatística em Câncer (GEECAN).",
            "foto": "midia/maria_paula.jpg",
            "orcid": "https://orcid.org/0000-0002-8929-5137",
            "lattes": "https://orcid.org/0000-0002-8929-5137",
            "linkedin": "https://www.linkedin.com/in/maria-curado-54ba60105/",
        },

        "Gisele Aparecida Fernandes": {
            "descrição": "Pesquisadora e Epidemiologista no A.C. Camargo Cancer Center.",
            "foto": "midia/gisele.jpg",
            "orcid": "",
            "lattes": "",
            "linkedin": "https://www.linkedin.com/in/gisele-fernandes-0b289553/",
        },

    }

}

st.header('O Projeto ConeCta-SP', divider='blue')

st.write('''
        \t O Projeto **ConeCta-SP** (Controle do Câncer no Estado de São Paulo: do conhecimento à ação) é uma iniciativa sediada na Fundação Oncocentro de São Paulo (FOSP), com financiamento da FAPESP e da Secretaria de Estado da Saúde de São Paulo (SES/SP), reúne diversas instituições de referência em saúde pública, epidemiologia e tecnologia com o propósito de gerar conhecimento robusto e subsidiar ações de prevenção, controle e gestão do câncer no Sistema Único de Saúde (SUS).
         
         No atual contexto de crescente incidência e mortalidade por câncer, o projeto está estruturado em dois eixos complementares de pesquisa e ação. Este site destina-se a divulgar e apresentar os estudos desenvolvidos no âmbito do Eixo 2 – **“Inteligência Artificial na predição de sobrevida de pacientes com câncer no período da epidemia da COVID-19 e anos não epidêmicos”** – realizados a partir da integração de informações do Registro Hospitalar de Câncer do Estado de São Paulo (RHC-SP) com metodologias avançadas de análise, em parceria com o Instituto Mauá de Tecnologia (IMT) e outras instituições acadêmicas e de pesquisa.

''')

st.write('\n\n')
st.subheader('Nossos Objetivos')

st.write('''
         
         As investigações aqui descritas buscam explorar diferentes dimensões do cuidado oncológico, sempre respeitando os limites metodológicos e interpretativos dos dados disponíveis. Dessa forma, é possível não apenas descrever e interpretar padrões observados, mas também fornecer insumos que *possam apoiar decisões de políticas públicas, melhorar a coordenação dos serviços oncológicos e, em última instância, contribuir para a melhora dos resultados em saúde da população paulista*. A produção e a divulgação científica desses estudos objetivam ampliar a compreensão pública e técnica sobre o câncer e fortalecer as estratégias de prevenção e cuidado em saúde no estado.
''')

st.write('\n\n')
st.subheader('Integrantes do Projeto', divider='blue')
st.write('\n\n')

# ---------- imt ----------

st.subheader("Instituto Mauá de Tecnologia (IMT)")

for chave in integrantes["imt"].keys():
    with st.popover(chave, type="tertiary"):
        a, b = st.columns([1, 4])
        with a:
            st.image(integrantes["imt"][chave]["foto"], width=150)
        with b:
            st.write(integrantes["imt"][chave]["descrição"])
            st.write(f"[Lattes]({integrantes['imt'][chave]['lattes']}) | [ORCID]({integrantes['imt'][chave]['orcid']}) | [LinkedIn]({integrantes['imt'][chave]['linkedin']})")

# ---------- fsp ----------

st.subheader("Faculdade de Saúde Pública da Universidade de São Paulo (FSP-USP)")

for chave in integrantes["fsp"].keys():
    with st.popover(chave, type="tertiary"):
        a, b = st.columns([1, 4])
        with a:
            st.image(integrantes["fsp"][chave]["foto"], width=150)
        with b:
            st.write(integrantes["fsp"][chave]["descrição"])
            st.write(f"[Lattes]({integrantes['fsp'][chave]['lattes']}) | [ORCID]({integrantes['fsp'][chave]['orcid']}) | [LinkedIn]({integrantes['fsp'][chave]['linkedin']})")

# ---------- fosp ----------

st.subheader("Informação e Epidemiologia - Fundação Oncocentro de São Paulo (FOSP)")


for chave in integrantes["fosp"].keys():
    with st.popover(chave, type="tertiary"):
        a, b = st.columns([1, 4])
        with a:
            st.image(integrantes["fosp"][chave]["foto"], width=150)
        with b:
            st.write(integrantes["fosp"][chave]["descrição"])
            st.write(f"[Lattes]({integrantes['fosp'][chave]['lattes']}) | [ORCID]({integrantes['fosp'][chave]['orcid']}) | [LinkedIn]({integrantes['fosp'][chave]['linkedin']})")

# ---------- ac ----------

st.subheader("Epidemiologia e Estatística em Câncer (GEECAN) - A.C. Camargo Cancer Center")

for chave in integrantes["ac"].keys():
    with st.popover(chave, type="tertiary"):
        a, b = st.columns([1, 4])
        with a:
            st.image(integrantes["ac"][chave]["foto"], width=150)
        with b:
            st.write(integrantes["ac"][chave]["descrição"])
            st.write(f"[Lattes]({integrantes['ac'][chave]['lattes']}) | [ORCID]({integrantes['ac'][chave]['orcid']}) | [LinkedIn]({integrantes['ac'][chave]['linkedin']})")


