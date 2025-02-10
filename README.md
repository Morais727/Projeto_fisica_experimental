# Dashboard de Análise de Dados de Experimentos Físicos

Este projeto é um **dashboard interativo** desenvolvido em **Python** utilizando a biblioteca **Streamlit**, projetado para a análise de dados coletados de **sensores físicos**. O dashboard oferece visualizações interativas e avançadas para análise de dados como **temperatura**, **umidade**, **gases**, entre outros, além de gerar gráficos interativos, mapas de calor, análises de regressão linear e muito mais.

## Relatório do Experimento

O relatório completo do experimento pode ser encontrado no seguinte link:

[Relatório do Experimento](https://projetosfisicaexperimental.blogspot.com/2025/02/freshness-de-alimentos-pereciveis_10.html)

## Como Executar o Dashboard

### Pré-requisitos

Antes de executar o dashboard, assegure-se de que você possui as seguintes dependências instaladas:

- **Python 3.8** ou superior
- **Pip** (gerenciador de pacotes do Python)

### Instalação das Dependências

1. **Clone o repositório** para o seu ambiente local:

    ```bash
    git clone https://github.com/Morais727/Projeto_fisica_experimental.git
    cd Projeto_fisica_experimental
    ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use venv\Scripts\activate
    ```

3. **Instale as dependências necessárias**:

    ```bash
    pip install -r requirements.txt
    ```

### Executando o Dashboard

Após instalar as dependências, execute o dashboard com o seguinte comando:

```bash
streamlit run dashboard.py
```

O dashboard será iniciado e estará disponível no seu navegador no endereço: http://localhost:8501.

Estrutura do Projeto
O dashboard oferece diversas funcionalidades, acessíveis através da barra lateral:

Página Inicial: Exibe uma tabela com a variação diária dos dados, gráficos não interativos e um mapa de calor da correlação entre os sensores.
Gráfico Interativo: Visualize gráficos interativos dos dados ao longo do tempo.
Time-Lapse: Exibe vídeos time-lapse dos experimentos.
Médias Diárias: Calcula e exibe as médias diárias dos dados selecionados.
Regressão Linear: Realiza análises de regressão linear entre pares de sensores.
Eventos Combinados: Detecta e exibe picos simultâneos em diferentes sensores.
Correlação com Lag: Gera gráficos de comparação temporal com defasagem entre sensores.
Visualizar Fotos: Permite visualizar fotos do experimento com base na data e hora selecionadas.
Informações Relevantes: Exibe detalhes sobre os sensores e informações sobre o experimento.
Dados Utilizados
Os dados utilizados no dashboard são carregados a partir de arquivos CSV, que podem ser locais ou obtidos via URL de uma planilha do Google Sheets. O código também integra dados meteorológicos do [INMET](https://portal.inmet.gov.br/), enriquecendo a análise com informações adicionais.

Personalização
Você pode personalizar o dashboard para carregar diferentes conjuntos de dados ou ajustar suas funcionalidades conforme necessário. Para isso, basta modificar o código para carregar os dados desejados e ajustar as funções de análise e visualização de acordo com os novos dados.

Contribuição
Contribuições são bem-vindas! Se você deseja contribuir para o projeto, sinta-se à vontade para abrir issues ou enviar pull requests. A colaboração é fundamental para o crescimento do projeto.

Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

Desenvolvimento Acadêmico
Este projeto foi desenvolvido como parte da disciplina Projetos de Física Experimental I da UFLA (Universidade Federal de Lavras) no ano de 2024/2.

Esperamos que este dashboard seja útil para a análise de seus experimentos físicos. Se tiver dúvidas ou sugestões, não hesite em entrar em contato!
