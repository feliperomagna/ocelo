import cv2
import os

def save_frames_from_video(video_path, output_folder):
    # Cria a pasta de saída se ela não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Captura o vídeo
    video_capture = cv2.VideoCapture(video_path)
    
    frame_count = 0

    while True:
        # Lê o frame do vídeo
        ret, frame = video_capture.read()

        # Se o frame não foi capturado, significa que chegamos ao final do vídeo
        if not ret:
            break

        # Define o nome do arquivo de saída
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.png")

        # Salva o frame como uma imagem
        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    # Libera o vídeo
    video_capture.release()
    print(f"Total de {frame_count} frames salvos na pasta '{output_folder}'.")

# Exemplo de uso
video_path = '/Users/feliperomagna/Document/data/butterfly_comfyui/shot_of_a_jaguar_cautiously_stepping_back_into_the_dense_rainforest_disappearing_among_the_trees_an_fmdnlr1vnro6xcm9oe0p_1.mov'
output_folder = '/Users/feliperomagna/Document/data/butterfly_comfyui/frames_onca2'
save_frames_from_video(video_path, output_folder)
