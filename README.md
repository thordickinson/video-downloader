# 📹 Video Downloader (FastAPI + yt-dlp)

A lightweight web application to download videos from YouTube, Instagram Reels, TikTok, and other platforms supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp).
It provides a clean, Google-like web interface built with FastAPI and served via Uvicorn.

Videos are stored temporarily inside the container and automatically cleaned up after \~30 minutes.

---

## 🚀 Features

✅ Download the best available video + audio
✅ Works with YouTube, Instagram, TikTok, and more
✅ Clean, mobile-friendly interface with TailwindCSS
✅ Clipboard button to quickly paste your URL
✅ Auto-removes old files after 30 minutes
✅ Runs in a container, no installation required on host

---

## 📦 Run with Docker

### 1️⃣ Build the Docker image

```bash
docker build -t video-downloader .
```

### 2️⃣ Run the container

```bash
docker run -d --name video-downloader -p 5000:5000 video-downloader
```

### 3️⃣ Open in your browser

```
http://localhost:5000
```

or, from another machine on the network:

```
http://<YOUR_SERVER_IP>:5000
```

---

## 🧽 Storage & Cleanup

Videos are stored in `/root/.video_downloader` inside the container and deleted automatically after \~30 minutes.
No persistent storage is required. Destroying the container removes everything.

---

## 🔄 Updating yt-dlp

Since platforms change frequently, it’s recommended to rebuild the image periodically to get the latest `yt-dlp`:

```bash
docker build -t video-downloader .
```

---

## 🔗 Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/) — modern async web framework
* [Uvicorn](https://www.uvicorn.org/) — lightning-fast ASGI server
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) — video downloader backend
* [TailwindCSS](https://tailwindcss.com/) — clean and simple styling (via CDN)

---

## 📝 Notes

* Requires Docker.
* Clipboard API may require HTTPS in some browsers for full functionality.
* Please respect the terms of service of each platform you download from.

