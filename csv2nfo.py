#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os
import argparse

# Function to ensure 'nfo' directory exists
def ensure_nfo_directory_exists():
    output_dir = "nfo"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Function to sanitize filenames by replacing spaces with periods and keeping only alphanumeric characters and periods
def sanitize_filename(title):
    # Replace spaces with periods
    title = title.replace(" ", ".")

    # Remove specific punctuation (like apostrophes) instead of replacing them with periods
    title = title.replace("'", "")  # Remove apostrophes

    # Keep only alphanumeric characters, periods, and hyphens
    sanitized_title = "".join(char for char in title if char.isalnum() or char in ".-")

    # Replace multiple periods with a single period using a while loop
    while ".." in sanitized_title:
        sanitized_title = sanitized_title.replace("..", ".")

    # Remove leading and trailing periods
    return sanitized_title.strip(".")

def generate_movie_nfo(entry_data, output_dir="."):
    # Sanitize the movie title
    movie_title = sanitize_filename(entry_data['title'])
    year = entry_data['year']
    
    # Create the formatted filename: MovieTitle.Year.nfo
    filename = f"{movie_title}.{year}.nfo"
    
    # Path to save the NFO file
    output_path = os.path.join(output_dir, filename)
    
    nfo_content = "<movie>\n"
    
    movie_tags_to_include = ['title', 'year', 'dateadded', 'actor1', 'actor2', 'actor3']
    
    for tag in movie_tags_to_include:
        if tag.startswith('actor'):
            actor_number = tag[-1]
            actor_name_key = f'actor_{actor_number}_name'
            actor_role_key = f'actor_{actor_number}_role'
            actor_order_key = f'actor_{actor_number}_order'
            actor_thumb_key = f'actor_{actor_number}_thumb'
            
            if all(k in entry_data for k in [actor_name_key, actor_role_key, actor_order_key, actor_thumb_key]):
                nfo_content += "<actor>\n"
                nfo_content += f"<name>{entry_data[actor_name_key]}</name>\n"
                nfo_content += f"<role>{entry_data[actor_role_key]}</role>\n"
                nfo_content += f"<order>{entry_data[actor_order_key]}</order>\n"
                nfo_content += f"<thumb>{entry_data[actor_thumb_key]}</thumb>\n"
                nfo_content += "</actor>\n"
        else:
            if tag in entry_data:
                nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</movie>"
    
    # Write the NFO content to the file
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())
    
    # Commented out the output
    # print(f"NFO file created: {output_path}")

def generate_tvshow_nfo(entry_data, output_dir="."):
    tvshow_tags_to_include = ['show_title', 'year']
    nfo_content = "<tvshow>\n"
    
    # Include the necessary tags in the NFO content
    for tag in tvshow_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</tvshow>"
    
    # Set the filename to always be 'tvshow.nfo'
    filename = "tvshow.nfo"
    
    # Define the output path for the NFO file
    output_path = os.path.join(output_dir, filename)
    
    # Write the NFO content to the file
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())


def generate_episode_nfo(entry_data, output_dir="."):
    show_title = sanitize_filename(entry_data['show_title'])
    year = entry_data['year']
    season = entry_data['season']
    episode = entry_data['episode']
    episode_title = sanitize_filename(entry_data['title'])

    # Create the formatted filename: ShowTitle.Year.SXXEXX.EpisodeTitle.nfo
    filename = f"{show_title}.{year}.S{season.zfill(2)}E{episode.zfill(2)}.{episode_title}.nfo"
    
    # Path to save the NFO file
    output_path = os.path.join(output_dir, filename)
    
    nfo_content = "<episodedetails>\n"
    nfo_content += f"<title>{entry_data['title']}</title>\n"
    nfo_content += f"<season>{entry_data['season']}</season>\n"
    nfo_content += f"<episode>{entry_data['episode']}</episode>\n"
    nfo_content += f"<aired>{entry_data['release_date']}</aired>\n"
    nfo_content += "</episodedetails>"
    
    # Write the NFO content to the file
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_music_nfo(entry_data, output_dir="."):
    music_title = sanitize_filename(entry_data['title'])
    
    # Create the formatted filename: MusicTitle.Year.nfo
    filename = f"{music_title}.{entry_data['year']}.nfo"
    
    nfo_content = "<music>\n"
    
    music_tags_to_include = ['title', 'year', 'dateadded', 'album', 'artist']
    
    for tag in music_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</music>"
    
    # Path to save the NFO file
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def find_entries(csv_file, search_term):
    matches = []
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for field in row.values():
                    if search_term.lower() in field.lower():
                        matches.append(row)
                        break  # Break to avoid adding the same row multiple times if the term appears in multiple fields
    return matches

# Function to find entries in by column only
def find_entries_by_column(csv_file, search_term, column):
    matches = []
    unique_titles = set()  # Track unique titles to avoid duplicates

    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Iterate through each row and search only in the specified column
            for row in reader:
                title = row[column].strip().lower()
                if search_term.lower() in title and title not in unique_titles:
                    matches.append(row)
                    unique_titles.add(title)  # Ensure uniqueness
    return matches

if __name__ == "__main__":
    # Set up basic argparse
    parser = argparse.ArgumentParser(description="Generate NFO files from CSV.")
    parser.add_argument('-m', '--movies', action='store_true', help='Search only in movies.csv')
    parser.add_argument('-e', '--episodes', action='store_true', help='Search only in tvshows.csv (episodes)')
    parser.add_argument('-s', '--songs', action='store_true', help='Search only in music.csv')
    parser.add_argument('-t', '--tvshow', action='store_true', help='Search only by TV show name in tvshows.csv')
    parser.add_argument('search_term', help='The search term for filtering entries')
    args = parser.parse_args()

    # Ensure 'nfo' directory exists
    output_dir = ensure_nfo_directory_exists()

    # Define the CSV files to search in the 'csv' directory
    csv_dir = "csv"

    # Apply filtering logic based on flags
    if args.tvshow:
        csv_files = {os.path.join(csv_dir, "tvshows.csv"): generate_tvshow_nfo}
    else:
        csv_files = {
            os.path.join(csv_dir, "movies.csv"): generate_movie_nfo,
            os.path.join(csv_dir, "tvshows.csv"): generate_episode_nfo,
            os.path.join(csv_dir, "music.csv"): generate_music_nfo
        }

    # Counter for NFO files created
    nfo_count = 0

    # Iterate through each CSV file and apply the corresponding function
    for csv_file, nfo_function in csv_files.items():
        if args.tvshow and nfo_function == generate_tvshow_nfo:
            # Use find_entries_by_column to search only the 'title' column for TV shows
            entries = find_entries_by_column(csv_file, args.search_term, column='show_title')

            if entries:
                generate_tvshow_nfo(entries[0], output_dir)  # Process only the first match
                nfo_count += 1
        else:
            # Use the simpler find_entries to search across all columns
            entries = find_entries(csv_file, args.search_term)

            if entries:
                for entry in entries:
                    nfo_function(entry, output_dir)  # Pass the 'nfo' directory as output_dir
                    nfo_count += 1

    # Provide feedback on the number of NFO files created
    if nfo_count > 0:
        print(f"{nfo_count} NFO file{'s' if nfo_count > 1 else ''} created.")
    else:
        print("0 NFO files created. No matches found.")
