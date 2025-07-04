from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
import subprocess
import uuid
import time
from pathlib import Path

app = FastAPI()

DOWNLOAD_DIR = Path.home() / ".video_downloader"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_AGE = 30 * 60  # 30 minutes

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

HTML_FORM = f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Video Downloader</title>
{TAILWIND_CDN}
</head>
<body class="bg-gray-50 flex justify-center pt-10 min-h-screen">
<div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md text-center">
  <h1 class="text-2xl font-bold mb-4 text-gray-800">Download Your Video</h1>
  <p class="text-gray-600 mb-6">Paste the video URL and click download</p>
  <form method="post" class="space-y-4">
    <div class="flex space-x-2">
      <input id="url-input" type="text" name="url" placeholder="https://…" class="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
      <button type="button" onclick="pasteClipboard()" class="px-3 bg-gray-200 rounded-md hover:bg-gray-300">📋</button>
    </div>
    <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600">Download</button>
  </form>
  <!-- MESSAGE -->
</div>

<script>
async function pasteClipboard() {{
    const input = document.getElementById('url-input');
    input.value = '';
    try {{
        const text = await navigator.clipboard.readText();
        input.value = text;
    }} catch(err) {{
        alert('Unable to access clipboard: ' + err);
    }}
}}
</script>

</body>
</html>
"""

def cleanup_old_files():
    now = time.time()
    for file in DOWNLOAD_DIR.iterdir():
        if file.is_file() and now - file.stat().st_mtime > MAX_FILE_AGE:
            try:
                file.unlink()
            except Exception as e:
                print(f"Error deleting {file}: {e}")

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return HTML_FORM.replace("<!-- MESSAGE -->", "")

@app.post("/", response_class=HTMLResponse)
async def download_video(url: str = Form(...)):
    if not url.strip():
        msg = '<p class="text-red-500 mt-4">Please enter a valid URL.</p>'
        return HTML_FORM.replace("<!-- MESSAGE -->", msg)

    cleanup_old_files()

    video_id = str(uuid.uuid4())
    output_template = str(DOWNLOAD_DIR / f"{video_id}.%(ext)s")

    # Step 1: download best available
    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "-o", output_template,
        url
    ]

    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        msg = '<p class="text-red-500 mt-4">Error downloading video. Check the URL.</p>'
        return HTML_FORM.replace("<!-- MESSAGE -->", msg)

    # Step 2: find downloaded file
    downloaded_file = next(DOWNLOAD_DIR.glob(f"{video_id}.*"), None)
    if not downloaded_file:
        msg = '<p class="text-red-500 mt-4">Downloaded file not found.</p>'
        return HTML_FORM.replace("<!-- MESSAGE -->", msg)

    # Step 3: convert to .mp4 if necessary
    if downloaded_file.suffix != ".mp4":
        mp4_file = downloaded_file.with_suffix(".mp4")
        cmd = [
            "ffmpeg", "-y", "-i", str(downloaded_file),
            "-c:v", "libx264", "-c:a", "aac",
            "-strict", "experimental", str(mp4_file)
        ]
        try:
            subprocess.check_call(cmd)
            downloaded_file.unlink()  # remove original
            downloaded_file = mp4_file
        except subprocess.CalledProcessError:
            msg = '<p class="text-red-500 mt-4">Error converting video to MP4.</p>'
            return HTML_FORM.replace("<!-- MESSAGE -->", msg)

    # Step 4: return file
    return FileResponse(path=downloaded_file, filename=downloaded_file.name, media_type="application/octet-stream")
