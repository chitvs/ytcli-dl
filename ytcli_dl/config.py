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
from pathlib import Path

DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Downloads" / "ytcli-downloads")

QUALITY_OPTIONS = {
    'best': 'best[ext=mp4]/best',
    '144p': 'best[height<=144][ext=mp4]/best[height<=144]',
    '240p': 'best[height<=240][ext=mp4]/best[height<=240]',
    '360p': 'best[height<=360][ext=mp4]/best[height<=360]',
    '480p': 'best[height<=480][ext=mp4]/best[height<=480]',
    '720p': 'best[height<=720][ext=mp4]/best[height<=720]',
    '1080p': 'best[height<=1080][ext=mp4]/best[height<=1080]',
    '1440p': 'best[height<=1440][ext=mp4]/best[height<=1440]',
    '2160p': 'best[height<=2160][ext=mp4]/best[height<=2160]',
}

AUDIO_FORMAT = 'mp3'

DEFAULT_YDL_OPTS = {
    'format': QUALITY_OPTIONS['best'],
    'outtmpl': os.path.join(DEFAULT_DOWNLOAD_DIR, '%(title)s.%(ext)s'),
    'ignoreerrors': True,
    'quiet': True,  
    'no_warnings': True,  
    'extractaudio': False,
    'audioformat': AUDIO_FORMAT,
    'embedsubs': True,
    'writesubtitles': False,
    'writeautomaticsub': False,
}