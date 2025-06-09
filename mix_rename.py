import os

def renomear_arquivos_par(diretorio):
    # Listar todos os arquivos no diretório
    arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    # Filtrar apenas os arquivos de imagem (por exemplo, PNG, JPG, JPEG)
    extensoes_imagem = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    arquivos_imagem = [f for f in arquivos if os.path.splitext(f)[1].lower() in extensoes_imagem]

    # Renomear os arquivos com numeração par
    contador = 2
    for arquivo in arquivos_imagem:
        nova_extensao = os.path.splitext(arquivo)[1]
        novo_nome = f"mix{contador:03d}{nova_extensao}"  # Exemplo: imagem_002.png
        os.rename(os.path.join(diretorio, arquivo), os.path.join(diretorio, novo_nome))
        contador += 2  # Incrementa por 2 para garantir numeração par

# Exemplo de uso
diretorio = '/Users/feliperomagna/Document/data/butterfly_comfyui/but_section_two'
renomear_arquivos_par(diretorio)

