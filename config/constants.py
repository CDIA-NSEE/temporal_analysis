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
    'Próstata': ['C18', 'C19', 'C20'],
    'Pulmão': ['C34'],
    'Mama': ['C50'],
    'Colo do Útero': ['C53'],
    'Colorretal': ['C61']
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