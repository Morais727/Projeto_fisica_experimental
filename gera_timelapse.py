import os
from datetime import datetime, timedelta
from PIL import Image
import cv2
import shutil

def parse_timestamp_from_filename(filename):
    """
    Extrai o timestamp do nome do arquivo no formato 'YYYY-MM-DD_HH-MM-SS.jpg'.
    """
    try:
        timestamp_str = filename.split('.')[0]  # Remove a extensão
        return datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
    except ValueError:
        print(f"Erro ao analisar o timestamp de {filename}. Nome inválido.")
        return None

def clear_directory(directory):
    """
    Remove todos os arquivos do diretório especificado.
    """
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


def select_images_for_timelapse(directory, output_directory, interval_minutes=30):
    """
    Seleciona imagens espaçadas por um intervalo de tempo para criar um timelapse.
    As imagens originais não são movidas.
    """

    # Lista todos os arquivos na pasta
    images = [
        file for file in os.listdir(directory)
        if file.lower().endswith(('png', 'jpg', 'jpeg'))
    ]

    # Extrai timestamps e associa ao nome do arquivo
    images_with_timestamps = []
    for image in images:
        timestamp = parse_timestamp_from_filename(image)
        if timestamp:
            images_with_timestamps.append((timestamp, image))

    # Ordena por timestamp
    images_with_timestamps.sort(key=lambda x: x[0])

    # Seleciona imagens espaçadas pelo intervalo de tempo
    selected_images = []
    last_selected_time = None

    for timestamp, image in images_with_timestamps:
        if last_selected_time is None or timestamp >= last_selected_time + timedelta(minutes=interval_minutes):
            selected_images.append(image)
            last_selected_time = timestamp

    # Copia as imagens selecionadas para o diretório de saída
    for image in selected_images:
        src_path = os.path.join(directory, image)
        dest_path = os.path.join(output_directory, image)
        shutil.copy(src_path, dest_path)
        print(f"Imagem selecionada: {src_path} -> {dest_path}")

    print(f"\nTotal de imagens selecionadas: {len(selected_images)}")
    return [os.path.join(output_directory, image) for image in selected_images]

def create_timelapse(images, output_video_path, fps=30):
    """
    Cria um vídeo timelapse a partir de uma lista de imagens, adicionando o nome da imagem como texto no quadro.
    """
    if not images:
        print("Nenhuma imagem selecionada para criar o timelapse.")
        return

    # Determina o tamanho do vídeo com base na primeira imagem
    first_image = cv2.imread(images[0])
    height, width, _ = first_image.shape

    # Inicializa o codificador de vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # Branco
    thickness = 2
    text_position = (10, height - 10)  # Posição na base da imagem

    for image_path in images:
        frame = cv2.imread(image_path)
        if frame is not None:
            # Adiciona o texto com o nome da imagem
            text = os.path.basename(image_path)
            text = text.split('.')[0]  # Remove a extensão
            cv2.putText(frame, text, text_position, font, font_scale, font_color, thickness, lineType=cv2.LINE_AA)
            video.write(frame)
            print(f"Adicionando ao vídeo: {image_path}")
        else:
            print(f"Erro ao carregar imagem: {image_path}")

    video.release()
    print(f"Timelapse criado em: {output_video_path}")

def main():
    # # Limpa o diretório de saída antes de copiar novas imagens
    # clear_directory('output_folder/concave_down/images_for_video')
    # clear_directory('output_folder/concave_up/images_for_video')
    # clear_directory('midia')

    
    
    # caminhos = ['up','down']
    
    # for i in caminhos:
    #     input_directory = f"output_folder/concave_{i}"
    #     output_directory = f"output_folder/concave_{i}/images_for_video"  # Substitua pelo caminho para salvar as imagens selecionadas
    #     output_video_path = f"midia/concave_{i}_timelapse.mp4"  # Substitua pelo caminho para salvar o vídeo
    #     interval_minutes = 2  # Intervalo desejado em minutos
    #     fps = 30  # Quadros por segundo no vídeo

    #     os.makedirs(output_directory, exist_ok=True)

    #     print(f"Selecionando imagens a cada {interval_minutes} minutos...")
    #     selected_images = select_images_for_timelapse(input_directory, output_directory, interval_minutes)

    #     print("\nCriando o timelapse...")
    #     create_timelapse(selected_images, output_video_path, fps)

    clear_directory = "images_for_video_EXP_2"
    input_directory ="EXP_FISICA_imagens_brutas/EXPERIMENTO_2_FISICA"
    output_directory = "images_for_video_EXP_2"
    output_video_path = f"midia/EXP_2_timelapse.mp4"  # Substitua pelo caminho para salvar o vídeo
    interval_minutes = 5  # Intervalo desejado em minutos
    fps = 30  # Quadros por segundo no vídeo

    os.makedirs(output_directory, exist_ok=True)

    print(f"Selecionando imagens a cada {interval_minutes} minutos...")
    selected_images = select_images_for_timelapse(input_directory, output_directory, interval_minutes)

    print("\nCriando o timelapse...")
    create_timelapse(selected_images, output_video_path, fps)

if __name__ == "__main__":
    main()
