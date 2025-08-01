# ytcli-dl, a minimal command-line YouTube downloader

**ytcli-dl** is a simple yet powerful tool to download YouTube videos and playlists directly from the command line. Using yt-dlp, it supports multiple formats and resolutions, audio-only downloads, and custom output options. Intended for personal use.

## Features

- Download videos in various qualities
- Extract audio in MP3 format
- Playlist support
- Download multiple URLs from a file
- List available formats before downloading
- Option to specify exact format codes for maximum control

## Installation

### Clone the repository

```bash
git clone https://github.com/chitvs/ytcli-dl.git
cd ytcli-dl
```

### Using a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### System-wide installation

```bash
pip install -e .
```

> [!NOTE]
> Installing system-wide may require `sudo` on some systems and could potentially conflict with other Python packages. Using a virtual environment is recommended to avoid dependency conflicts.

## Quick start

### Basic usage

Download a video in the best available quality:
```bash
ytcli-dl "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download audio only:
```bash
ytcli-dl -a "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download in a specific resolution:
```bash
ytcli-dl -q 720p "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download entire playlist:
```bash
ytcli-dl -p "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Download from file with multiple URLs:
```bash
ytcli-dl -f urls.txt
```

List available formats for a video:
```bash
ytcli-dl -l "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download with a specific format code:
```bash
ytcli-dl --format-code "137+140" "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Examples

Download a music video in 720p quality:
```bash
ytcli-dl -q 720p "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Download to a custom directory:
```bash
ytcli-dl -o ~/Videos/YouTube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Check available formats before downloading:
```bash
ytcli-dl -l "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# Then use a specific format
ytcli-dl --format-code "248+140" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Options

```
ytcli-dl [OPTIONS] [URL]

Arguments:
  URL  YouTube video or playlist URL

Options:
  -q, --quality [best|144p|240p|360p|480p|720p|1080p|1440p|2160p]
                                 Video quality to download (default: best)
  -a, --audio-only               Download audio only (MP3 format)
  -o, --output PATH              Output directory for downloads (default: ~/Downloads/ytcli-downloads)
  -p, --playlist                 Download entire playlist
  -f, --file PATH                Download URLs from a text file (one per line)
  -l, --list-formats             List available formats for the video without downloading
  --format-code TEXT             Download specific format
  -v, --version                  Show version and exit
  -h, --help                     Show this help message and exit
```

## Requirements

- Python
- yt-dlp
- click
- tqdm

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file for details.

## Legal disclaimer

Please read the following carefully before using this software:

1. **Usage Responsibility:** This tool is intended for personal and educational use only, in accordance with applicable copyright laws and YouTube's Terms of Service. Users are solely responsible for ensuring their use of this software complies with all relevant laws and regulations in their jurisdiction.

2. **Copyright:** Users are responsible for respecting copyright. Do not download copyrighted material without permission from the copyright holder. This software does not endorse or condone copyright infringement.

3. **YouTube's Terms of Service:** YouTube's Terms of Service generally prohibit the unauthorized downloading of content. By using this software, you acknowledge and agree that you are solely responsible for any consequences arising from your non-compliance with YouTube's Terms of Service.
