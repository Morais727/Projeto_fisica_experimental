import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')

# Criando o diagrama do circuito
d = schemdraw.Drawing()

# Arduino (para leitura dos sensores de gás) - Representação como microcontrolador
arduino_start = (0, 0)  # Posição de início para o Arduino
arduino_width = 4       # Largura do retângulo
arduino_height = 3      # Altura do retângulo

# Criando o retângulo do Arduino
d.add(elm.Line().right().length(arduino_width).at(arduino_start))   # Linha superior
d.add(elm.Line().down().length(arduino_height).at((arduino_start[0] + arduino_width, arduino_start[1])))  # Linha direita
d.add(elm.Line().left().length(arduino_width).at((arduino_start[0] + arduino_width, arduino_start[1] - arduino_height)))  # Linha inferior
d.add(elm.Line().up().length(arduino_height).at((arduino_start[0], arduino_start[1] - arduino_height)))  # Linha esquerda

# Colocando o label dentro do retângulo do Arduino
d.add(elm.Label('Arduino\n(Sensores)').at((arduino_start[0] + arduino_width / 2, arduino_start[1] - arduino_height / 2)))

# ESP32 (para captura de imagens e envio via HTTP)
esp32_start = (6, 0)  # Posição de início para o ESP32
esp32_width = 4        # Largura do retângulo
esp32_height = 3       # Altura do retângulo

# Criando o retângulo do ESP32
d.add(elm.Line().right().length(esp32_width).at(esp32_start))   # Linha superior
d.add(elm.Line().down().length(esp32_height).at((esp32_start[0] + esp32_width, esp32_start[1])))  # Linha direita
d.add(elm.Line().left().length(esp32_width).at((esp32_start[0] + esp32_width, esp32_start[1] - esp32_height)))  # Linha inferior
d.add(elm.Line().up().length(esp32_height).at((esp32_start[0], esp32_start[1] - esp32_height)))  # Linha esquerda

# Colocando o label dentro do retângulo do ESP32
d.add(elm.Label('ESP32\n(Captura Imagens)').at((esp32_start[0] + esp32_width / 2, esp32_start[1] - esp32_height / 2)))

# Sensores MQ (conectados ao Arduino)
mq3 = d.add(elm.Resistor().left().label("MQ-3", loc="top"))
mq4 = d.add(elm.Resistor().left().label("MQ-4", loc="top"))
mq7 = d.add(elm.Resistor().left().label("MQ-7", loc="top"))
mq8 = d.add(elm.Resistor().left().label("MQ-8", loc="top"))
mq135 = d.add(elm.Resistor().left().label("MQ-135", loc="top"))

# Sensor de temperatura e umidade (conectado ao Arduino)
dht11 = d.add(elm.Resistor().left().label("DHT11", loc="top"))

# Conexões entre os sensores e o Arduino
for sensor in [mq3, mq4, mq7, mq8, mq135, dht11]:
    d.add(elm.Line().right().at(sensor.start).tox(arduino_start))

# Conexão entre o Arduino e o ESP32 (via comunicação serial)
d.add(elm.Line().right().at((arduino_start[0] + arduino_width, arduino_start[1] - arduino_height / 2)).length(2))  # Comunicação Serial
d.add(elm.Line().right().at((arduino_start[0] + arduino_width + 2, arduino_start[1] - arduino_height / 2)).tox(esp32_start))  # Envio via HTTP

# Alimentação (5V e GND para o Arduino) - Agora à direita
vcc = d.add(elm.SourceV().up().at((arduino_start[0] + arduino_width + 7, arduino_start[1])))
gnd = d.add(elm.Ground().down().at((arduino_start[0] + arduino_width + 8, arduino_start[1] - arduino_height)))

# Salvar o diagrama
d.save('diagrama_circuito.png')
