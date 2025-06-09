import cv2
import os

# Função para segmentar um vídeo em frames e salvar apenas um a cada N frames
def segment_video_to_frames(video_file, output_dir="frames_onca", frame_step=1):
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Captura o vídeo
    cap = cv2.VideoCapture(video_file)

    # Verifica se o vídeo foi aberto com sucesso
    if not cap.isOpened():
        print("Erro ao abrir o arquivo de vídeo.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total de frames no vídeo: {frame_count}")

    frame_index = 0
    saved_frame_index = 0

    while True:
        # Lê um frame do vídeo
        ret, frame = cap.read()
        if not ret:
            break

        # Salva apenas um frame a cada frame_step frames
        if frame_index % frame_step == 0:
            # Define o caminho para salvar o frame
            frame_path = os.path.join(output_dir, f"frame{saved_frame_index:04d}.png")
            # Salva o frame como uma imagem
            cv2.imwrite(frame_path, frame)
            print(f"Frame {saved_frame_index} salvo em {frame_path}")
            saved_frame_index += 1

        frame_index += 1

    # Libera o objeto de captura de vídeo
    cap.release()
    print("Processamento concluído.")

# Exemplo de uso
video_file = "/Users/feliperomagna/Document/data/butterfly_comfyui/shot_of_a_jaguar_cautiously_stepping_back_into_the_dense_rainforest_disappearing_among_the_trees_an_fmdnlr1vnro6xcm9oe0p_1.mov"  # Substitua pelo caminho do seu arquivo de vídeo
segment_video_to_frames(video_file, output_dir="frames_onca2", frame_step=0)
