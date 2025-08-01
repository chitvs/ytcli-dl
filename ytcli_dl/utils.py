"""
ytcli-dl - A minimal command-line YouTube downloader.

MIT License

Copyright (c) 2025 Alessandro Chitarrini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
from pathlib import Path
from typing import List, Optional
import click

def validate_url(url: str) -> bool:
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return bool(youtube_regex.match(url))

def validate_playlist_url(url: str) -> bool:
    playlist_regex = re.compile(
        r'(https?://)?(www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)'
    )
    return bool(playlist_regex.match(url))

def create_output_dir(output_path: str) -> str:
    abs_path = os.path.abspath(os.path.expanduser(output_path))
    Path(abs_path).mkdir(parents=True, exist_ok=True)
    return abs_path

def read_urls_from_file(file_path: str) -> List[str]:
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if validate_url(line) or validate_playlist_url(line):
                        urls.append(line)
                    else:
                        click.echo(f"Warning: Invalid URL on line {line_num} - {line}")
    except FileNotFoundError:
        click.echo(f"Error: File '{file_path}' not found")
        return []
    except IOError as e:
        click.echo(f"Error: Failed to read file '{file_path}' - {e}")
        return []
    
    return urls

def format_bytes(bytes_size: Optional[int]) -> str:
    if bytes_size is None:
        return "Unknown size"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def format_duration(seconds: Optional[float]) -> str:
    if seconds is None:
        return "Unknown duration"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def sanitize_filename(filename: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    filename = filename.strip('. ')
    
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename