from flask import Flask, render_template, request, send_file
import requests
from pytubefix import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
RECAPTCHA_SECRET = "6Ld0aa0qAAAAAJrbEnUxeFdJtxZHMrTnFMo88RKy"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def verify_recaptcha(response):
    """
    Verifica la respuesta del reCAPTCHA con la clave secreta.
    """
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        'secret': RECAPTCHA_SECRET,
        'response': response
    }
    r = requests.post(url, data=data)
    return r.json().get("success", False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Validar reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_response):
            return "Error: Verificación de reCAPTCHA fallida. Inténtalo de nuevo."

        # Obtener la URL del video desde el formulario
        url = request.form.get('video_url')
        yt = YouTube(url, use_po_token=True)

        # Seleccionar la mejor resolución disponible
        video_stream = yt.streams.get_highest_resolution()
        filepath = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
        video_stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp4")

        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)