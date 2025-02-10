import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import subprocess
from itertools import combinations
import seaborn as sns
from datetime import datetime, time
from PIL import Image
import os

# URL fixa do arquivo Google Sheets
# google_sheets_url = "https://docs.google.com/spreadsheets/d/14QwHMEPjJa1oyMwA95IvkczRaEVPASt7ym-SO0W0-lQ/export?format=csv&gid=879940212"

def carregar_dados(google_sheets_url):
    nomes_colunas = ['DataHora', 'Temperatura', 'Umidade', 'MQ-3', 'MQ-4', 'MQ-7', 'MQ-8', 'MQ-135']
    dados_experimento = pd.read_csv(google_sheets_url, header=None, names=nomes_colunas, delimiter=',')

    # Converter DataHora para datetime com o formato correto
    dados_experimento['DataHora'] = pd.to_datetime(dados_experimento['DataHora'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    
    if google_sheets_url == "data/EXPERIMENTO_1_FISICA_Dados.csv":
        # Definir o dia 11 de janeiro como "hora zero"
        inicio_experimento = pd.Timestamp("2025-01-11 00:00:00")
    elif google_sheets_url == "data/EXPERIMENTO_2_FISICA_Dados.csv":
        # Definir o dia 24 de janeiro como "hora zero"
        inicio_experimento = pd.Timestamp("2025-01-24 21:00:00")

    dados_experimento['HorasDecorridas'] = (dados_experimento['DataHora'] - inicio_experimento).dt.total_seconds() / 3600
    
    # Definir o intervalo a ser removido
    inicio_remocao = pd.Timestamp("2025-01-09 00:00:00")
    fim_remocao = pd.Timestamp("2025-01-10 23:59:59")

    # Filtrar os dados do período a ser removido
    dados_removidos = dados_experimento[(dados_experimento['DataHora'] >= inicio_remocao) & (dados_experimento['DataHora'] <= fim_remocao)]
    dados_experimento = dados_experimento[~((dados_experimento['DataHora'] >= inicio_remocao) & (dados_experimento['DataHora'] <= fim_remocao))]
    
    return dados_experimento, dados_removidos


def carregar_dados_inmet():
    # Lê os dados do INMET
    nomes_colunas = ['Data', 'Hora (UTC)', 'Temp. Ins. (C)']
    dados_inmet = pd.read_csv("data/inmet_dados.csv", delimiter=';', usecols=nomes_colunas)

    # Garantir que Hora (UTC) seja uma string e tenha 4 dígitos (HHMM)
    dados_inmet['Hora (UTC)'] = dados_inmet['Hora (UTC)'].astype(str).str.zfill(4)  # Garantir que hora tenha 4 dígitos (ex: 100 -> 0100)

    # Transformar a hora no formato HH:MM
    dados_inmet['Hora (UTC)'] = dados_inmet['Hora (UTC)'].apply(lambda x: x[:2] + ':' + x[2:])  # Ex: "0100" -> "01:00"

    # Garantir que a Data também seja uma string
    dados_inmet['Data'] = dados_inmet['Data'].astype(str)

    # Combina Data e Hora (UTC) para formar DataHora
    try:
        dados_inmet['DataHora'] = pd.to_datetime(dados_inmet['Data'] + ' ' + dados_inmet['Hora (UTC)'], format="%d/%m/%Y %H:%M", errors='raise')
    except Exception as e:
        print(f"Erro ao combinar Data e Hora: {e}")
        print(dados_inmet[['Data', 'Hora (UTC)']].head())

    # Verificar se a coluna DataHora foi criada corretamente
    if 'DataHora' not in dados_inmet.columns:
        print("Erro: A coluna 'DataHora' não foi criada corretamente.")
        return None

    # Selecionar apenas a coluna de interesse e a DataHora
    dados_inmet = dados_inmet[['DataHora', 'Temp. Ins. (C)']]
    
    return dados_inmet


def mesclar_temperatura(dados_experimento, dados_inmet):
    # Garantir que a coluna 'DataHora' em 'dados' seja somente data e hora (sem minutos e segundos)
    dados_experimento['DataHora'] = dados_experimento['DataHora'].dt.floor('H')  # Arredonda para a hora mais próxima (desconsidera minutos e segundos)
    
    # Garantir que a coluna 'DataHora' em 'dados_inmet' também tenha apenas data e hora (sem minutos e segundos)
    dados_inmet['DataHora'] = dados_inmet['DataHora'].dt.floor('H')  # Arredonda para a hora mais próxima (desconsidera minutos e segundos)
    
    # Faz a junção dos DataFrames com base na DataHora
    dados_experimento = pd.merge(dados_experimento, dados_inmet[['DataHora', 'Temp. Ins. (C)']], on="DataHora", how="left")

    # Renomeia a temperatura do INMET para evitar confusão
    dados_experimento.rename(columns={'Temp. Ins. (C)': 'Temperatura_Externa'}, inplace=True)

    dados_experimento['Temperatura_Externa'] = dados_experimento['Temperatura_Externa'].str.replace(',', '.').astype(float)
    

    return dados_experimento


def calcular_variacoes_diarias(dados, colunas_selecionadas):
    try:
        dados['Dia'] = dados['DataHora'].dt.date
        dados[colunas_selecionadas] = dados[colunas_selecionadas].apply(pd.to_numeric, errors='coerce')

        estatisticas_diarias = (
            dados.groupby('Dia')[colunas_selecionadas]
            .agg(['min', 'max', 'mean', 'std'])
        )
        return estatisticas_diarias
    except Exception as e:
        st.error(f"Erro ao calcular variações diárias: {e}")
        return None

def exibir_tabela_variacao_diaria(estatisticas_diarias):
    try:
        if estatisticas_diarias is not None:
            estatisticas_transpostas = estatisticas_diarias.stack().transpose()
            estatisticas_transpostas.index.names = ['Estatística']
            estatisticas_transpostas.columns = pd.MultiIndex.from_tuples(
                [(col[0], col[1]) for col in estatisticas_transpostas.columns],
                names=['Dia', 'Métrica']
            )
            st.dataframe(estatisticas_transpostas)

            st.write("### Dias com Maior Desvio Padrão para Cada Sensor")
            
            # Identificar o dia com maior desvio padrão para cada sensor
            dias_maior_std = estatisticas_diarias.xs('std', level=1, axis=1).idxmax()

            # Obter os valores do maior desvio padrão correspondente
            valores_maior_std = estatisticas_diarias.xs('std', level=1, axis=1).max()

            # Criar uma tabela com ambos os valores
            dias_maior_std_tabela = pd.DataFrame({
                'Dia': dias_maior_std,
                'Valor': valores_maior_std
            })
            dias_maior_std_tabela.index.name = "Sensor"
            
            st.table(dias_maior_std_tabela)
        else:
            st.warning("Nenhuma variação diária foi calculada.")
    except Exception as e:
        st.error(f"Erro ao exibir tabela de variação diária: {e}")


def exibir_graficos_interativos(dados_filtrados, colunas_selecionadas, medias_removidos):
    st.write("### Gráficos Interativos Relativos ao Tempo")

    cores_colunas = px.colors.qualitative.Set1
    cor_mapeamento = {coluna: cores_colunas[i % len(cores_colunas)] for i, coluna in enumerate(colunas_selecionadas)}

    fig = go.Figure()
    for coluna in colunas_selecionadas:
        fig.add_trace(
            go.Scatter(
                x=dados_filtrados['HorasDecorridas'],
                y=dados_filtrados[coluna].astype(float),
                mode='lines+markers',
                name=coluna,
                line=dict(color=cor_mapeamento[coluna]),
                hovertemplate='%{x:.2f} horas desde o início<br>Data e Hora: %{customdata}<br>Valor: %{y}<extra></extra>',
                customdata=dados_filtrados['DataHora'].dt.strftime('%Y-%m-%d %H:%M:%S')
            )
        )
        # Adicionar linha média dos dados removidos
        if coluna in medias_removidos:
            fig.add_trace(
                go.Scatter(
                    x=dados_filtrados['HorasDecorridas'],
                    y=[medias_removidos[coluna]] * len(dados_filtrados),
                    mode='lines',
                    line=dict(dash='dash', color=cor_mapeamento[coluna]),
                    showlegend=False
                )
            )

    # Adicionar um único trace para "Zero de cada sensor" na legenda
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(dash='dash', color='gray'),
            name="Zero de cada sensor"
        )
    )

    fig.update_layout(
        title="Gráficos Interativos Relativos ao Tempo",
        xaxis_title="Horas Decorridas",
        yaxis_title="Valor",
        legend_title="Sensores",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

def exibir_grafico_nao_interativo_linhas(dados, colunas_selecionadas):
    st.write("### Gráficos Não Interativos")
    try:
        # Criação do gráfico usando plotly.graph_objects
        fig = go.Figure()
        for coluna in colunas_selecionadas:
            fig.add_trace(
                go.Scatter(
                    x=dados['HorasDecorridas'],
                    y=dados[coluna].astype(float),
                    mode='lines',
                    name=coluna
                )
            )

        # Configuração do layout do gráfico
        fig.update_layout(
            title="Gráfico Não Interativo (Linhas)",
            xaxis_title="Horas Decorridas",
            yaxis_title="Valores",
            legend_title="Sensores",
            hovermode="x unified",  # Exibir informações detalhadas no hover
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao criar o gráfico de linhas: {e}")

def exibir_mapa_calor(dados_filtrados, colunas_selecionadas):
    if colunas_selecionadas:
        st.write("### Mapa de Calor da Correlação")
        try:
            dados_corr = dados_filtrados[colunas_selecionadas].apply(pd.to_numeric, errors='coerce').corr()

            fig = px.imshow(dados_corr, text_auto=True, color_continuous_scale='Reds')
            fig.update_layout(title="Correlação Entre os Sensores")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar o mapa de calor: {e}")

def verificar_video(input_video, output_video):
    if not os.path.exists(output_video):
        conversion_command = f"ffmpeg -i {input_video} -vcodec libx264 -crf 28 {output_video}"
        subprocess.run(conversion_command, shell=True, check=True)
    video_file = open(output_video, "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)

def exibir_pagina_inicial(dados, estatisticas_diarias, colunas_selecionadas, dados_filtrados, medias_removidos):
    st.title("Página Inicial")
    st.write("### Tabela de Variação Diária")
    exibir_tabela_variacao_diaria(estatisticas_diarias)
    

    exibir_grafico_nao_interativo_linhas(dados_filtrados, colunas_selecionadas)

    exibir_mapa_calor(dados_filtrados, colunas_selecionadas)

def informacoes():
    st.write('# Informações relevantes')

    st.write('Inicio do experiento dia 11/01 às 11:26.')
    st.write('Fim do experimento dia 19/01 às 16:55.')

    st.write('77 dias desde o início do projeto (08/11/2024 - 24/01/2025).')

    st.write('Altura dos sensores em relação as bananas: 20 cm')
    st.write('Dia 15/01 às 13h: Adicionamos uma barreira para tentar evitar a dispersão dos gases.')

    st.write('## Definições: ')
    st.write('### DHT-11: ')
    st.write('Temperatura e umidade;')
    st.write('### MQ-3: ')
    st.write('Módulo capaz de detectar vapores de álcool e etanol;')
    st.write('### MQ-4: ')
    st.write('Módulo capaz de detectar gases inflamáveis como Metano, Propano e Butano;')
    st.write('### MQ-7: ')
    st.write('Módulo capaz de detectar o gás Monóxido de Carbono CO;')
    st.write('### MQ-8: ')
    st.write('Módulo capaz de detectar concentrações de gás hidroênio no ar;')
    st.write('### MQ-135: ')
    st.write('Capaz de detectar amônia, dióxido de carbono, benzeno, óxido nítrico e também fumaça e álcool.')

    st.write('## Visualizar antes e depois: ')
    st.write('Visualizar a banana antes do início do experiemnto: VISUALIZAR FOTOS --> DATA: 2025/01/11 HORA: 11:20')
    st.write('Visualizar a banana após o fim do experiemnto: VISUALIZAR FOTOS --> DATA: 2025/01/19 HORA: 17:00')

def exibir_medias_diarias(dados_filtrados, colunas_selecionadas):
    st.write("### Médias Diárias para os Dados Selecionados")

    # Dicionário explicativo dos sensores
    descricao_sensores = {
        "MQ-3": "Módulo capaz de detectar vapores de álcool e etanol.",
        "MQ-4": "Módulo capaz de detectar gases inflamáveis como Metano, Propano e Butano.",
        "MQ-7": "Módulo capaz de detectar o gás Monóxido de Carbono (CO).",
        "MQ-8": "Módulo capaz de detectar concentrações de gás hidrogênio no ar.",
        "MQ-135": "Capaz de detectar amônia, dióxido de carbono, benzeno, óxido nítrico e também fumaça e álcool."
    }


    try:
        # Garantir que as colunas são numéricas
        for coluna in colunas_selecionadas:
            dados_filtrados[coluna] = pd.to_numeric(dados_filtrados[coluna], errors='coerce')
        
        dados_filtrados['Dia'] = dados_filtrados['DataHora'].dt.date
        medias_diarias = dados_filtrados.groupby('Dia')[colunas_selecionadas].mean()

        if medias_diarias.empty:
            st.warning("Nenhuma média diária foi calculada. Verifique os dados selecionados.")
            return
        
        st.dataframe(medias_diarias)

        # Calculando a taxa de aumento
        taxas_aumento = medias_diarias.pct_change() * 100
        # Exibir DataFrame com taxas de aumento
        st.write("#### Taxas de Aumento (%)")
        st.dataframe(taxas_aumento)                

        # Criar um gráfico único com todas as médias diárias
        fig = px.line(
            medias_diarias,
            x=medias_diarias.index,
            y=colunas_selecionadas,
            title="Médias Diárias para os Dados Selecionados",
            labels={"x": "Dia", "value": "Média"},
        )

        # Adicionando pontos ao gráfico
        fig.update_traces(mode="lines+markers")
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráficos de linha para as médias diárias
        for coluna in colunas_selecionadas:
            st.write(f"**Médias diárias do sensor {coluna}:**")
            
            # Criar gráfico para o sensor atual
            fig = px.line(
                medias_diarias,
                x=medias_diarias.index,
                y=coluna,
                title=f"{coluna}",
                labels={"x": "Dia", coluna: "Média"},
            )
            fig.update_traces(mode="lines+markers")
            st.plotly_chart(fig, use_container_width=True)

            # Exibir a descrição do sensor abaixo do gráfico
            if coluna in descricao_sensores:
                st.markdown(f"📌 **Descrição do {coluna}:** {descricao_sensores[coluna]}")
            else:
                st.markdown(f"📌 **Descrição do {coluna}:** Informação não disponível.")


    except Exception as e:
        st.error(f"Erro ao calcular/exibir médias diárias: {e}")

def analisar_regressoes(dados_filtrados, colunas_selecionadas):
    """
    Realiza análises de regressão linear para todas as combinações possíveis
    de pares de colunas selecionadas e gera gráficos com as equações.

    Args:
        dados_filtrados (DataFrame): O DataFrame com os dados filtrados.
        colunas_selecionadas (list): Lista de colunas selecionadas para análise.
    """
    if len(colunas_selecionadas) < 2:
        st.error("Por favor, selecione pelo menos duas colunas para realizar a análise.")
        return
    
    # Gerar todas as combinações possíveis de pares de colunas
    combinacoes = list(combinations(colunas_selecionadas, 2))
    
    for sensor_1, sensor_2 in combinacoes:
        # Verificar se há valores faltantes (NaN) nos dados
        if dados_filtrados[[sensor_1, sensor_2]].isna().sum().sum() > 0:
            st.error(f"Os dados de {sensor_1} ou {sensor_2} contêm valores ausentes (NaN).")
            st.write(f"Linhas com NaN em {sensor_1}:")
            st.write(dados_filtrados[dados_filtrados[sensor_1].isna()])
            st.write(f"Linhas com NaN em {sensor_2}:")
            st.write(dados_filtrados[dados_filtrados[sensor_2].isna()])
            continue  # Pular para a próxima combinação se houver NaN
        
        try:
            # Inicializar o modelo de regressão linear
            regressor = LinearRegression()
            
            # Ajustar o modelo
            X = dados_filtrados[[sensor_1]]
            y = dados_filtrados[sensor_2]
            regressor.fit(X, y)
            
            # Obter o coeficiente e o intercepto
            coef = regressor.coef_[0]
            intercept = regressor.intercept_
            
            # Previsões
            y_pred = regressor.predict(X)
            
            # Mostrar a equação da regressão
            st.write(f"**Equação de regressão entre {sensor_1} e {sensor_2}:**")
            st.write(f"{sensor_2} = {coef:.4f} * {sensor_1} + {intercept:.4f}")
            
            # Plotar o gráfico de dispersão com a linha de regressão
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=sensor_1, y=sensor_2, data=dados_filtrados, color='blue', s=10)
            plt.plot(dados_filtrados[sensor_1], y_pred, color='red')  # Linha de regressão
            plt.title(f"Relação entre {sensor_1} e {sensor_2}")
            plt.xlabel(sensor_1)
            plt.ylabel(sensor_2)
            st.pyplot(plt)
        
        except Exception as e:
            # Caso ocorra algum erro durante o ajuste do modelo
            st.error(f"Erro ao ajustar o modelo de regressão entre {sensor_1} e {sensor_2}: {e}")
            st.write(f"Linhas de dados problemáticas (se houver) em {sensor_1} e {sensor_2}:")
            st.write(dados_filtrados[[sensor_1, sensor_2]].head())  # Mostra as primeiras linhas para diagnóstico


def exibir_imagens_experimento(diretorio_imagens,data_inicial,data_final,hora_inicial,hora_final):
    st.title("Visualização de Fotos do Experimento")

    # Seleção de data
    data_selecionada = st.date_input("Selecione a data:", min_value=data_inicial, max_value=data_final)

    # Seleção de hora
    hora_selecionada = st.time_input("Selecione a hora:", value=hora_inicial)

    # Formatar a data e hora para buscar os arquivos
    formato_busca = data_selecionada.strftime("%Y-%m-%d") + "_" + hora_selecionada.strftime("%H-%M")

    # Buscar arquivos correspondentes no diretório
    imagens_encontradas = [
        os.path.join(diretorio_imagens, arquivo)
        for arquivo in os.listdir(diretorio_imagens)
        if formato_busca in arquivo
    ]

    if imagens_encontradas:
        st.write(f"Imagens encontradas para {data_selecionada} às {hora_selecionada}:")
        for caminho_imagem in imagens_encontradas:
            imagem = Image.open(caminho_imagem)
            st.image(imagem, caption=os.path.basename(caminho_imagem), use_container_width=True)

    else:
        st.warning("Nenhuma imagem encontrada para a data e hora selecionadas.")

def detectar_picos_simultaneos(dados_filtrados, colunas_selecionadas):
    """
    Detecta picos simultâneos para todas as combinações de sensores e gera gráficos interativos com Plotly.

    Args:
        dados_filtrados (DataFrame): O DataFrame com os dados filtrados.
        colunas_selecionadas (list): Lista de colunas selecionadas para análise.
    """
    if len(colunas_selecionadas) < 2:
        st.error("Por favor, selecione pelo menos duas colunas para realizar a análise.")
        return

    # Gerar todas as combinações possíveis de pares de colunas
    combinacoes = list(combinations(colunas_selecionadas, 2))

    for sensor_1, sensor_2 in combinacoes:
        # Detectar picos em cada sensor
        peaks_sensor_1, _ = find_peaks(dados_filtrados[sensor_1])
        peaks_sensor_2, _ = find_peaks(dados_filtrados[sensor_2])

        # Identificar picos simultâneos
        picos_simultaneos = list(set(peaks_sensor_1).intersection(peaks_sensor_2))

        # Criar o gráfico interativo com Plotly
        fig = go.Figure()

        # Adicionar as linhas dos sensores
        fig.add_trace(
            go.Scatter(
                x=dados_filtrados['HorasDecorridas'],
                y=dados_filtrados[sensor_1],
                mode='lines',
                name=sensor_1,
                line=dict(color='blue')
            )
        )
        fig.add_trace(
            go.Scatter(
                x=dados_filtrados['HorasDecorridas'],
                y=dados_filtrados[sensor_2],
                mode='lines',
                name=sensor_2,
                line=dict(color='green')
            )
        )

        # Adicionar os picos simultâneos
        if picos_simultaneos:
            fig.add_trace(
                go.Scatter(
                    x=dados_filtrados['HorasDecorridas'].iloc[picos_simultaneos],
                    y=dados_filtrados[sensor_1].iloc[picos_simultaneos],
                    mode='markers',
                    name="Picos Simultâneos",
                    marker=dict(color='red', size=8, symbol='circle')
                )
            )

        # Configuração do layout
        fig.update_layout(
            title=f"Detecção de Picos Simultâneos entre {sensor_1} e {sensor_2}",
            xaxis_title="Horas Decorridas",
            yaxis_title="Valores",
            legend_title="Sensores",
            hovermode="x unified",  # Informações detalhadas ao passar o mouse
            template="plotly_white"
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)

def grafico_com_defasagem_para_combinacoes(dados, colunas_selecionadas, lag=1):
    """
    Gera gráficos interativos de comparação temporal para combinações de sensores com defasagem.

    Args:
        dados (DataFrame): DataFrame com os dados.
        colunas_selecionadas (list): Lista de colunas selecionadas para análise.
        lag (int): Número de períodos de defasagem.
    """
    # Gerar todas as combinações possíveis entre os sensores
    combinacoes = list(combinations(colunas_selecionadas, 2))
    
    for sensor_1, sensor_2 in combinacoes:
        # Criar a coluna temporária com o dado defasado
        dados[f'{sensor_1}_lag'] = dados[sensor_1].shift(lag)
        
        # Criar o gráfico interativo com Plotly
        fig = go.Figure()

        # Adicionar os valores defasados
        fig.add_trace(
            go.Scatter(
                x=dados['HorasDecorridas'],
                y=dados[f'{sensor_1}_lag'],
                mode='lines',
                name=f'{sensor_1} (com lag={lag})',
                line=dict(color='blue', dash='dash')  # Linha tracejada para diferenciar
            )
        )

        # Adicionar os valores originais do segundo sensor
        fig.add_trace(
            go.Scatter(
                x=dados['HorasDecorridas'],
                y=dados[sensor_2],
                mode='lines',
                name=sensor_2,
                line=dict(color='green')
            )
        )

        # Configuração do layout
        fig.update_layout(
            title=f"Comparação Temporal: {sensor_1} com Lag {lag} e {sensor_2}",
            xaxis_title="Horas Decorridas",
            yaxis_title="Valores",
            legend_title="Sensores",
            hovermode="x unified",
            template="plotly_white"
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Remover a coluna temporária para não alterar o DataFrame original
        dados.drop(columns=[f'{sensor_1}_lag'], inplace=True)

def normalizar_dados(dados, colunas_selecionadas):
    # Inicializando o escalonador
    scaler = MinMaxScaler()

    # Aplicar o Min-Max Scaling em todas as colunas numéricas
    dados[colunas_selecionadas] = scaler.fit_transform(dados[colunas_selecionadas])

    return dados

def main():
    try:
         # Seleção do experimento
        experimento = st.sidebar.radio("Selecione o experimento:", ["Experimento 1", "Experimento 2"])
        
        if experimento == "Experimento 1":
            google_sheets_url = "data/EXPERIMENTO_1_FISICA_Dados.csv"            
            diretorio_imagens = "EXP_FISICA_imagens_brutas/EXPERIMENTO_1_FISICA" # Diretório onde as imagens estão salvas
            verifica = True

            # Definir data e hora inicial e final
            data_inicial = datetime(2025, 1, 11)
            data_final = datetime(2025, 1, 19)
            hora_inicial = time(11, 23, 00)
            hora_final = time(17, 20, 00)

        elif experimento == "Experimento 2":
            google_sheets_url = "data/EXPERIMENTO_2_FISICA_Dados.csv"  # Substitua pela URL do segundo experimento
            diretorio_imagens = "EXP_FISICA_imagens_brutas/EXPERIMENTO_2_FISICA" # Diretório onde as imagens estão salvas
            verifica = False

            # Definir data e hora inicial e final
            data_inicial = datetime(2025, 1, 24)
            data_final = datetime(2025, 1, 30)
            hora_inicial = time(21, 00, 00)
            hora_final = time(8, 11, 00)

        # Carregar os dados do experimento selecionado
        dados_experimento, dados_removidos = carregar_dados(google_sheets_url)
        dados_inmet = carregar_dados_inmet()
        dados = mesclar_temperatura(dados_experimento, dados_inmet)
        dados = normalizar_dados(dados, ['Temperatura', 'Umidade', 'MQ-3', 'MQ-4', 'MQ-7', 'MQ-8', 'MQ-135','Temperatura_Externa'])

        
        st.sidebar.title("Navegação")
        pagina = st.sidebar.radio("Escolha a página:", [
                                                            "Página Inicial", "Gráfico Interativo", "Time-Lapse",  "Médias Diárias", "Regressão Linear", 
                                                            "Eventos Combinados", "Correlacao com Lag", "Visualizar Fotos", "Informações relevantes"
                                                        ])

        st.sidebar.write("### Selecione o intervalo de tempo para visualização")
        inicio_selecionado = st.sidebar.date_input("Data Inicial", min_value=dados['DataHora'].min().date(),
                                                   max_value=dados['DataHora'].max().date(),
                                                   value=dados['DataHora'].min().date())
        fim_selecionado = st.sidebar.date_input("Data Final", min_value=dados['DataHora'].min().date(),
                                                max_value=dados['DataHora'].max().date(),
                                                value=dados['DataHora'].max().date())
        filtro_visualizacao = (dados['DataHora'] >= pd.Timestamp(inicio_selecionado)) & (dados['DataHora'] <= pd.Timestamp(fim_selecionado) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
        dados_filtrados = dados[filtro_visualizacao]

        st.sidebar.write("### Controle de Visualização")
        colunas_para_visualizacao = ['Temperatura', 'Umidade', 'MQ-3', 'MQ-4', 'MQ-7', 'MQ-8', 'MQ-135','Temperatura_Externa']
        colunas_selecionadas = st.sidebar.multiselect(
            "Selecione os dados para visualização nos gráficos", colunas_para_visualizacao, default=colunas_para_visualizacao
        )

        if colunas_selecionadas:
            nomes_colunas = ['Temperatura', 'Umidade', 'MQ-3', 'MQ-4', 'MQ-7', 'MQ-8', 'MQ-135']
            
            medias_removidos = {col: dados_removidos[col].astype(float).mean() for col in nomes_colunas}
            estatisticas_diarias = calcular_variacoes_diarias(dados_filtrados, colunas_selecionadas)

            if pagina == "Página Inicial":
                exibir_pagina_inicial(dados, estatisticas_diarias, colunas_selecionadas, dados_filtrados, medias_removidos)                                
            elif pagina == "Gráfico Interativo":
                st.title("Gráfico Interativo")
                exibir_graficos_interativos(dados_filtrados, colunas_selecionadas, medias_removidos)
            elif pagina == "Time-Lapse":
                st.title("Time-Lapse")                 
                # Configuração dos arquivos de vídeo
                if verifica:
                    caminhos = ['up','down']
                    for i in caminhos:
                        input_video = f"midia/concave_{i}_timelapse.mp4"
                        output_video = f"midia/concave_{i}_output.mp4"                              
                        verificar_video(input_video, output_video)
                else:
                    input_video = "midia/EXP_2_timelapse.mp4"
                    output_video = "midia/EXP_2_timelapse_output.mp4"                           
                    verificar_video(input_video, output_video)
                    
            elif pagina ==  "Médias Diárias":
                exibir_medias_diarias(dados_filtrados, colunas_selecionadas)
            elif pagina == "Visualizar Fotos":
                exibir_imagens_experimento(diretorio_imagens,data_inicial,data_final,hora_inicial,hora_final)
            elif pagina == "Informações relevantes":
                informacoes()
            elif pagina == "Regressão Linear":
                analisar_regressoes(dados_filtrados, colunas_selecionadas)
            elif pagina == "Eventos Combinados":
                detectar_picos_simultaneos(dados_filtrados, colunas_selecionadas)
            elif pagina == "Correlacao com Lag":
                grafico_com_defasagem_para_combinacoes(dados_filtrados, colunas_selecionadas)

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

if __name__ == "__main__":
    main()