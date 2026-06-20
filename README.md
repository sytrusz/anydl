<div align="center">
  <h1>anydl</h1>
  <p>A unified, clean, and modern desktop application for downloading audio and video.</p>

  <img src="screenshots/home.png" alt="App Homepage" width="600">
</div>

## Overview

**anydl** is an open-source Python desktop application built with [Flet](https://flet.dev). It serves as a user-friendly graphical interface (GUI) that orchestrates several industry-standard command-line download engines.

---

## 📌 Quick Start (Installation & Running)

Running **anydl** as simple as possible. It runs locally as a fast, responsive web application directly in your browser.

### 1. Prerequisites
**🪟 For Windows Users:**
You don't need to install anything! The `start_windows.bat` script will automatically download and set up a portable version of Python and FFmpeg for you if they are missing from your system.

**🍎 macOS / 🐧 Linux Users:**
Before using the app, you must install the following on your system:
- **Python 3.8 or newer**: Pre-installed on most Linux distros. Mac users can [download it here](https://www.python.org/downloads/).
- **FFmpeg**: Required to convert video and audio formats.
  - **macOS**: Install via Homebrew: `brew install ffmpeg`
  - **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg` or `sudo dnf install ffmpeg`)

### 2. Download and Run
1. **Download the Repository:**
   Click the green **"Code"** button at the top and select **"Download ZIP"**, then extract it. *(Or clone via terminal: `git clone https://github.com/sytrusz/anydl.git`)*

2. **Launch the Application:**
   Open the extracted folder and run the startup script for your operating system:
   - 🪟 **Windows:** Double-click the `start_windows.bat` file.
   - 🍎 **macOS / 🐧 Linux:** Run the `start_linux.sh` script in your terminal (`./start_linux.sh`).

*That's it! The script will automatically set everything up and launch the app in your default web browser.*

---

## How to Use

1. **Select your tool:** Click one of the cards (Spotify, YouTube, TikTok, etc.) on the home screen.
2. **Choose a folder:** Click the folder icon at the bottom to set your download directory.
3. **Download:** Paste your URL and click **Download**.

---

## Features

- 🎥 **Video Downloads**: Download the "Best Video" (automatically merged to MP4) from YouTube, TikTok, Facebook, Instagram, and X.
- 🎵 **Music Downloads**: High-quality MP3 downloads from Spotify and SoundCloud with full metadata.
- 🚀 **Spotify Rate-Limit Bypassing**: Add your own Spotify Developer API keys via the Settings menu to bypass annoying rate limits on user-created playlists.
- 📁 **Smart Playlist Folders**: Playlists are automatically organized into neatly named subfolders (`anydl@sytrus - [Playlist Name]`).
- 📊 **Progress & Stats**: Watch your downloads complete with a live progress bar, and get detailed summaries of successful/missing songs upon completion.
- 📂 **Custom Save Locations**: Easily choose where your files go using your operating system's native folder picker.
- 🎨 **Modern UI**: A clean, distraction-free interface with Dark/Light mode support.

---

## Powered By

This project is built upon the incredible work of the following repositories:

- [**yt-dlp**](https://github.com/yt-dlp/yt-dlp): The engine used for YouTube, TikTok, Facebook, X (Twitter), and Instagram downloads.
- [**spotDL**](https://github.com/spotDL/spotify-downloader): The engine used for Spotify track and playlist downloads.
- [**scdl**](https://github.com/flyingrub/scdl): The engine used for SoundCloud audio downloads.

---

## Credits & Acknowledgements

Massive thanks to the open-source community:
- [**Flet**](https://flet.dev/): The UI framework.
- [**yt-dlp**](https://github.com/yt-dlp/yt-dlp): The video engine.
- [**spotDL**](https://github.com/spotDL/spotify-downloader): The Spotify engine.
- [**scdl**](https://github.com/flyingrub/scdl): The SoundCloud engine.

## License
This project is open-source. Feel free to fork, modify, and distribute it!
