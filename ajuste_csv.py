import pandas as pd
from datetime import datetime

def filtrar_csv(arquivo_entrada, arquivo_saida, data_limite):
    # Lê o CSV
    df = pd.read_csv(arquivo_entrada, header=None)
    
    # Converte a primeira coluna para datetime
    df[0] = pd.to_datetime(df[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    # Define a data e hora limite
    data_limite = datetime.strptime(data_limite, "%d/%m/%Y %Hh")
    
    # Filtra os dados
    df_filtrado = df[df[0] > data_limite]
    
    # Salva os dados filtrados em um novo CSV
    df_filtrado.to_csv(arquivo_saida, index=False, header=False)

# Exemplo de uso
arquivo_entrada = "data/EXPERIMENTO_1_FISICA_Dados.csv"
arquivo_saida = "data/EXPERIMENTO_11_FISICA_Dados.csv"
data_limite = "24/01/2020 21h"

filtrar_csv(arquivo_entrada, arquivo_saida, data_limite)
