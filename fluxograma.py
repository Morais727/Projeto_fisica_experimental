from graphviz import Digraph

# Criação do fluxograma com melhorias visuais e detalhamento adicional
fluxograma = Digraph("Fluxograma do Projeto Melhorado", format="pdf")
fluxograma.attr(rankdir="TB", size="8", dpi="300")

# Etapas principais do projeto
fluxograma.node("A0", "Início do projeto (19/12)", shape="ellipse", style="filled", color="lightblue")
fluxograma.node("A", "Etapa 1: Preparação do Ambiente", shape="box", style="filled", color="lightgray")
fluxograma.node("B", "Etapa 2: Configuração de Hardware", shape="box", style="filled", color="lightgray")
fluxograma.node("C", "Etapa 3: Comunicação Arduino ↔ ESP32-CAM", shape="box", style="filled", color="lightgray")
fluxograma.node("D", "Etapa 4: Processamento e Envio de Dados", shape="box", style="filled", color="lightgray")
fluxograma.node("E", "Etapa 5: Análise de Dados no Servidor", shape="box", style="filled", color="lightgray")
fluxograma.node("F", "Etapa 6: Validação e Iteração", shape="box", style="filled", color="lightgray")
fluxograma.node("G", "Resultado Final (24/01)", shape="ellipse", style="filled", color="lightblue")

# Subetapas detalhadas
# Etapa 1
fluxograma.node("A1", "Comprar componentes", style="filled", color="green")
fluxograma.node("A2", "Montar suporte para sensores" ,style="filled", color="green")
fluxograma.node("A3", "Verificação inicial do ambiente" ,style="filled", color="green")

fluxograma.edge("A", "A1")
fluxograma.edge("A", "A2")
fluxograma.edge("A2", "A3")

# Etapa 2
fluxograma.node("B1", "Configuração do Arduino" , style="filled", color="green")
fluxograma.node("B2", "Configuração do ESP32-CAM" , style="filled", color="green")
fluxograma.node("B3", "Teste inicial do hardware" , style="filled", color="green")

fluxograma.edge("B", "B1")
fluxograma.edge("B", "B2")
fluxograma.edge("B2", "B3")

# Etapa 3
fluxograma.node("C1", "Configuração da UART", style="filled", color="green")
fluxograma.node("C2", "Teste de recepção de dados", style="filled", color="green")
fluxograma.node("C3", "Verificação da comunicação bidirecional", style="filled", color="green")

fluxograma.edge("C", "C1")
fluxograma.edge("C1", "C2")
fluxograma.edge("C2", "C3")

# Etapa 4
fluxograma.node("D1", "Captura de imagens", style="filled", color="green")
fluxograma.node("D2", "Integração de dados dos sensores", style="filled", color="green")
fluxograma.node("D3", "Configuração de API no servidor", style="filled", color="green")
fluxograma.node("D4", "Envio HTTP para o servidor", style="filled", color="green")

fluxograma.edge("D", "D1")
fluxograma.edge("D", "D2")
fluxograma.edge("D", "D3")
fluxograma.edge("D3", "D4")

# Etapa 5
fluxograma.node("E1", "Armazenamento no servidor", style="filled", color="green")
fluxograma.node("E2", "Pré-processamento de dados", style="filled", color="green")
fluxograma.node("E3", "Treinamento de Redes Neurais")
fluxograma.node("E3.1", "CNN para imagens")
fluxograma.node("E3.2", "MLP para sensores")
fluxograma.node("E4", "Integração dos resultados")
fluxograma.node("E5", "Dashboard para visualização", style="filled", color="green")

fluxograma.edge("E", "E1")
fluxograma.edge("E", "E2")
fluxograma.edge("E", "E3")
fluxograma.edge("E3", "E3.1")
fluxograma.edge("E3", "E3.2")
fluxograma.edge("E3.2", "E4")
fluxograma.edge("E3.1", "E4")
fluxograma.edge("E2", "E5")

# Etapa 6
fluxograma.node("F1", "Validação dos modelos")
fluxograma.node("F2", "Ajustes nos parâmetros")
fluxograma.node("F3", "Teste final do sistema")

fluxograma.edge("F", "F1")
fluxograma.edge("F1", "F2")
fluxograma.edge("F2", "F3")

# Conexões principais
fluxograma.edge("A0", "A")
fluxograma.edge("A", "B")
fluxograma.edge("B", "C")
fluxograma.edge("C", "D")
fluxograma.edge("D", "E")
fluxograma.edge("E", "F")
fluxograma.edge("F", "G")

# Adição de uma legenda
fluxograma.node(f"Legenda", "Cores:\n Azul - Início/Fim\n Verde - Etapas Concluídas\n Cinza - Etapas", shape="note", style="dashed")

# Gerar e visualizar
fluxograma.render("fluxograma_projeto_melhorado", view=True)