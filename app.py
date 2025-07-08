import os
from flask import Flask, request, send_file, render_template
import subprocess

app = Flask(__name__, static_folder="static", template_folder="templates")
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    face_image = request.files['faceImage']
    text = request.form['text']

    input_path = os.path.join(UPLOAD_FOLDER, face_image.filename)
    face_image.save(input_path)

    output_video_path = os.path.join(OUTPUT_FOLDER, "result.mp4")

    command = [
        "python", "inference.py",
        "--driven_text", text,
        "--source_image", input_path,
        "--result_dir", OUTPUT_FOLDER
    ]

    try:
        subprocess.run(command, check=True)
        return send_file(output_video_path, mimetype="video/mp4")
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to generate video.", "details": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)