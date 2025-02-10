import os
import shutil
from datetime import datetime

def mover_imagens_com_data(diretorio_origem, diretorio_destino, data_limite):
    """
    Move imagens de um diretório para outro com base na data no nome do arquivo.

    Args:
        diretorio_origem (str): O diretório onde as imagens estão localizadas.
        diretorio_destino (str): O diretório para onde as imagens serão movidas.
        data_limite (datetime): A data limite para a modificação das imagens.
    """
    # Verifica se o diretório de destino existe, se não, cria
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)
    
    # Percorre todos os arquivos no diretório de origem
    for arquivo in os.listdir(diretorio_origem):
        # Obtém o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_origem, arquivo)
        
        # Verifica se é um arquivo e se tem uma imagem válida (por exemplo, com extensão .jpg, .png)
        if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                # Extrai a data do nome do arquivo (assumindo que está no formato 'YYYY-MM-DD_HH-MM-SS')
                data_arquivo_str = arquivo.split('_')[0]  # Pega apenas a parte da data (YYYY-MM-DD)
                data_arquivo = datetime.strptime(data_arquivo_str, "%Y-%m-%d")
                
                # Verifica se a data do arquivo é posterior à data limite
                if data_arquivo > data_limite:
                    # Move o arquivo para o diretório de destino
                    shutil.move(caminho_arquivo, os.path.join(diretorio_destino, arquivo))
                    print(f"Imagem {arquivo} movida para o diretório de destino.")
            except Exception as e:
                print(f"Erro ao processar o arquivo {arquivo}: {e}")

# Defina os diretórios de origem e destino
diretorio_origem = "EXP_FISICA_imagens_experimento-20250130T120524Z-001/EXP_FISICA_imagens_experimento"  # Altere para o diretório de origem
diretorio_destino = "EXP_FISICA_imagens_brutas/EXPERIMENTO_2_FISICA"

# Defina a data limite (21 de janeiro de 2025)
data_limite = datetime(2025, 1, 21)

# Chama a função para mover as imagens
mover_imagens_com_data(diretorio_origem, diretorio_destino, data_limite)
