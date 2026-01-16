from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json.get("url")
    ydl_opts = {"quiet": True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        seen = set()
        for f in info.get("formats", []):
            h = f.get("height")
            if h and h not in seen:
                formats.append(h)
                seen.add(h)

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": sorted(formats, reverse=True)
        })
    except:
        return jsonify({"error": "Invalid URL"}), 400

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data["url"]
    mode = data["mode"]
    quality = data.get("quality")
    audio_format = data.get("audio_format", "mp3")

    if mode == "audio":
        opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "192"
            }],
        }
    else:
        opts = {
            "format": f"bestvideo[height<={quality}]+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    return jsonify({"status": "completed"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)