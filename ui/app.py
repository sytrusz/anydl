import flet as ft
from core.manager import DownloadManager
import threading
import time
import os
import asyncio
import re
from pathlib import Path

async def main_app(page: ft.Page):
    page.title = "anydl"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_50

    manager = DownloadManager()

    # Determine default download path
    default_download_path = os.path.join(os.path.expanduser("~"), "Documents", "anydl")

    # Setup FilePicker
    get_directory_dialog = ft.FilePicker()

    TOOLS = {
        "spotdl": {
            "name": "Spotify Downloader",
            "desc": "Spotify track/playlist to MP3",
            "hint": "Paste Spotify URL or search",
            "color": "#21c25e",
            "icon": ft.Icons.LIBRARY_MUSIC
        },
        "yt-dlp": {
            "name": "YouTube Downloader",
            "desc": "YouTube to Video/Audio",
            "hint": "Paste YouTube URL or search",
            "color": ft.Colors.RED_600,
            "icon": ft.Icons.VIDEO_LIBRARY
        },
        "scdl": {
            "name": "SoundCloud Downloader",
            "desc": "SoundCloud to MP3",
            "hint": "Paste SoundCloud URL (Track or Playlist)",
            "color": ft.Colors.ORANGE_700,
            "icon": ft.Icons.CLOUD_DOWNLOAD
        },
        "tiktok": {
            "name": "TikTok Downloader",
            "desc": "TikTok Video to MP4",
            "hint": "Paste TikTok URL",
            "color": ft.Colors.CYAN_400,
            "icon": ft.Icons.MUSIC_VIDEO
        },
        "facebook": {
            "name": "Facebook Downloader",
            "desc": "Facebook Reels to Video/Audio",
            "hint": "Paste Facebook Video URL",
            "color": ft.Colors.BLUE_800,
            "icon": ft.Icons.FACEBOOK
        },
        "instagram": {
            "name": "Instagram Reels",
            "desc": "Instagram Reels to Video/Audio ",
            "hint": "Paste Instagram URL",
            "color": ft.Colors.PINK_500,
            "icon": ft.Icons.CAMERA_ALT
        },
        "twitter": {
            "name": "X (Twitter)",
            "desc": "X to Video/Audio",
            "hint": "Paste X/Twitter URL",
            "color": ft.Colors.BLACK,
            "icon": ft.Icons.WEB
        }
    }
    
    current_tool_id = "yt-dlp" # Default placeholder

    # -------------------------------------------------------------
    # Shared State & Elements
    # -------------------------------------------------------------
    tool_title = ft.Text("", size=36, color=ft.Colors.BLACK, weight=ft.FontWeight.W_400)
    tool_desc = ft.Text("", size=16, color=ft.Colors.GREY_700)
    
    url_input = ft.TextField(
        border=ft.InputBorder.NONE,
        expand=True,
        color=ft.Colors.BLACK,
        cursor_color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
        content_padding=ft.Padding.only(left=15, right=15, top=10, bottom=10)
    )
    
    search_border = ft.Container(
        content=url_input,
        border_radius=ft.BorderRadius.only(top_left=4, bottom_left=4),
        bgcolor=ft.Colors.WHITE,
        expand=True,
        height=50,
        padding=0
    )
    
    download_btn_container = ft.Container(
        content=ft.Row([
            ft.Text("Download", color=ft.Colors.WHITE, weight=ft.FontWeight.W_500, size=16),
            ft.Icon(ft.Icons.DOWNLOAD, color=ft.Colors.WHITE, size=20)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        padding=ft.Padding.only(left=20, right=20),
        border_radius=ft.BorderRadius.only(top_right=4, bottom_right=4),
        height=50,
        ink=True
    )

    # Directory Selection UI
    selected_dir_text = ft.Text(f"Save to: {default_download_path}", size=12, color=ft.Colors.GREY_600)
    current_selected_dir = default_download_path

    async def open_dir_picker(e):
        nonlocal current_selected_dir
        selected_path = await get_directory_dialog.get_directory_path()
        if selected_path:
            current_selected_dir = selected_path
            selected_dir_text.value = f"Save to: {current_selected_dir}"
            page.update()

    dir_selector = ft.Row([
        ft.IconButton(ft.Icons.FOLDER_OPEN, icon_color=ft.Colors.GREY_600, tooltip="Change download folder", on_click=open_dir_picker),
        selected_dir_text
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Format Selector (yt-dlp only)
    format_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("video", text="Best Video (MP4)"),
            ft.dropdown.Option("audio", text="Audio Only (MP3)"),
        ],
        value="video",
        width=180,
        height=40,
        content_padding=ft.Padding.only(left=10, right=10),
        text_size=12,
        visible=False
    )

    options_row = ft.Row([dir_selector, format_dropdown], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    log_area = ft.ListView(expand=True, spacing=5, auto_scroll=True)
    
    # Progress Bar (hidden by default, starts indeterminate)
    progress_bar = ft.ProgressBar(width=400, color=ft.Colors.BLUE_400, bgcolor=ft.Colors.GREY_200, value=None)
    progress_text = ft.Text("0%", size=12, color=ft.Colors.GREY_600)
    progress_container = ft.Container(
        content=ft.Row([progress_bar, progress_text], alignment=ft.MainAxisAlignment.CENTER), 
        margin=ft.Margin.only(top=10, bottom=10), 
        visible=False
    )

    log_container = ft.Container(
        content=log_area,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.GREY_200),
        border_radius=ft.BorderRadius.all(4),
        padding=10,
        margin=ft.Margin.only(top=10),
        height=200,
        visible=False
    )

    # -------------------------------------------------------------
    # Logic & Background Processes
    # -------------------------------------------------------------
    # State for tracking playlist progress
    playlist_state = {"total": 0, "downloaded": 0}

    def log_message(msg_type, msg, batch_update=False):
        color = ft.Colors.BLACK
        if msg_type == "ERROR":
            color = ft.Colors.RED_400
        elif msg_type == "STATUS":
            color = ft.Colors.BLUE_400
        elif msg_type == "STDERR":
            color = ft.Colors.ORANGE_400
            
        log_area.controls.append(ft.Text(f"[{msg_type}] {msg}", color=color, font_family="monospace", size=12))
        
        # Parse percentage from log output
        if msg_type in ["STDOUT", "STDERR"]:
            # 1. Look for explicit percentages (e.g. yt-dlp)
            match = re.search(r'(\d{1,3}(?:\.\d+)?)%', msg)
            if match:
                try:
                    pct = float(match.group(1))
                    if 0 <= pct <= 100:
                        progress_bar.value = pct / 100.0
                        progress_text.value = f"{pct:.1f}%"
                except ValueError:
                    pass
            
            # 2. Look for spotdl playlist total
            total_match = re.search(r'Found (\d+) songs', msg)
            if total_match:
                playlist_state["total"] = int(total_match.group(1))
                playlist_state["downloaded"] = 0
                progress_bar.value = 0.0
                progress_text.value = "0%"

            # 3. Look for spotdl downloaded song
            if "Downloaded \"" in msg and playlist_state["total"] > 0:
                playlist_state["downloaded"] += 1
                pct = (playlist_state["downloaded"] / playlist_state["total"]) * 100
                progress_bar.value = pct / 100.0
                progress_text.value = f"{pct:.1f}%"

        # Hide loading spinner if process finished
        if "Process finished" in msg or msg_type == "ERROR":
            progress_bar.visible = False
            progress_container.visible = False
            progress_bar.value = None
            progress_text.value = "0%"
            download_btn_container.disabled = False
            url_input.disabled = False
            format_dropdown.disabled = False

        log_container.visible = True
        if not batch_update:
            page.update()

    def start_download(e):
        url = url_input.value
        if not url:
            log_message("ERROR", "URL cannot be empty")
            return
            
        # Ensure target directory exists
        target_dir = current_selected_dir
        if not target_dir:
            target_dir = default_download_path
            
        try:
            Path(target_dir).mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            log_message("ERROR", f"Failed to create directory: {ex}")
            return

        # Show loading state and reset progress
        playlist_state["total"] = 0
        playlist_state["downloaded"] = 0
        progress_bar.value = None
        progress_text.value = "0%"
        progress_bar.visible = True
        progress_container.visible = True
        download_btn_container.disabled = True
        url_input.disabled = True
        format_dropdown.disabled = True
        page.update()

        # Map UI tool IDs to actual CLI engines
        engine = current_tool_id
        if current_tool_id in ["tiktok", "facebook", "instagram", "twitter"]:
            engine = "yt-dlp"

        command = [engine]
        if engine == "yt-dlp":
            if format_dropdown.value == "audio":
                command.extend(["-x", "--audio-format", "mp3"])
            elif format_dropdown.value == "video":
                command.extend(["--merge-output-format", "mp4"])
        elif engine == "scdl":
            command.extend(["-l"]) # scdl requires -l for the URL
            
        command.append(url)

        manager.start_download(command, cwd=target_dir)
        url_input.value = ""
        page.update()

    download_btn_container.on_click = start_download

    async def poll_queue(e=None):
        while True:
            messages = manager.get_messages()
            if messages:
                for msg_type, msg in messages:
                    log_message(msg_type, msg, batch_update=True)
                page.update()
            await asyncio.sleep(0.1)

    page.run_task(poll_queue)

    # -------------------------------------------------------------
    # Navigation Methods
    # -------------------------------------------------------------
    def show_home():
        tool_view.visible = False
        home_view.visible = True
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = ft.Colors.BLACK
            theme_btn.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = ft.Colors.GREY_50
            theme_btn.icon = ft.Icons.DARK_MODE
        page.update()

    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Toggle Theme",
        on_click=toggle_theme
    )

    def show_tool(tool_id):
        nonlocal current_tool_id
        current_tool_id = tool_id
        t = TOOLS[tool_id]
        
        tool_title.value = t["name"]
        tool_desc.value = t["desc"]
        url_input.hint_text = t["hint"]
        search_border.border = ft.Border.all(2, t["color"])
        download_btn_container.bgcolor = t["color"]
        
        # Tools using yt-dlp engine support format selection
        if tool_id in ["yt-dlp", "tiktok", "facebook", "instagram", "twitter"]:
            format_dropdown.visible = True
            format_dropdown.disabled = False
        else:
            format_dropdown.visible = False

        log_area.controls.clear()
        log_container.visible = False

        home_view.visible = False
        tool_view.visible = True
        page.update()

    # -------------------------------------------------------------
    # Tool View
    # -------------------------------------------------------------
    tool_view = ft.Container(
        visible=False,
        expand=True,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.TextButton(
                        "Back to Home", 
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: show_home(),
                        style=ft.ButtonStyle(color=ft.Colors.GREY_700)
                    ),
                    alignment=ft.Alignment(-1, -1),
                    padding=ft.Padding.only(left=20, top=20)
                ),
                ft.Container(height=20),
                tool_title,
                tool_desc,
                ft.Container(height=30),
                ft.Row(
                    [
                        search_border,
                        download_btn_container
                    ],
                    spacing=0,
                    width=700
                ),
                progress_container,
                ft.Container(height=10),
                options_row,
                log_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # -------------------------------------------------------------
    # Home View
    # -------------------------------------------------------------
    cards = []
    for t_id, t_data in TOOLS.items():
        card = ft.Container(
            content=ft.Column([
                ft.Icon(t_data["icon"], size=48, color=t_data["color"]),
                ft.Container(height=10),
                ft.Text(t_data["name"], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Text(t_data["desc"], size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
            width=280,
            height=220,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.BorderRadius.all(8),
            border=ft.Border.all(1, ft.Colors.GREY_200),
            ink=True,
            on_click=lambda e, id=t_id: show_tool(id)
        )
        cards.append(card)

    home_view = ft.Container(
        visible=True,
        expand=True,
        content=ft.Column([
            ft.Container(height=40),
            ft.Text("What would you like to download?", size=32, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK),
            ft.Container(height=40),
            ft.GridView(
                expand=True,
                runs_count=3,
                max_extent=300,
                child_aspect_ratio=1.3,
                spacing=20,
                run_spacing=20,
                controls=cards,
                padding=ft.Padding.only(left=40, right=40)
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # -------------------------------------------------------------
    # Header, Footer & Assembly
    # -------------------------------------------------------------
    header = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Text(spans=[
                    ft.TextSpan("ANY", style=ft.TextStyle(color="#21c25e", weight=ft.FontWeight.BOLD, size=22)),
                    ft.TextSpan("DL", style=ft.TextStyle(color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, size=22)),
                ])
            ], on_click=lambda _: show_home()),
            theme_btn
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.only(left=30, right=30, top=10, bottom=10),
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_200))
    )

    footer = ft.Container(
        content=ft.Row([
            ft.Text("Built with ❤️ by ", size=12, color=ft.Colors.GREY_600),
            ft.TextButton(
                "sytrusz/anydl",
                url="https://github.com/sytrusz/anydl",
                style=ft.ButtonStyle(color="#21c25e", padding=ft.Padding.all(0))
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.Padding.only(bottom=20)
    )

    page.add(
        ft.Column([
            header,
            ft.Container(content=ft.Column([home_view, tool_view], expand=True), expand=True),
            footer
        ], expand=True, spacing=0)
    )

