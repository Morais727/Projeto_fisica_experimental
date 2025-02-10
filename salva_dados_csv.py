import serial
import time
import csv
import os

# Configuração da porta serial
serial_port = "/dev/ttyUSB0"
baud_rate = 9600

# Nome do arquivo CSV
csv_filename = "dados_arduino.csv"

# Conecta à porta serial
try:
    ser = serial.Serial(serial_port, baud_rate)
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")
    exit() # Encerra o programa se a porta serial não abrir

def read_data_from_serial():
    """Lê os dados da porta serial"""
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            return data

def format_data_to_list(data):
    """Formata os dados para uma lista para o CSV"""
    try:
        # Esperamos que os dados venham no formato "temperature:value,humidity:value,..."
        params = data.split(",")
        formatted_data = {}

        for param in params:
            if ":" in param:
                name, value = param.split(":", 1)
                formatted_data[name.strip()] = value.strip()
            else:
                print(f"Formato inválido ignorado: {param}")

        # Retorna uma lista com os valores, na ordem das chaves
        return list(formatted_data.values())
    except Exception as e:
        print(f"Erro ao formatar os dados: {e}")
        return None

def write_data_to_csv(data):
    """Escreve os dados em um arquivo CSV"""
    if data is None:
        return

    try:
        file_exists = os.path.isfile(csv_filename)
        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                # Escreve o cabeçalho apenas se o arquivo for novo
                header = []
                # Extrai os nomes dos campos do primeiro dado formatado
                primeiro_dado = data
                if primeiro_dado is not None:
                    for item in primeiro_dado:
                        header.append(list(item.keys())[0])
                writer.writerow(header)
            writer.writerow(data)
        print("Dados gravados no CSV com sucesso!")
    except Exception as e:
        print(f"Erro ao escrever no CSV: {e}")

def main():
    print("Iniciando leitura dos dados do Arduino...")

    while True:
        data_serial = read_data_from_serial()
        print(f"Dados recebidos: {data_serial}")
        
        if data_serial: # Verifica se data_serial não é None ou vazio
            data_formatado = format_data_to_list(data_serial)
            data_formatado.append(time.asctime())

            if data_formatado: # Verifica se data_formatado não é None
                write_data_to_csv(data_formatado)

        time.sleep(10)

if __name__ == "__main__":
    main()