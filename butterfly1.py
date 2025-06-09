#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
from random import randint
from PIL import Image
import io
import os
from random import uniform

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

#==================================
def linear_map(value, in_min, in_max, out_min, out_max):
    input_span = in_max - in_min
    output_span = out_max - out_min 
    value_scaled = float(value - in_min) / float(input_span)
    return out_min + (value_scaled * output_span)


# load the workflow JSON from file
with open(r"/Users/feliperomagna/Document/data/butterfly_comfyui/workflow_but_one.json", "r", encoding="utf-8") as f:
    workflow_data = f.read()

workflow = json.loads(workflow_data)


#==================================
image_dir = "/Users/feliperomagna/Documents/Pessoais/Doutorado/Doutorado UFMG/Disciplinas/2024/python24/butterfly_comfyui/frames_red"

# Obter todos os arquivos de imagem
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])

for i in range(0, 105):
    image_file = os.path.join(image_dir, f"frame{i:04d}.png")

    if not os.path.exists(image_file):
        continue

    # Definir o arquivo de imagem para o workflow
    workflow["13"]["inputs"]["image"] = image_file

    # Definir parâmetros adicionais para o workflow
    # workflow["7"]["inputs"]["text"] = "text, watermark, cartoon, anime, person, face, sketch, drawing, illustration, painting, people, body, letters"
    workflow["4"]["inputs"]["ckpt_name"] = "realvisxlV40_v40LightningBakedvae.safetensors"


    seed = randint(0, 1000000)
    #denoise = uniform(0.90, 0.99)
    workflow["3"]["inputs"]["seed"] = seed
    #workflow["3"]["inputs"]["denoise"] = denoise
    
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, workflow)

    # Descomente as linhas a seguir para exibir as imagens de saída
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))