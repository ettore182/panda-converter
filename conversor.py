import os

def convert_mp4_to_m4a(input_file, output_file):
    # Verifica se o arquivo de entrada existe
    if os.path.exists(input_file):
        # Renomeia o arquivo MP4 para M4A
        os.rename(input_file, output_file)
        print(f"Arquivo convertido para {output_file}")
    else:
        print("Arquivo de entrada não encontrado.")

# Exemplo de uso:
input_file = 'audio.mp4'  # Arquivo MP4 de áudio
output_file = 'audio.m4a'  # Novo nome com extensão M4A
convert_mp4_to_m4a(input_file, output_file)
