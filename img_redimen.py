import cv2
import os

# Definir o caminho para o diretório contendo as imagens
diretorio_imagens = '/Users/feliperomagna/Document/data/butterfly_comfyui/frames'
diretorio_salvar = '/Users/feliperomagna/Document/data/butterfly_comfyui/frames_red'

# Verificar se o diretório de saída existe, caso contrário, criar
if not os.path.exists(diretorio_salvar):
    os.makedirs(diretorio_salvar)

# Definir a nova largura e altura
nova_largura = 2048
nova_altura = 1152

# Contador para processar apenas as primeiras 400 imagens
contador = 0
limite_imagens = 1572

# Percorrer todas as imagens no diretório
for nome_arquivo in os.listdir(diretorio_imagens):
    if contador >= limite_imagens:
        break

    # Verificar se o arquivo é uma imagem PNG
    if nome_arquivo.lower().endswith('.png'):
        # Caminho completo da imagem
        caminho_imagem = os.path.join(diretorio_imagens, nome_arquivo)

        # Carregar a imagem
        imagem = cv2.imread(caminho_imagem)

        # Verificar se a imagem foi carregada corretamente
        if imagem is None:
            print(f"Erro ao carregar a imagem: {caminho_imagem}")
            continue

        # Redimensionar a imagem
        imagem_redimensionada = cv2.resize(imagem, (nova_largura, nova_altura))

        # Caminho completo para salvar a imagem redimensionada
        caminho_salvar = os.path.join(diretorio_salvar, nome_arquivo)

        # Salvar a imagem redimensionada
        cv2.imwrite(caminho_salvar, imagem_redimensionada)

        # Incrementar o contador
        contador += 1

print(f"{contador} imagens foram redimensionadas e salvas em '{diretorio_salvar}'")
