import os
import shutil
from PIL import Image
import imagehash

def calculate_image_hash(image_path):
    """
    Calcula o hash perceptual de uma imagem.
    """
    try:
        with Image.open(image_path) as img:
            return imagehash.average_hash(img)
    except Exception as e:
        print(f"Erro ao calcular hash da imagem {image_path}: {e}")
        return None

def find_similar_images(reference_image_path, directory, similarity_threshold=0.25, destination_directory="similar_images"):
    """
    Encontra imagens semelhantes no diretório com base em uma imagem de referência e move para um novo diretório.
    """
    # Calcula o hash da imagem de referência
    reference_hash = calculate_image_hash(reference_image_path)
    if reference_hash is None:
        print("Erro ao calcular o hash da imagem de referência.")
        return []

    similar_images = []

    # Cria o diretório de destino, se não existir
    os.makedirs(destination_directory, exist_ok=True)

    # Percorre o diretório para comparar os hashes
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff')):
                image_path = os.path.join(root, file)
                target_hash = calculate_image_hash(image_path)
                if target_hash:
                    # Calcula a diferença de hash
                    difference = reference_hash - target_hash
                    similarity = difference / len(reference_hash.hash.flatten())
                    if similarity <= similarity_threshold:
                        similar_images.append((image_path, similarity * 100))

                        # Move a imagem para o diretório de destino
                        dest_path = os.path.join(destination_directory, file)
                        shutil.move(image_path, dest_path)
                        print(f"Imagem semelhante movida: {image_path} -> {dest_path}")

    return similar_images

def main():
    # Caminho da imagem de referência
    reference_image_path = "EXP_FISICA_imagens_experimento/2025-01-13_06-30-27.jpg"
    # Caminho do diretório onde buscar as imagens
    directory = "EXP_FISICA_imagens_experimento"
    # Limite de similaridade (25% de diferença)
    similarity_threshold = 0.05

    print(f"Buscando imagens semelhantes a: {reference_image_path} com até {similarity_threshold * 100}% de diferença...")

    similar_images = find_similar_images(reference_image_path, directory, similarity_threshold)

    if similar_images:
        print("\nImagens semelhantes encontradas e movidas:")
        for image_path, similarity in similar_images:
            print(f"  - {image_path} com diferença de {similarity:.2f}%")
    else:
        print("\nNenhuma imagem semelhante encontrada.")

if __name__ == "__main__":
    main()
