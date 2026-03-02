#!/usr/bin/env python3
"""
Create a new song page for SongShare.
Usage: python3 create_song.py [date]
  date format: M-D-YY (e.g., 3-2-26)
  If date not provided, you'll be prompted.
"""

import sys
import os
from pathlib import Path

def parse_date(date_str):
    """Parse and validate date string in M-D-YY format."""
    try:
        parts = date_str.split('-')
        if len(parts) != 3:
            return None
        month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
        if not (1 <= month <= 12 and 1 <= day <= 31 and 0 <= year <= 99):
            return None
        return date_str
    except ValueError:
        return None

def format_date_display(date_str):
    """Convert M-D-YY to display format (e.g., 3-1-26 -> Mar 1st)."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    
    parts = date_str.split('-')
    month, day = int(parts[0]), int(parts[1])
    
    month_str = months[month - 1]
    suffix = suffixes.get(day % 10 if day % 10 in suffixes else 0, 'th')
    
    return f"{month_str} {day}{suffix}"

def create_song_page(date, artist, song_title, links):
    """Generate the HTML content for a song page."""
    image_path = f"/songshare/assets/{date}.jpg"
    
    # helper to render a link or placeholder text
    def render_link(url, label):
        if url:
            return f'<a href = "{url}">{label}</a>'
        else:
            return f'<span>{label}: Not found, sorry</span>'

    html_template = f"""<!DOCTYPE html>
<html>
  <head>
    <title>SongShare</title>
    <meta name = "description" content = "A song-sharing site!">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/songshare/styles.css">
    <style>
      @font-face {{
        font-family: "Bpmf Huninn", sans-serif;
        src: url(assets/fonts/BpmfHuninn-Regular.ttf);
      }} 
      @font-face {{
        font-family: "Montserrat", sans-serif;
        src: url(assets/fonts/Montserrat-VariableFont_wght.ttf);
      }} 
    </style>
  </head>
  <body>
    <header>
        <a href = "/songshare"><h1>SongShare</h1></a>
        <h3>You have no excuse to not listen to the song now!</h3>
    </header>
    <h3>{artist} - {song_title}</h3>
    <!-- USE SPOTIFY ALBUM COVER -->
    <img src="{image_path}" alt="ALBUM COVER" height="25%" width="25%">
    <hr>
    <div class = "links">
        {render_link(links.get('spotify', ''), 'Spotify')}
        {render_link(links.get('soundcloud', ''), 'Soundcloud')}
        {render_link(links.get('apple', ''), 'Apple Music')}
        {render_link(links.get('youtube', ''), 'Youtube Music')}
        {render_link(links.get('tidal', ''), 'TIDAL')}
        {render_link(links.get('qobuz', ''), 'Qobuz')}
        <a href = "mailto:archnails@proton.me?subject=My%20music%20service%20is%20not%20listed.&body=Hello%20developer%2C%0A%0AI%20use%20%5BYOUR%20MUSIC%20SERVICE%20HERE%5D.%0A%0ACheck.%0A%0ASincerely%2C%0A%0AA%20user">My music service is not listed here! HA!</a>
    </div>
  </body>
</html>"""
    
    return html_template

def main():
    # Get date
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        while True:
            date = input("Enter date (M-D-YY format, e.g., 3-2-26): ").strip()
            if parse_date(date):
                break
            print("Invalid date format. Use M-D-YY (e.g., 3-2-26)")
    
    # Get artist and song
    artist = input("Enter artist name: ").strip()
    song_title = input("Enter song title: ").strip()
    
    if not artist or not song_title:
        print("Artist and song title are required.")
        return
    
    # Get music service links
    services = {
        'spotify': 'Spotify',
        'soundcloud': 'Soundcloud',
        'apple': 'Apple Music',
        'youtube': 'Youtube Music',
        'tidal': 'TIDAL',
        'qobuz': 'Qobuz'
    }
    
    links = {}
    print("\nEnter music service links (press Enter to skip):")
    for key, name in services.items():
        url = input(f"{name} URL: ").strip()
        if url:
            links[key] = url
    
    # Create the HTML file
    base_dir = Path(__file__).parent
    output_file = base_dir / "songs" / f"{date}.html"
    
    # If file exists, add a number suffix
    if output_file.exists():
        counter = 1
        while True:
            output_file = base_dir / "songs" / f"{date}-{counter}.html"
            if not output_file.exists():
                break
            counter += 1
        print(f"File for {date} exists. Creating {output_file.name} instead.")
    
    html_content = create_song_page(date, artist, song_title, links)
    output_file.write_text(html_content)
    print(f"\n✓ Created {output_file.name}")
    
    # Ask if user wants to update index.html
    update_index = input("Update index.html with new song? (y/n): ").strip().lower()
    if update_index == 'y':
        update_index_file(output_file, date, artist, song_title, base_dir)

def update_index_file(output_file, date, artist, song_title, base_dir):
    """Add new song to index.html's latest list."""
    index_file = base_dir / "index.html"
    content = index_file.read_text()
    
    # Create the new link HTML
    date_display = format_date_display(date)
    relative_path = output_file.name
    new_link = f'      <a href="songs/{relative_path}"><u>{date_display}</u></a>'
    
    # Find the list div and insert the new song at the top
    list_start = content.find('<div class = "list">')
    list_content_start = content.find('\n', list_start) + 1
    
    # Insert new link after the opening div
    new_content = content[:list_content_start] + new_link + '\n' + content[list_content_start:]
    
    index_file.write_text(new_content)
    print(f"✓ Updated index.html with {date_display}")

if __name__ == "__main__":
    main()
