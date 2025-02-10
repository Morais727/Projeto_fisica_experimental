import serial
import requests
import time

# Configuração da porta serial
serial_port = "/dev/ttyUSB0"  
baud_rate = 9600

# URL do servidor onde os dados serão enviados
server_url = "https://script.google.com/macros/s/AKfycbxzhZMYWJfwdQCrudlleLUzTCNrczItP8tLbW2msph1eCn4EEHpuP7QlKHoc6bciPKo/exec"

# Conecta à porta serial
ser = serial.Serial(serial_port, baud_rate)

def read_data_from_serial():
    """Lê os dados da porta serial"""
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()  # Lê uma linha da serial
            return data


def format_data_to_url(data):
    """Formata os dados para a URL em formato query string"""
    try:
        # Esperamos que os dados venham no formato "temperature:value,humidity:value,..."
        params = data.split(",")  # Divide os dados em partes com base na vírgula
        formatted_data = []
        
        # Para cada item, separa nome e valor e formata para "nome=valor"
        for param in params:
            if ":" in param:  # Verifica se contém ":"
                name, value = param.split(":", 1)  # Divide nome e valor, ignorando valores extras
                formatted_data.append(f"{name.strip()}={value.strip()}")  # Remove espaços e formata
            else:
                print(f"Formato inválido ignorado: {param}")
        
        # Junta todos os parâmetros com "&" e retorna a string resultante
        return "&".join(formatted_data)
    except Exception as e:
        print(f"Erro ao formatar os dados: {e}")
        return ""  # Retorna string vazia em caso de erro


def send_data_to_server(data):
    """Envia os dados para o servidor via HTTP GET"""
    try:
        # Formata os dados para a URL
        formatted_data = format_data_to_url(data)
        url = f"{server_url}?{formatted_data}"  # Adiciona os dados formatados à URL
        
        response = requests.get(url)
        print(url)  # Imprime a URL chamada para depuração
        print(response)  # Imprime a resposta da requisição
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            print("Dados enviados com sucesso!")
        else:
            print(f"Erro ao enviar dados. Código de resposta: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def main():
    print("Iniciando leitura dos dados do Arduino...")

    while True:
        # Lê os dados do Arduino
        data = read_data_from_serial() 
        print(f"Dados recebidos: {data}")
        
        # Envia os dados para o servidor
        send_data_to_server(data)

        # Aguarda 10 segundos antes de ler novamente
        time.sleep(10)

if __name__ == "__main__":
    main()


