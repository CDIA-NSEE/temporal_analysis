import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

def tratamento_por_drs(df):

    # Total de pacientes por DRS de residência
    total_por_drs = df.groupby('DRS').size().rename('total_pacientes')

    # Cálculo de estatísticas de distância/tempo por DRS (média e mediana)
    dist_media = df.groupby('DRS')['DISTANCIA_CARRO'].mean().round(2).rename('dist_carro_media')
    dist_mediana = df.groupby('DRS')['DISTANCIA_CARRO'].median().round(2).rename('dist_carro_mediana')
    tempo_medio = df.groupby('DRS')['TEMPO_CARRO'].mean().round(2).rename('tempo_carro_media')
    tempo_mediano = df.groupby('DRS')['TEMPO_CARRO'].median().round(2).rename('tempo_carro_mediana')

    # Junta em uma tabela as estatísticas calculadas por DRS
    stats = pd.concat([total_por_drs, dist_media, dist_mediana, tempo_medio,
                       tempo_mediano], axis=1)

    # Exibe a tabela de estatísticas por DRS
    display(stats)

    print("\n\n\n")

    # Recalcula total de pacientes por DRS (repetido para a lógica a seguir)
    total_por_drs = df.groupby('DRS').size().rename('total_pacientes')

    # --- Identifica a DRS externa mais popular para cada DRS de residência ---
    # Considera apenas os registros em que houve saída para outra DRS (DRS != DRS_INST)
    externa_popular = (
        df[df['DRS'] != df['DRS_INST']]
        .groupby(['DRS', 'DRS_INST'])
        .size()
        .rename('qtd')
        .reset_index()
    )

    # Para cada DRS de residência, seleciona a DRS_INST (externa) com maior número de pacientes
    externa_top = (
        externa_popular
        .sort_values(['DRS', 'qtd'], ascending=[True, False])
        .groupby('DRS')
        .first()
        .rename(columns={'DRS_INST': 'top_DRS_ext', 'qtd': 'qtd_princ_DRS_ext'})
    )

    # Conta quantos pacientes foram tratados na mesma DRS de residência (sem saída)
    mesma_drs = df[df['DRS'] == df['DRS_INST']].groupby('DRS').size().rename('mesma_DRS')

    # Junta os totais e as contagens de permanência; preenche NaN com 0 quando não houver ocorrência
    stats = pd.concat([total_por_drs, mesma_drs], axis=1).fillna(0)
    stats['mesma_DRS'] = stats['mesma_DRS'].astype(int)  # garante tipo inteiro

    # Calcula percentuais de permanência na mesma DRS
    stats['pct_mesma_DRS'] = (stats['mesma_DRS'] / stats['total_pacientes']) * 100
    stats['pct_mesma_DRS'] = stats['pct_mesma_DRS'].round(2)  # arredonda para 2 casas decimais
    # stats['pct_outra_DRS'] = 100 - stats['pct_mesma_DRS']      # complemento para 100% (comentado)

    # Junta as estatísticas de permanência com a informação da principal DRS externa
    resultado = stats.join(externa_top[['top_DRS_ext', 'qtd_princ_DRS_ext']])

    # Seleciona apenas registros em que houve saída para outra DRS (usado posteriormente)
    df_grandes_evasoes = df[(df['DRS'] != df['DRS_INST'])]

    # Inicializa estrutura com a DRS externa principal e sua quantidade (a partir do 'resultado')
    df_final_grandes_evasoes = resultado[['top_DRS_ext', 'qtd_princ_DRS_ext']]

    # Calcula médias (mean) e medianas (median) de distância e tempo para cada par (DRS, DRS_INST)
    medias = (
                df.groupby(['DRS', 'DRS_INST'])[['DISTANCIA_CARRO', 'TEMPO_CARRO']]
                .agg(['mean', 'median'])
                .round(2)
            )

    # Traz as médias de distância da DRS externa principal para o resultado, fazendo merge por (DRS, top_DRS_ext)
    aux = df_final_grandes_evasoes.merge(
                medias['DISTANCIA_CARRO'],
                left_on = ['DRS', 'top_DRS_ext'],
                right_on = ['DRS', 'DRS_INST'],
                how = 'left'
            )

    # Adiciona ao 'resultado' as médias e medianas de distância na DRS externa principal
    resultado['dist_media_DRS_ext'] = aux['mean']
    resultado['dist_mediana_DRS_ext'] = aux['median']

    # Faz merge para trazer as médias de tempo da DRS externa principal
    df_final_grandes_evasoes = df_final_grandes_evasoes.merge(
                medias['TEMPO_CARRO'],
                left_on = ['DRS', 'top_DRS_ext'],
                right_on = ['DRS', 'DRS_INST'],
                how = 'left'
            )

    # Adiciona ao 'resultado' as médias e medianas de tempo na DRS externa principal
    resultado['tempo_medio_DRS_ext'] = df_final_grandes_evasoes['mean']
    resultado['tempo_mediano_DRS_ext'] = df_final_grandes_evasoes['median']

    # Ordena o resultado por DRS (ordem crescente) para apresentação
    resultado = resultado.sort_values('DRS', ascending=True)

    # Exibe o DataFrame resumo final com informação de permanência e médias externas
    display(resultado)

