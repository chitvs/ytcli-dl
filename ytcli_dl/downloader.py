"""
ytcli-dl -- A minimal command-line YouTube downloader.

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
import sys
from typing import List, Dict, Any, Optional
import yt_dlp
import click
from .config import DEFAULT_YDL_OPTS, QUALITY_OPTIONS, AUDIO_FORMAT
from .utils import (
    validate_url, 
    validate_playlist_url, 
    create_output_dir, 
    format_bytes,
    format_duration,
)

class YouTubeDownloader:
    
    def __init__(self, output_dir, quality='best', audio_only=False, format_code=None):
        self.output_dir = create_output_dir(output_dir)
        self.quality = quality
        self.audio_only = audio_only
        self.format_code = format_code
        self.ydl_opts = self._build_ydl_opts()
    
    def _build_ydl_opts(self) -> Dict[str, Any]:
        opts = DEFAULT_YDL_OPTS.copy()

        opts['outtmpl'] = os.path.join(self.output_dir, '%(title)s.%(ext)s')
        opts['overwrites'] = True
        opts['quiet'] = True
        opts['no_warnings'] = True
        opts['progress_hooks'] = [self._minimal_progress_hook]

        if self.format_code:
            opts['format'] = self.format_code
            if '+' in self.format_code:
                opts['merge_output_format'] = 'mp4'
        elif self.audio_only:
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': '192',
            }]
        else:
            video_height = self.quality.replace('p', '') if 'p' in self.quality else ''
            if video_height.isdigit():
                opts['format'] = (
                    f"bestvideo[ext=mp4][height<={video_height}]+"
                    f"bestaudio[ext=m4a]/best[height<={video_height}]"
                )
            else:
                opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'

            opts['merge_output_format'] = 'mp4'
            opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]

        return opts
    
    def _minimal_progress_hook(self, d):
        if d['status'] == 'finished':
            filename = os.path.basename(d.get('filename', 'file'))
            click.echo(f" - {filename}")
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            click.echo(f"Error: Failed to get video info - {str(e)}")
            return None
    
    def download_single_video(self, url: str) -> bool:
        if not validate_url(url):
            click.echo(f"Error: Invalid YouTube URL: {url}")
            return False
        
        try:
            info = self.get_video_info(url)
            if not info:
                return False
            
            title = info.get('title', 'Unknown Title')
            duration = format_duration(info.get('duration'))
            uploader = info.get('uploader', 'Unknown Uploader')
            
            click.echo(f"Title: {title}")
            click.echo(f"Uploader: {uploader}")
            click.echo(f"Duration: {duration}")
            
            if self.audio_only:
                click.echo("Downloading audio only...")
            elif self.format_code:
                click.echo(f"Downloading with custom format: {self.format_code}...")
            else:
                click.echo(f"Downloading in {self.quality} quality...")
            
            downloaded_files = []
            
            def enhanced_progress_hook(d):
                if d['status'] == 'finished':
                    filename = os.path.basename(d.get('filename', 'file'))
                    downloaded_files.append(filename)
                    click.echo(f" - {filename}")
            
            opts_with_hooks = self.ydl_opts.copy()
            opts_with_hooks['progress_hooks'] = [enhanced_progress_hook]
            
            with yt_dlp.YoutubeDL(opts_with_hooks) as ydl:
                try:
                    ydl.download([url])
                except SystemExit as e:
                    if e.code != 0:
                        return False
            
            if not downloaded_files:
                click.echo("Error: No files were downloaded")
                return False
            
            return True
            
        except yt_dlp.DownloadError as e:
            click.echo(f"Error: Download failed - {str(e)}")
            return False
        except Exception as e:
            click.echo(f"Error: Unexpected error during download - {str(e)}")
            return False
        
    def download_playlist(self, url: str) -> bool:
        if not validate_playlist_url(url) and not validate_url(url):
            click.echo(f"Error: Invalid playlist URL: {url}")
            return False
        
        try:
            click.echo("Getting playlist information...")
            info = self.get_video_info(url)
            if not info:
                return False
            
            if 'entries' in info:
                playlist_title = info.get('title', 'Unknown Playlist')
                video_count = len([entry for entry in info['entries'] if entry])
                
                click.echo(f"Playlist: {playlist_title}")
                click.echo(f"Videos: {video_count}")
                
                if not click.confirm(f"Download all {video_count} videos?"):
                    click.echo("Download cancelled.")
                    return False
                
                playlist_opts = self.ydl_opts.copy()
                playlist_opts['outtmpl'] = os.path.join(
                    self.output_dir, 
                    '%(playlist)s',
                    '%(playlist_index)s - %(title)s.%(ext)s'
                )
                
                if self.audio_only:
                    click.echo("Downloading playlist audio only...")
                else:
                    click.echo(f"Downloading playlist in {self.quality} quality...")
                
                with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                    ydl.download([url])
                
                click.secho("Playlist download completed!", fg='green')
                return True
            else:
                return self.download_single_video(url)
                
        except yt_dlp.DownloadError as e:
            click.echo(f"Error: Playlist download failed - {str(e)}")
            return False
        except Exception as e:
            click.echo(f"Error: Unexpected error during playlist download - {str(e)}")
            return False
    
    def download_multiple_urls(self, urls: List[str]) -> Dict[str, bool]:
        results = {}
        total_urls = len(urls)
        
        click.echo(f"Starting batch download of {total_urls} URLs...")
        
        for i, url in enumerate(urls, 1):
            click.echo(f"[{i}/{total_urls}] Processing: {url}")
            
            try:
                if validate_playlist_url(url):
                    success = self.download_playlist(url)
                else:
                    success = self.download_single_video(url)
                
                results[url] = success
                
            except KeyboardInterrupt:
                click.echo("Error: Download interrupted by user.")
                results[url] = False
                break
            except Exception as e:
                click.echo(f"Error: Failed to process {url} - {str(e)}")
                results[url] = False
        
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        click.echo("=" * 50)
        click.echo("Batch Download Summary:")
        click.echo(f"Total URLs: {len(results)}")
        
        click.secho(f"Successful: {successful}", fg='green')
        if failed > 0:
            click.echo(f"Failed: {failed}")
        click.echo("=" * 50)
        
        return results
    
    def list_formats(self, url: str) -> bool:
        if not validate_url(url):
            click.echo(f"Error: Invalid YouTube URL: {url}")
            return False
        
        try:
            opts = {'listformats': True, 'quiet': True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            click.echo(f"Error: Failed to list formats - {str(e)}")
            return False
        
def list_video_formats(url: str) -> None:
    try:
        with yt_dlp.YoutubeDL({'listformats': True, 'quiet': False}) as ydl:
            ydl.download([url])
    except Exception as e:
        click.echo(f"Error: Failed to list formats - {str(e)}")
