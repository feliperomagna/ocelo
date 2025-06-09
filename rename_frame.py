import os

# Função para renomear arquivos em um diretório
def rename_files_in_directory(directory, prefix="upone"):
    # Obtém a lista de arquivos no diretório
    files = sorted(os.listdir(directory))
    
    for index, filename in enumerate(files):
        # Ignora subdiretórios
        if os.path.isdir(os.path.join(directory, filename)):
            continue
        
        # Define a nova extensão e a nova numeração para o arquivo
        new_name = f"{prefix}{index:04d}.png"

        # Caminhos completo do arquivo antigo e do novo
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        # Renomeia o arquivo
        os.rename(old_path, new_path)
        print(f"{filename} renomeado para {new_name}")

# Exemplo de uso
directory = "/Users/feliperomagna/Document/data/butterfly_comfyui/but_for_flux_two"  # Substitua pelo caminho do diretório com seus arquivos
rename_files_in_directory(directory, prefix="upone")
