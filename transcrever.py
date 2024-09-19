import speech_recognition as sr
from pydub import AudioSegment
from fpdf import FPDF
from tkinter import Tk, Label, Button, filedialog, messagebox, Canvas
from tkinter import ttk  # Para a barra de progresso
from PIL import Image, ImageTk  # Para a imagem de fundo
import os

def audio_to_wav(input_file, wav_file):
    # Converte qualquer arquivo de áudio para WAV
    audio = AudioSegment.from_file(input_file)
    audio.export(wav_file, format="wav")

def transcribe_large_audio(wav_file, status_label, progress_bar):
    recognizer = sr.Recognizer()
    status_label.config(text="Transcrevendo o áudio...")
    progress_bar['value'] = 0

    with sr.AudioFile(wav_file) as source:
        audio_length = source.DURATION
        segment_duration = 30  # segundos
        full_text = ""

        for i in range(0, int(audio_length), segment_duration):
            with sr.AudioFile(wav_file) as source:
                # Processa o áudio em blocos de 30 segundos
                audio_data = recognizer.record(source, duration=segment_duration, offset=i)
                try:
                    # Transcreve usando Google Speech Recognition
                    text = recognizer.recognize_google(audio_data, language="pt-BR")
                    full_text += text + "\n\n"  # Adiciona parágrafos
                except sr.UnknownValueError:
                    full_text += "[Áudio não pôde ser entendido]\n\n"
                except sr.RequestError as e:
                    status_label.config(text=f"Erro no serviço de reconhecimento de fala: {e}")
                    return None
            
            # Atualiza a barra de progresso
            progress_bar['value'] = (i + segment_duration) / audio_length * 100
            progress_bar.update()

    return full_text

def save_text_as_pdf(text, pdf_file):
    # Cria o objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Define a fonte e o tamanho
    pdf.set_font("Arial", size=12)

    # Divide o texto em linhas de acordo com o tamanho da página
    lines = text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, line)
    
    # Salva o PDF
    pdf.output(pdf_file)
    print(f"Arquivo PDF salvo como {pdf_file}")

def transcribe_audio_to_pdf(input_file, pdf_file, status_label, progress_bar):
    wav_file = "temp_audio.wav"
    status_label.config(text="Convertendo áudio para WAV...")
    audio_to_wav(input_file, wav_file)
    
    # Transcreve o arquivo de áudio
    text = transcribe_large_audio(wav_file, status_label, progress_bar)
    
    if text:
        # Formata e salva em PDF
        save_text_as_pdf(text, pdf_file)
        status_label.config(text=f"Transcrição concluída! Arquivo salvo como {pdf_file}")
    else:
        status_label.config(text="Erro na transcrição.")

def choose_file(status_label):
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.m4a *.mp3 *.mp4 *.wav *.ogg *.flac"), ("All Files", "*.*")], title="Escolha o arquivo de áudio")
    if file_path:
        status_label.config(text=f"Arquivo selecionado: {file_path}")
        return file_path
    else:
        status_label.config(text="Nenhum arquivo foi selecionado.")
        return None

# Função para iniciar o processo quando o botão for clicado
def start_transcription(status_label, file_label, progress_bar):
    input_file = file_label["text"].replace("Arquivo selecionado: ", "")
    if input_file:
        pdf_file = os.path.splitext(os.path.basename(input_file))[0] + ".pdf"
        transcribe_audio_to_pdf(input_file, pdf_file, status_label, progress_bar)
    else:
        status_label.config(text="Nenhum arquivo selecionado para transcrição.")

# Função para carregar a imagem de fundo
def load_background(canvas, image_path, root):
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)  # Atualizado para LANCZOS
    bg_image = ImageTk.PhotoImage(bg_image)
    
    # Adiciona a imagem no canvas
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    
    # Manter a referência da imagem para não ser destruída pelo garbage collector
    canvas.image = bg_image

# Cria a interface gráfica
def create_gui():
    root = Tk()
    root.title("Transcrição de Áudio para PDF")
    
    # Maximiza a janela
    root.state('zoomed')

    # Cria o canvas para a imagem de fundo
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)

    # Carrega a imagem de fundo
    load_background(canvas, "background.jpg", root)  # Certifique-se de que o arquivo 'background.jpg' está no mesmo diretório

    # Centralizar o texto
    canvas.create_text(root.winfo_screenwidth() // 2, 100, text="Bem-vindo ao Transcritor de Áudio para PDF", font=("Arial", 18), fill="white")

    # Labels e botões centralizados
    file_label = Label(root, text="Nenhum arquivo selecionado", font=("Arial", 12), bg="#FFFFFF")
    file_label_window = canvas.create_window(root.winfo_screenwidth() // 2, 150, window=file_label)

    status_label = Label(root, text="", font=("Arial", 12), bg="#FFFFFF", fg="green")
    status_label_window = canvas.create_window(root.winfo_screenwidth() // 2, 200, window=status_label)

    select_button = Button(root, text="Selecionar Arquivo de Áudio", command=lambda: file_label.config(text=f"Arquivo selecionado: {choose_file(status_label)}"))
    select_button_window = canvas.create_window(root.winfo_screenwidth() // 2, 250, window=select_button)

    start_button = Button(root, text="Iniciar Transcrição", command=lambda: start_transcription(status_label, file_label, progress_bar))
    start_button_window = canvas.create_window(root.winfo_screenwidth() // 2, 300, window=start_button)

    # Barra de progresso centralizada
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar_window = canvas.create_window(root.winfo_screenwidth() // 2, 350, window=progress_bar)

    exit_button = Button(root, text="Sair", command=root.quit)
    exit_button_window = canvas.create_window(root.winfo_screenwidth() // 2, 400, window=exit_button)

    # Inicia a interface
    root.mainloop()

import os

def is_running_on_server():
    return os.environ.get("RENDER") is not None

# Só chamar a GUI se o código não estiver no servidor
if not is_running_on_server():
    create_gui()