def describe_por_drs(df):

    # Lista de colunas de distância/tempo a serem analisadas
    cols_d_t = ['DISTANCIA_CARRO', 'TEMPO_CARRO', 'DISTANCIA_TRANSP', 'TEMPO_TRANSP']

    # Para cada coluna dessa lista, calcula e mostra as estatísticas descritivas por DRS
    for col in cols_d_t:
        print(col)  # Imprime o nome da coluna que está sendo processada
        # Agrupa por 'DRS' e aplica describe() na coluna atual, arredondando para 2 casas decimais,
        # em seguida exibe o resultado (display é útil em notebooks para formatação)
        display(df.groupby('DRS')[col].describe().round(2))
        print('\n\n')  # Quebra de linhas para separar visualmente os blocos de saída

def top_distancias_por_drs(df):#, n_pacientes=10):

    # Agrupa os registros por DRS e instituição (DSCINST) e calcula a média das colunas de distância/tempo
    # Em seguida, arredonda os valores para 2 casas decimais e ordena pelo DRS (crescente) e pela DISTANCIA_CARRO (decrescente)
    df_drs = df.groupby(['DRS', 'DSCINST'])[
        ['DISTANCIA_CARRO', 'TEMPO_CARRO', 'DISTANCIA_TRANSP', 'TEMPO_TRANSP', 'DRS_INST']
        ].mean().round(2).sort_values(['DRS', 'DISTANCIA_CARRO'], ascending=[True, False])

    df_drs = df_drs.reset_index()  # Reinicia o índice para transformar DRS e DSCINST em colunas regulares

    # Conta o número de pacientes por combinação (DRS, DSCINST) e renomeia a série resultante para 'Pacientes'
    df_pacientes = df.groupby(['DRS', 'DSCINST']).size().rename('Pacientes')

    # Faz o merge da tabela de médias com a contagem de pacientes, juntando pelas colunas DRS e DSCINST
    df_drs = df_drs.merge(df_pacientes, on=['DRS', 'DSCINST'])

    # Seleção de um número mínimo de pacientes
    # df_drs = df_drs[df_drs['Pacientes'] >= n_pacientes]
    print(df_drs.shape)
    print()

    # Itera por cada DRS único na tabela df_drs e mostra uma visão superior e inferior de cada grupo
    for drs in df_drs.DRS.unique():
        print(f'DRS {drs}')                           # Imprime o identificador do DRS atual como cabeçalho
        display(df_drs[df_drs.DRS == drs])            # Mostra o subconjunto inteiro
        print()                                       # Linha em branco para separar visualmente os blocos de saída

@st.cache_data(show_spinner="Calculando estatísticas...")
def estatisticas_ec(df, topo, drs, col):

    df = df.copy()

    #seleção das topografias escolhidas
    df = df[df['TOPOGRUP'].isin(topo)]

    # #seleção das DRS escolhidas
    if drs is not None:
        df = df[df['DRS'] == drs]

    # Estatísticas descritivas gerais para toda a coluna (média, mediana, std, min, max, etc.)
    # Arredonda os valores para 2 casas decimais e renomeia a série para 'Geral'
    geral = df[col].describe().round(2).rename('Geral')

    # Estatísticas descritivas agrupadas por estágio clínico (ECGRUP)
    # Aplica describe() por grupo, arredonda para 2 casas e transpõe para facilitar a concatenação
    ec = df.groupby('ECGRUP')[col].describe().round(2).T
    # Concatena as estatísticas gerais e as estatísticas por ECGRUP lado a lado (por colunas)
    tudo_junto = pd.concat([geral, ec], axis=1)

    # Exibe o DataFrame resultante com as estatísticas compiladas
    return tudo_junto

