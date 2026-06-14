<div align="center">
  <h1>Any Downloader Tool</h1>
  <p>A unified, clean, and modern desktop application for downloading audio and video.</p>

  <!-- TODO: Add a screenshot of the app here -->
  <!-- <img src="screenshots/homepage.png" alt="App Homepage" width="600"> -->
</div>

## 📖 Overview

**Any Downloader Tool** is an open-source Python desktop application built with [Flet](https://flet.dev). It serves as a user-friendly graphical interface (GUI) for two of the most powerful command-line downloaders available:
- [**yt-dlp**](https://github.com/yt-dlp/yt-dlp): For downloading high-quality YouTube videos and converting them to audio.
- [**spotDL**](https://github.com/spotDL/spotify-downloader): For downloading Spotify playlists and tracks directly to MP3.

---

## Features

- 🎥 **YouTube Video & Audio**: Download the "Best Video" (automatically merged to MP4) or extract "Audio Only" (MP3).
- 🎵 **Spotify Playlists**: Paste a Spotify playlist or track link, and the app will download all songs as MP3s with full metadata and album art.
- 📂 **Custom Save Locations**: Easily choose where your files go using your operating system's native folder picker.

---

## Getting Started

### Prerequisites

Before using the app, you must have the following installed on your system:
1. **Python 3.8 or newer**: [Download Python here](https://www.python.org/downloads/).
2. **FFmpeg**: This is required by the underlying tools to convert video and audio formats.
   - **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via winget: `winget install ffmpeg`
   - **macOS**: Install via Homebrew: `brew install ffmpeg`
   - **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg` or `sudo dnf install ffmpeg`)

### Installation

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/yourusername/any-downloader-tool.git
   cd any-downloader-tool
   ```

2. **Set up a Python Virtual Environment:**
   This keeps the app's dependencies isolated from your system.
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   - **Linux/macOS:** `source .venv/bin/activate`
   - **Windows:** `.venv\Scripts\activate`

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **(Linux Only) Install Desktop Shortcut:**
   If you want the app to appear in your system's application launcher, run the provided script:
   ```bash
   ./install_desktop.sh
   ```

---

## How to Use

1. **Launch the App:**
   Make sure your virtual environment is activated, then run:
   ```bash
   python3 main.py
   ```
2. **Select your tool:** Click either the Spotify Downloader or the YouTube Downloader on the home screen.
3. **Choose a folder:** Click the folder icon at the bottom to choose where the downloaded files should be saved. (Defaults to `Documents/AnyDownloader`).
4. **Select Format (YouTube Only):** If using the YouTube tool, choose between "Best Video (MP4)" or "Audio Only (MP3)" from the dropdown menu.
5. **Download:** Paste your URL into the search bar and click the **Download** button. The progress bar and terminal logs will show you what is happening in real-time!

---

## Troubleshooting

- **"Failed to merge formats" or "Audio conversion failed"**
  - **Fix:** You are missing `FFmpeg`. Please see the Prerequisites section and ensure FFmpeg is installed and added to your system's PATH.
- **The UI is blank or crashing on Linux**
  - **Fix:** Flet relies on a few system libraries. Make sure your system is up to date. You may need to install `zenity` (for the folder picker).

---

## Credits & Acknowledgements

This project would not be possible without the incredible work of the open-source community. Massive thanks to:
- [**Flet**](https://flet.dev/): The UI framework that makes building Python desktop apps a breeze.
- [**yt-dlp**](https://github.com/yt-dlp/yt-dlp): The premier, feature-rich command-line audio/video downloader.
- [**spotDL**](https://github.com/spotDL/spotify-downloader): The fastest and most accurate Spotify downloader available.