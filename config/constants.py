# ---------- informações usadas para filtro ----------

TIPOS_GRAFICO = {
    'Número de Consultas': 'DTCONSULT',
    'Inícios de Tratamento':'DTTRAT',
    'Últimas informações':'DTULTINFO',
}

CARACTERISTICAS = {
    'Derivada': 'deriv_sbv',
    'Integral': 'int_sbv',
}


PERIODOS_TEMPO = {
    'Semanas': 'W',
    'Meses': 'ME',
}

TOPOGRAFIAS = {
    'Colorretal': ['C18', 'C19', 'C20'],
    'Pulmão': ['C34'],
    'Mama': ['C50'],
    'Colo do Útero': ['C53'],
    'Próstata': ['C61']
    }

COD_TOPOGRAFIAS = {
    'Colorretal': ['C18', 'C180', 'C181', 'C182', 'C183', 'C184', 'C185', 'C186', 'C187','C188','C189', 'C19', 'C199', 'C20','C209'],
    'Pulmão': ['C34', 'C340', 'C341', 'C342', 'C343', 'C348', 'C349'],
    'Mama': ['C50', 'C500', 'C501', 'C502', 'C503', 'C504', 'C505', 'C506', 'C508', 'C509'],
    'Colo do Útero': ['C53', 'C530', 'C531', 'C538', 'C539'],
    'Próstata': ['C61', 'C619']
    }

ESTADIAMENTO_CLINICO = {
    'I': ['I'],
    'II':['II'],
    'III':['III'],
    'IV':['IV']
}

TIPO_DRS = {
    'DRS de Residência': 'DRS',
    'DRS de Hospital': 'DRS_INST',
}

DRS_DICT = {
    "Capital": 1,
    "Interior": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
    "DRS 1 - Grande São Paulo": 1,
    "DRS 2 - Araçatuba": 2,
    "DRS 3 - Araraquara": 3,
    "DRS 4 - Baixada Santista": 4,
    "DRS 5 - Barretos": 5,
    "DRS 6 - Bauru": 6,
    "DRS 7 - Campinas": 7,
    "DRS 8 - Franca": 8,
    "DRS 9 - Marília": 9,
    "DRS 10 - Piracicaba": 10,
    "DRS 11 - Presidente Prudente": 11,
    "DRS 12 - Registro": 12,
    "DRS 13 - Ribeirão Preto": 13,
    "DRS 14 - São João da Boa Vista": 14,
    "DRS 15 - São José do Rio Preto": 15,
    "DRS 16 - Sorocaba": 16,
    "DRS 17 - Taubaté": 17
}

ESCOLARIDADE = {'Analfabeto': 1,
                'Ensino Fundamental Incompleto': 2,
                'Ensino Fundamental Completo': 3,
                'Ensino Médio': 4,
                'Ensino Superior': 5,
                'Ignorado': 9}

FAIXA_ETARIA = ['20-29', '30-39', '40-49', '50-59', '60-69', '70+']

CATEATEND = {
    'Convênio': 1,
    'SUS': 2,
    'Particular': 3,
    'Sem Informação': 9
}

HABILIT_HOSP = {
    'UNACON sem radioterapia': 1,
    'CACON': 2,
    'UNACON com radioterapia': 3,
}

FEATURES = {
    'Colorretal': ['INSTITU', 'ESCOLARI', 'SEXO', 'IBGE', 'CATEATEND',
               'DIAGPREV', 'TOPO', 'MORFO', 'ECGRUP', 'ANODIAG',
               'FAIXAETAR', 'DRS', 'IBGEATEN',
               'DRS_INST', 'HABILIT_HOSP', 'DISTANCIA_CARRO', 'TEMPO_CARRO'
               'TRATCONS_CAT', 'DIAGTRAT_CAT', 'ivs_infraestrutura_urbana',
               'ivs_capital_humano', 'ivs_renda_e_trabalho'
            ],
    'Pulmão': ['INSTITU', 'ESCOLARI', 'SEXO', 'IBGE', 'CATEATEND', 'DIAGPREV', 'TOPO',
            'MORFO', 'ECGRUP', 'ANODIAG', 'FAIXAETAR', 'DRS', 'IBGEATEN',
            'DRS_INST', 'HABILIT_HOSP', 'DISTANCIA_CARRO', 'TEMPO_CARRO',
            'TRATCONS_CAT', 'DIAGTRAT_CAT', 'ivs_infraestrutura_urbana',
            'ivs_capital_humano', 'ivs_renda_e_trabalho'
            ] ,
    'Mama': ['INSTITU', 'ESCOLARI', 'IBGE', 'CATEATEND', 'DIAGPREV', 'TOPO', 'MORFO',
            'ECGRUP', 'ANODIAG', 'FAIXAETAR', 'DRS', 'IBGEATEN', 'DRS_INST',
            'HABILIT_HOSP', 'DISTANCIA_CARRO', 'TEMPO_CARRO', 'TRATCONS_CAT',
            'DIAGTRAT_CAT', 'ivs_infraestrutura_urbana', 'ivs_capital_humano',
            'ivs_renda_e_trabalho'
            ],
    'Colo do Útero': ['INSTITU', 'ESCOLARI', 'IBGE', 'CATEATEND', 'DIAGPREV', 'TOPO', 'MORFO',
            'ECGRUP', 'ANODIAG', 'FAIXAETAR', 'DRS', 'IBGEATEN', 'DRS_INST',
            'HABILIT_HOSP', 'DISTANCIA_CARRO', 'TEMPO_CARRO', 'TRATCONS_CAT',
            'DIAGTRAT_CAT', 'ivs_infraestrutura_urbana', 'ivs_capital_humano',
            'ivs_renda_e_trabalho'
            ],
    'Próstata': ['INSTITU', 'ESCOLARI', 'IBGE', 'CATEATEND', 'DIAGPREV', 'TOPO', 'MORFO',
            'ECGRUP', 'ANODIAG', 'FAIXAETAR', 'DRS', 'IBGEATEN', 'DRS_INST',
            'HABILIT_HOSP', 'DISTANCIA_CARRO', 'TEMPO_CARRO', 'TRATCONS_CAT',
            'DIAGTRAT_CAT', 'ivs_infraestrutura_urbana', 'ivs_capital_humano',
            'ivs_renda_e_trabalho'
            ]
}