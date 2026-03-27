import streamlit as st
import pandas as pd

def dicionario_dados(legenda):
    dic_nomes = [

        'INSTITU', 'ESCOLARI',  'IBGE', 'TOPO', 'MORFO',
        'ANODIAG', 'FAIXAETAR', 'DRS', 'IBGEATEN', 'DRS_INST',
        'DISTANCIA_CARRO', 'TEMPO_CARRO', 'ivs_infraestrutura_urbana', 'ivs_capital_humano', 'ivs_renda_e_trabalho'
    
    ]

    dic_tipo = [
        'int64', 'int64', 'int64', 'string', 'int64',
        'int64', 'string', 'int64', 'int64', 'int64',
        'float64', 'int64', 'float64', 'float64', 'float64'
    ]
    
    dic_desc = [

                'Código da Instituição. Código de seis dígitos no formato 999999.',
                'Código para a escolaridade do paciente. Domínio: 1 - Analfabeto, 2 - Ens. Fundamental Incompleto, 3 - Ens. Fundamental Completo, 4 - Ens. Médio, 5 - Ens. Superior, 9 - Ignorado.', 
                'Código do município de residência do paciente, conforme tabela do IBGE. Código de sete dígitos no formato 9999999.',
                'Código da topografia do tumor, conforme CID-O-3, no formato C99',
                'Código da morfologia do tumor, conforme CID-O-3, no formato 99999.',
                'Ano de diagnóstico do câncer, no formato 9999.',
                'Faixa etária do paciente no momento do diagnóstico, no formato. Domínio: \'20-29\', \'30-39\', \'40-49\', \'50-59\', \'60-69\', \'70+\'',
                'Código do Departamento Regional de Saúde (DRS) do paciente.',
                'Código do município de atendimento do paciente, conforme tabela do IBGE. Código de sete dígitos no formato 9999999.',
                'Código do Departamento Regional de Saúde (DRS) da Instituição.',
                'Distância entre o município de residência e o município de atendimento, em quilômetros.',
                'Tempo necessário para deslocamento entre o município de residência e o município de atendimento, em minutos.',
                'Dimensão de Infraestrutua Urbana do Índice de Vulnerabilidade Social (IVS). Formato decimal.',
                'Dimensão de Capital Humano do Índice de Vulnerabilidade Social (IVS). Formato decimal.',
                'Dimensão de Renda e Trabalho do Índice de Vulnerabilidade Social (IVS). Formato decimal.',

    ]

    dicionario = st.expander(legenda)
    dicionario.table(pd.DataFrame({
            'Nome da Coluna': dic_nomes,
            'Tipo de Dado': dic_tipo,
            'Descrição': dic_desc
        }).set_index('Nome da Coluna'))
    
    return dicionario