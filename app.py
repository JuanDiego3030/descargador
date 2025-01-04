from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import shutil

app = Flask(__name__)

# Ruta predeterminada para guardar los videos
DEFAULT_DOWNLOAD_PATH = "downloads"

# Asegurarse de que la carpeta de descargas existe
if not os.path.exists(DEFAULT_DOWNLOAD_PATH):
    os.makedirs(DEFAULT_DOWNLOAD_PATH)

# Página principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener enlace de YouTube y ruta de descarga
        video_link = request.form.get("video_link")
        user_path = request.form.get("download_path", DEFAULT_DOWNLOAD_PATH)
        
        # Verificar que los campos no estén vacíos
        if not video_link or not user_path:
            return "Faltan datos: Link o ruta de descarga", 400

        # Descargar video
        try:
            screen_title = "Descargando..."
            mp4_video = YouTube(video_link).streams.get_highest_resolution().download(user_path)

            # Abrir y cerrar el video con moviepy para verificar que se descargó correctamente
            vid_clip = VideoFileClip(mp4_video)
            vid_clip.close()

            screen_title = "Descarga completa"
            return f"Descarga completa: {mp4_video}", 200

        except Exception as e:
            return f"Error en la descarga: {str(e)}", 500

    return render_template("index.html")

# Ruta para servir los archivos descargados
@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DEFAULT_DOWNLOAD_PATH, filename)

if __name__ == "__main__":
    app.run(debug=True)

