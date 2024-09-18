from flask import Flask, request, render_template
from transcrever import transcrever_audio  # Importe sua função de transcrição

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Crie um arquivo HTML simples para upload de arquivos

@app.route('/transcrever', methods=['POST'])
def transcrever():
    if 'audiofile' not in request.files:
        return "Nenhum arquivo de áudio enviado"
    audio_file = request.files['audiofile']
    # Chame sua função de transcrição
    texto_transcrito = transcrever_audio(audio_file)
    return f"Texto transcrito: {texto_transcrito}"

if __name__ == "__main__":
    app.run(debug=True)