@st.cache_data(show_spinner="Gerando gráficos...")
def boxplots_ec(df, topo, drs, col, x_title):

    df = df.copy()

    #seleção das topografias escolhidas
    df = df[df['TOPOGRUP'].isin(topo)]

    # #seleção das DRS escolhidas
    if drs is not None:
        df = df[df['DRS'] == drs]

    fig = go.Figure()

    # Caixa geral (toda a amostra) representada como a categoria "Geral" no eixo y — orientada horizontalmente
    fig.add_trace(go.Box(
        x=df[col],  # valores da variável selecionada
        y=['Geral'] * len(df),  # repete a etiqueta "Geral" para cada ponto, para posicionar a caixa no eixo y
        name='Geral',
        orientation='h',  # orientação horizontal
    ))

    # Caixas por estágio clínico (ECGRUP) — cada uma como uma linha horizontal separada
    for g in ['I', 'II', 'III', 'IV']:
        vals = df.loc[df['ECGRUP'] == g, col]  # seleciona os valores da coluna para o grupo ECGRUP = g
        fig.add_trace(go.Box(
            x=vals,  # valores do grupo
            y=[g] * len(vals),  # etiqueta do grupo repetida para posicionamento no eixo y
            name=f'ECGRUP {g}',
            orientation='h',  # orientação horizontal
        ))

    # Ajustes de layout: título do eixo x, inverter a ordem das categorias no eixo y (Geral no topo)
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(autorange='reversed')

    # Remove legenda (opcional, para deixar o gráfico mais limpo)
    fig.update_layout(showlegend=False)

    return fig

@st.cache_data(show_spinner="Calculando métricas...")
def características_drs(df, topo, ec, drs, col):

    df = df.copy()

    #seleção das topografias escolhidas
    df = df[df['TOPOGRUP'].isin(topo)]

    #seleciona o estadiamento clínico especificado
    df = df[df['ECGRUP'].isin(ec)]

    # #seleção das DRS escolhidas
    if drs is not None:
        df = df[df['DRS'] == drs]
    
    total_pacientes = df.shape[0]
    dist_media = round(df[f'DISTANCIA_{col}'].mean(), 2)
    dist_mediana = round(df[f'DISTANCIA_{col}'].median(), 2)
    tempo_medio = round(df[f'TEMPO_{col}'].mean())
    tempo_mediano = round(df[f'TEMPO_{col}'].median())
    mesma_drs = df[df['DRS'] == df['DRS_INST']].shape[0]

    externa_popular = (
        df[df['DRS'] != df['DRS_INST']]
        .groupby(['DRS','DRS_INST'])
        .size()
        .rename('qtd')
        .reset_index()
    )

    externa_top = (
        externa_popular
        .sort_values(['DRS','qtd'], ascending=[True, False])
        .groupby("DRS")
        .first()
        .rename(columns={'DRS_INST': 'top_DRS_ext', 'qtd': 'qtd_princ_DRS_ext'})
    )

    drs_ext_princ = externa_top['top_DRS_ext'].values[0]
    df_princ_ext = df[(df['DRS'] != df['DRS_INST']) & (df['DRS_INST'] == drs_ext_princ)]
    media_dist_principal = round(df_princ_ext[f'DISTANCIA_{col}'].mean(), 2)

    resultados = {
        'Total de Pacientes': total_pacientes,
        'Distância Média (km)': dist_media,
        'Distância Mediana (km)': dist_mediana,
        'Tempo Médio (min)': tempo_medio,
        'Tempo Mediano (min)': tempo_mediano,
        'Pacientes na Mesma DRS': mesma_drs,
        'Principal DRS de Saida': externa_top['top_DRS_ext'].values[0],
        'Qtd. na Principal DRS de Saída': externa_top['qtd_princ_DRS_ext'].values[0],
        'Distância Média de Saída (km)': media_dist_principal
    }

    return resultados





