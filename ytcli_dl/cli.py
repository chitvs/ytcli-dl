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

import sys
from pathlib import Path
import click

from . import __version__
from .config import DEFAULT_DOWNLOAD_DIR, QUALITY_OPTIONS
from .downloader import YouTubeDownloader, list_video_formats
from .utils import read_urls_from_file, validate_url, validate_playlist_url

class CustomChoice(click.Choice):
    def convert(self, value, param, ctx):
        try:
            return super().convert(value, param, ctx)
        except click.BadParameter as e:
            click.echo(f"Error: {e.format_message()}", err=True)
            click.echo("Try 'ytcli-dl -h' for help.", err=True)
            sys.exit(1)

class CustomPath(click.Path):
    def convert(self, value, param, ctx):
        try:
            return super().convert(value, param, ctx)
        except click.BadParameter as e:
            click.echo(f"Error: {e.format_message()}", err=True)
            click.echo("Try 'ytcli-dl -h' for help.", err=True)
            sys.exit(1)

class CustomString(click.ParamType):
    name = "text"
    
    def convert(self, value, param, ctx):
        try:
            if value is None:
                return None
            return str(value)
        except (ValueError, TypeError) as e:
            click.echo(f"Error: Invalid value for {param.name}: {value}", err=True)
            click.echo("Try 'ytcli-dl -h' for help.", err=True)
            sys.exit(1)

class NoBlankLineCommand(click.Command):
    def make_context(self, info_name, args, parent=None, **extra):
        ctx = super().make_context(info_name, args, parent, **extra)
        
        original_fail = ctx.fail
        def custom_fail(message, code=1):
            click.echo(f"Error: {message}", err=True)
            click.echo("Try 'ytcli-dl -h' for help.", err=True)
            sys.exit(code)
        ctx.fail = custom_fail
        
        return ctx

@click.command(cls=NoBlankLineCommand, context_settings={"help_option_names": ["-h", "--help"]})
@click.argument('url', required=False, type=CustomString())
@click.option(
    '-q', '--quality', 
    type=CustomChoice(list(QUALITY_OPTIONS.keys())), 
    default='best',
    help='Video quality to download (default: best)',
)
@click.option(
    '-a', '--audio-only', 
    is_flag=True,
    help='Download audio only (MP3 format)'
)
@click.option(
    '-o', '--output', 
    type=CustomPath(),
    default=DEFAULT_DOWNLOAD_DIR,
    help=f'Output directory for downloads (default: {DEFAULT_DOWNLOAD_DIR})'
)
@click.option(
    '-p', '--playlist', 
    is_flag=True,
    help='Download entire playlist'
)
@click.option(
    '-f', '--file', 
    type=CustomPath(exists=True),
    help='Download URLs from text file (one URL per line)'
)
@click.option(
   '-l', '--list-formats', 
    is_flag=True,
    help='List available formats for the video without downloading'
)
@click.option(
    '--format-code',
    type=CustomString(),
    help='Download specific format (e.g., "137+140" for 1080p video + audio)'
)
@click.version_option(__version__, '-v', '--version', prog_name='ytcli-dl')
def main(url, quality, audio_only, output, playlist, file, list_formats, format_code):
    
    if list_formats:
        if not url:
            click.echo("Error: --list-formats requires a URL", err=True)
            click.echo("Try 'ytcli-dl -h' for help.", err=True)
            sys.exit(1)
        list_video_formats(url)
        sys.exit(0)

    if not url and not file:
        click.echo("Error: You must provide either a URL or use --file option", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)

    if url and file:
        click.echo("Error: Cannot use both URL argument and --file option simultaneously", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)

    if format_code and audio_only:
        click.echo("Error: Cannot use --format-code with --audio-only", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)

    try:
        downloader = YouTubeDownloader(
            output_dir=output,
            quality=quality,
            audio_only=audio_only,
            format_code=format_code
        )

        click.echo(f"Output directory: {downloader.output_dir}")
        if format_code:
            click.echo(f"Custom format: {format_code}")
        else:
            mode_text = "Audio only (MP3)" if audio_only else f"Quality: {quality}"
            click.echo(f"Mode: {mode_text}")

    except Exception as e:
        click.echo(f"Error: Failed to initialize downloader - {str(e)}", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)

    success = False

    try:
        if file:
            urls = read_urls_from_file(file)
            if not urls:
                click.echo("Error: No valid URLs found in the file", err=True)
                click.echo("Try 'ytcli-dl -h' for help.", err=True)
                sys.exit(1)
            click.echo(f"Found {len(urls)} valid URLs in file.")
            results = downloader.download_multiple_urls(urls)
            success = any(results.values())

        elif url:
            if playlist or validate_playlist_url(url):
                success = downloader.download_playlist(url)
            else:
                if not validate_url(url):
                    click.echo(f"Error: Invalid YouTube URL - {url}", err=True)
                    click.echo("Try 'ytcli-dl -h' for help.", err=True)
                    sys.exit(1)
                success = downloader.download_single_video(url)

    except KeyboardInterrupt:
        click.echo("Error: Download interrupted by user", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: Unexpected error - {str(e)}", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)

    if success:
        click.secho("Download completed successfully!", fg='green')
        sys.exit(0)
    else:
        click.echo("Error: Download failed or was cancelled", err=True)
        click.echo("Try 'ytcli-dl -h' for help.", err=True)
        sys.exit(1)