import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
from random import randint
import os
from PIL import Image
import io

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    try:
        p = {"prompt": prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
        response = json.loads(urllib.request.urlopen(req).read())
        print(f"Prompt {prompt} enfileirado com sucesso. ID do prompt: {response['prompt_id']}")
        return response
    except Exception as e:
        print(f"Erro ao enfileirar o prompt: {e}")
        return None

def get_image(filename, subfolder, folder_type):
    try:
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
            print(f"Imagem {filename} obtida com sucesso.")
            return response.read()
    except Exception as e:
        print(f"Erro ao obter a imagem: {e}")
        return None

def get_history(prompt_id):
    try:
        with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
            print(f"Histórico do prompt {prompt_id} obtido com sucesso.")
            return json.loads(response.read())
    except Exception as e:
        print(f"Erro ao obter o histórico: {e}")
        return None

def get_images(ws, prompt):
    try:
        prompt_id = queue_prompt(prompt)['prompt_id']
        if not prompt_id:
            print("Erro ao enfileirar o prompt.")
            return {}

        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        print(f"Execução do prompt {prompt_id} concluída.")
                        break #Execution is done
            else:
                print("Recebido dado binário (pré-visualização)")
                continue #previews are binary data

        history = get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        image_data = get_image(image['filename'], image['subfolder'], image['type'])
                        if image_data:
                            images_output.append(image_data)
                    output_images[node_id] = images_output

        print(f"Imagens para o prompt {prompt_id} obtidas com sucesso.")
        return output_images
    except Exception as e:
        print(f"Erro ao obter imagens: {e}")
        return {}

with open(r"/Users/feliperomagna/Document/data/butterfly_comfyui/workflow_up_one.json", "r", encoding="utf-8") as f:
    workflow_data = f.read()

workflow = json.loads(workflow_data)

#==================================
image_dir = "/Users/feliperomagna/Document/data/butterfly_comfyui/up_one"

# Obter todos os arquivos de imagem
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])

for i in range(0, 104):
    image_file = os.path.join(image_dir, f"butone{i:04d}.png")

    if not os.path.exists(image_file):
        print(f"Imagem não encontrada: {image_file}")
        continue

    # Definir o arquivo de imagem para o workflow
    workflow["2"]["inputs"]["image"] = image_file

    # Definir parâmetros adicionais para o workflow
    # workflow["4"]["inputs"]["ckpt_name"] = "realvisxlV40_v40LightningBakedvae.safetensors"

    # seed = randint(0, 1000000000)
    # workflow["3"]["inputs"]["noise_seed"] = seed

    try:
        print(f"Conectando ao servidor WebSocket em ws://{server_address}/ws?clientId={client_id}")
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
        print("Conexão WebSocket estabelecida com sucesso.")
        images = get_images(ws, workflow)

        # Descomente as linhas a seguir para exibir as imagens de saída
        for node_id in images:
            for image_data in images[node_id]:
                image = Image.open(io.BytesIO(image_data))
                # image.show()
    except Exception as e:
        print(f"Erro ao conectar ou processar imagens: {e}")
