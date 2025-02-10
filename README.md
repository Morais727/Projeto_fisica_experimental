Dashboard de Análise de Dados de Experimentos Físicos
Este projeto é um dashboard interativo desenvolvido em Python utilizando a biblioteca Streamlit para análise de dados de experimentos físicos. O dashboard permite visualizar e analisar dados coletados de sensores, como temperatura, umidade e gases, além de gerar gráficos interativos, mapas de calor, análises de regressão linear e muito mais.

Como Executar o Dashboard
Pré-requisitos
Antes de executar o dashboard, certifique-se de que você possui as seguintes dependências instaladas:

Python 3.8 ou superior

Pip (gerenciador de pacotes do Python)

Instalação das Dependências
Clone o repositório para o seu ambiente local:

bash
Copy
git clone https://github.com/Morais727/Projeto_fisica_experimental.git
cd Projeto_fisica_experimental
Crie um ambiente virtual (opcional, mas recomendado):

bash
Copy
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
Instale as dependências necessárias:

bash
Copy
pip install -r requirements.txt
O arquivo requirements.txt deve conter as seguintes bibliotecas:

plaintext
Copy
streamlit
pandas
numpy
scipy
matplotlib
plotly
seaborn
scikit-learn
Pillow
Executando o Dashboard
Após instalar as dependências, você pode executar o dashboard com o seguinte comando:

bash
Copy
streamlit run dashboard.py
Substitua nome_do_arquivo.py pelo nome do arquivo Python que contém o código do dashboard.

O dashboard será iniciado e estará disponível no seu navegador no endereço http://localhost:8501.

Estrutura do Projeto
O projeto é composto por várias funcionalidades que podem ser acessadas através da barra lateral do dashboard:

Página Inicial: Exibe uma tabela de variação diária dos dados, gráficos não interativos e um mapa de calor da correlação entre os sensores.

Gráfico Interativo: Permite visualizar gráficos interativos dos dados ao longo do tempo.

Time-Lapse: Exibe vídeos time-lapse dos experimentos.

Médias Diárias: Calcula e exibe as médias diárias dos dados selecionados.

Regressão Linear: Realiza análises de regressão linear entre pares de sensores.

Eventos Combinados: Detecta e exibe picos simultâneos em diferentes sensores.

Correlação com Lag: Gera gráficos de comparação temporal com defasagem entre os sensores.

Visualizar Fotos: Permite visualizar fotos do experimento com base na data e hora selecionadas.

Informações Relevantes: Exibe informações sobre os sensores e detalhes do experimento.

Dados Utilizados
Os dados utilizados no dashboard são carregados a partir de arquivos CSV, que podem ser locais ou obtidos via URL de uma planilha do Google Sheets. O código também realiza a integração com dados meteorológicos do INMET para enriquecer a análise.

Personalização
Você pode personalizar o dashboard para carregar diferentes conjuntos de dados ou ajustar as funcionalidades conforme necessário. Basta modificar o código para carregar os dados desejados e ajustar as funções de análise e visualização.

Contribuição
Se você deseja contribuir para o projeto, sinta-se à vontade para abrir issues ou enviar pull requests. Todas as contribuições são bem-vindas!

Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

Esperamos que este dashboard seja útil para a análise dos seus experimentos físicos! Se tiver alguma dúvida ou sugestão, não hesite em entrar em contato.
