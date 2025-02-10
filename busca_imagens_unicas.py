import os
import shutil
from PIL import Image
import hashlib

def calculate_image_hash(image_path):
    """
    Calcula o hash de uma imagem para identificar duplicatas.
    """
    hash_md5 = hashlib.md5()
    try:
        with Image.open(image_path) as img:
            img = img.resize((128, 128)).convert('L')  # Redimensiona e converte para tons de cinza
            hash_md5.update(img.tobytes())
    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")
        return None
    return hash_md5.hexdigest()

def calculate_similarity(hash1, hash2):
    """
    Calcula a similaridade entre dois hashes usando a contagem de bits diferentes.
    """
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2)) / len(hash1)

def find_duplicate_images(directory, destination_directory="duplicates", similarity_threshold=0.02):
    """
    Encontra imagens duplicadas em um diretório e move as duplicatas para um novo diretório.
    """
    image_hashes = {}
    duplicates = []

    # Cria o diretório de destino, se não existir
    os.makedirs(destination_directory, exist_ok=True)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                image_path = os.path.join(root, file)
                image_hash = calculate_image_hash(image_path)

                if image_hash:
                    found_duplicate = False
                    for stored_hash, stored_path in image_hashes.items():
                        similarity = calculate_similarity(image_hash, stored_hash)
                        if similarity <= similarity_threshold:
                            duplicates.append((stored_path, image_path))

                            # Move a imagem duplicada para o diretório de destino
                            dest_path = os.path.join(destination_directory, file)
                            shutil.move(image_path, dest_path)
                            print(f"Imagem semelhante movida: {image_path} -> {dest_path}")
                            found_duplicate = True
                            break

                    if not found_duplicate:
                        image_hashes[image_hash] = image_path

    return duplicates

def main():
    directory = "EXP_FISICA_imagens_experimento"
    destination_directory = "similar_images"  # Diretório para salvar duplicatas
    similarity_threshold = 0.08  # Limite de similaridade 

    print("Buscando imagens semelhantes...")
    duplicates = find_duplicate_images(directory, destination_directory, similarity_threshold)

    if duplicates:
        print("\nImagens semelhantes encontradas e movidas:")
        for original, duplicate in duplicates:
            print(f"  - {original} é semelhante a {duplicate}")
    else:
        print("Nenhuma imagem semelhante encontrada.")

if __name__ == "__main__":
    main()
