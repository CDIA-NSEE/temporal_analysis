import streamlit as st
from streamlit_carousel import carousel

st.set_page_config(layout='wide', page_title='Introdução', page_icon='midia/conecta-logo.png')

st.title('Introdução')

# ---------- dados ----------
integrantes = {

    "imt": {

        "Vanderlei Cunha Parro": {
            "descrição": "Doutor em Engenharia com consolidada trajetória em Engenharia de Sistemas, Instrumentação Astronômica e Ciência de Dados.",
            "foto": "midia/vanderlei.jpg",
            "orcid": "https://orcid.org/0000-0002-8232-0125",
            "lattes": "http://lattes.cnpq.br/5302657052708622",
            "linkedin": "https://www.linkedin.com/in/vparro/",
        },

        "Lucas Buk Cardoso": {
            "descrição": "Doutorando em Engenharia Elétrica. Lidera a participação do NSEE no projeto ConeCta-SP.",
            "foto": "midia/lucas.jpg",
            "orcid": "https://orcid.org/0009-0003-0328-4803",
            "lattes": "http://lattes.cnpq.br/5417608945198427",
            "linkedin": "https://www.linkedin.com/in/lucasbukcardoso/",
        },

        "Yasmin Pacheco Gil Bonilha": {
            "descrição": "Graduanda em Ciência da Computação pelo IMT. Estagiária do NSEE, atuando no projeto ConeCta-SP.",
            "foto": "midia/yasmin.jpg",
            "orcid": "https://orcid.org/0009-0001-6784-4078",
            "lattes": "",
            "linkedin": "https://www.linkedin.com/in/yasminbonilha/",
        },
    
    },

    "fsp": {

        "Tatiana Natasha Toporcov":{
            "descrição":"Professora Associada do Departamento de Epidemiologia da FSP-USP e pesquisadora principal do projeto ConeCta-SP.",
            "foto":"midia/tatiana.jpg",
            "orcid":"https://orcid.org/0000-0002-8929-5137",
            "lattes":"http://lattes.cnpq.br/5345064895953228",
            "linkedin": "https://www.linkedin.com/in/tatiana-toporcov-6b94b3a/",
        },

        "Fernando Maia": {
            "descrição": "Doutor em Saúde Coletiva. Pós-Doutorando em Epidemiologia do Câncer na FSP-USP, atuando no projeto ConeCta-SP.",
            "foto": "midia/fernando.jpg",
            "orcid": "https://orcid.org/0000-0001-7227-9774",
            "lattes": "http://lattes.cnpq.br/4778500596109672",
            "linkedin": "https://www.linkedin.com/in/fernando-maia-/",
        },

        "Simone Aldrey Angelo": {
            "descrição": "Doutora em Engenharia. Pesquisadora do projeto ConeCta-SP na área de Ciência de Dados e Inteligência Artificial aplicada à saúde, atuando no projeto ConeCta-SP.",
            "foto": "midia/simone.jpg",
            "orcid": "https://orcid.org/0000-0001-9700-7986",
            "lattes": "http://lattes.cnpq.br/4284294704799065",
            "linkedin": "https://www.linkedin.com/in/simoneangelo/",
        },

    },

    "fosp": {

        "Adeylson Guimarães Ribeiro": {
            "descrição": "Doutor em Saúde Pública. Diretor Adjunto de Informação e Epidemiologia na FOSP.",
            "foto": "midia/adeylson.jpg",
            "orcid": "https://orcid.org/0000-0001-8447-8463",
            "lattes": "http://lattes.cnpq.br/4139571558376095",
            "linkedin": "https://www.linkedin.com/in/adeylson-ribeiro-phd-13169514/",
        },

    },

    "ac": {

        "Maria Paula Curado": {
            "descrição": "Doutora em Oncologia. Chefe do Grupo de Epidemiologia e Estatística em Câncer (GEECAN).",
            "foto": "midia/maria_paula.jpg",
            "orcid": "https://orcid.org/0000-0001-8172-2483",
            "lattes": "http://lattes.cnpq.br/3397823736381748",
            "linkedin": "https://www.linkedin.com/in/maria-curado-54ba60105/",
        },

        "Gisele Aparecida Fernandes": {
            "descrição": "Doutora em Saúde Pública. Pesquisadora Científica no grupo de Epidemiologia e Estatística em Câncer do A.C. Camargo Cancer Center.",
            "foto": "midia/gisele.jpg",
            "orcid": "https://orcid.org/0000-0002-5978-3279",
            "lattes": "http://lattes.cnpq.br/0243509188105307",
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

# ---------- instituições ----------

instituicoes = { "imt":"Núcleo de Sistemas Eletrônicos Embarcados do Instituto Mauá de Tecnologia (NSEE-IMT)", "fsp":"Faculdade de Saúde Pública da Universidade de São Paulo (FSP-USP)", "fosp":"Fundação Oncocentro de São Paulo (FOSP)", "ac":"A.C. Camargo Cancer Center (AC)"}

for chave, valor in instituicoes.items():

    st.subheader(valor)

    for c in integrantes[chave].keys():

        lattes_link = f"[Lattes]({integrantes[chave][c]['lattes']}) | " if integrantes[chave][c]["lattes"] else ""
        orcid_link = f"[ORCID]({integrantes[chave][c]['orcid']}) | " if integrantes[chave][c]["orcid"] else ""
        linkedin_link = f"[LinkedIn]({integrantes[chave][c]['linkedin']})" if integrantes[chave][c]["linkedin"] else ""

        with st.popover(c, type="tertiary"):
            a, b = st.columns([1, 4])
            with a:
                st.image(integrantes[chave][c]["foto"], width=150)
            with b:
                st.write(integrantes[chave][c]["descrição"])
                st.write(f"{lattes_link}{orcid_link}{linkedin_link}")
