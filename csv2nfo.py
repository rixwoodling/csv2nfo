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

# Function to create the directory structure based on the -d flag
def get_output_directory(base_dir, title, year, use_directory_flag, season=None):
    if use_directory_flag:
        # Sanitize title and year for directory structure
        sanitized_title = sanitize_filename(f"{title} ({year})")
        show_or_movie_dir = os.path.join(base_dir, sanitized_title)
        if not os.path.exists(show_or_movie_dir):
            os.makedirs(show_or_movie_dir)
        if season:
            season_dir = os.path.join(show_or_movie_dir, f"S{season.zfill(2)}")
            if not os.path.exists(season_dir):
                os.makedirs(season_dir)
            return season_dir
        return show_or_movie_dir
    # Default behavior: return the base directory
    return base_dir

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

def generate_movie_nfo(entry_data, output_dir=".", use_directory_flag=False):
    movie_title = sanitize_filename(entry_data['title'])
    year = entry_data['year']

    # Get the output directory based on the -d flag
    output_dir = get_output_directory(output_dir, entry_data['title'], year, use_directory_flag)

    # Create the formatted filename: MovieTitle.Year.nfo
    filename = f"{movie_title}.{year}.nfo"
    output_path = os.path.join(output_dir, filename)

    nfo_content = "<movie>\n"
    movie_tags_to_include = ['title', 'year']

    for tag in movie_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</movie>"

    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_tvshow_nfo(entry_data, output_dir=".", use_directory_flag=False):
    tvshow_tags_to_include = ['show_title', 'year']

    # Get the output directory based on the -d flag
    output_dir = get_output_directory(output_dir, entry_data['show_title'], entry_data['year'], use_directory_flag)

    filename = "tvshow.nfo"
    output_path = os.path.join(output_dir, filename)

    nfo_content = "<tvshow>\n"
    for tag in tvshow_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"
    nfo_content += "</tvshow>"

    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_episode_nfo(entry_data, output_dir=".", use_directory_flag=False):
    show_title = sanitize_filename(entry_data['show_title'])
    year = entry_data['year']
    season = entry_data['season']
    episode = entry_data['episode']
    episode_title = sanitize_filename(entry_data['title'])

    # Get the output directory based on the -d flag (with season subdirectory)
    output_dir = get_output_directory(output_dir, entry_data['show_title'], year, use_directory_flag, season)

    # Create the formatted filename: SXXEXX.EpisodeTitle.nfo
    filename = f"S{season.zfill(2)}E{episode.zfill(2)}.{episode_title}.nfo"
    output_path = os.path.join(output_dir, filename)

    nfo_content = "<episodedetails>\n"
    nfo_content += f"<title>{entry_data['title']}</title>\n"
    nfo_content += f"<season>{entry_data['season']}</season>\n"
    nfo_content += f"<episode>{entry_data['episode']}</episode>\n"
    nfo_content += f"<aired>{entry_data['release_date']}</aired>\n"
    nfo_content += "</episodedetails>"

    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_music_nfo(entry_data, output_dir=".", use_directory_flag=False):
    music_title = sanitize_filename(entry_data['title'])
    year = entry_data['year']

    # Get the output directory based on the -d flag
    output_dir = get_output_directory(output_dir, entry_data['title'], year, use_directory_flag)

    # Create the formatted filename: MusicTitle.Year.nfo
    filename = f"{music_title}.{year}.nfo"
    output_path = os.path.join(output_dir, filename)

    nfo_content = "<music>\n"
    music_tags_to_include = ['title', 'year', 'album', 'artist']

    for tag in music_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</music>"

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
                        break  # Avoid adding the same row multiple times if the term appears in multiple fields
    return matches

# Function to find entries in by column only
def find_entries_by_column(csv_file, search_term, column):
    exact_matches = []
    partial_matches = []
    unique_entries = set()  # To keep track of unique show_title and year combinations

    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row[column].strip().lower()
                search_term_lower = search_term.strip().lower()
                year = row['year'].strip()

                # Create a unique identifier for title and year
                unique_identifier = f"{title} ({year})"

                # Check for an exact match (case-insensitive)
                if title == search_term_lower:
                    if unique_identifier not in unique_entries:
                        exact_matches.append(row)
                        unique_entries.add(unique_identifier)
                # Check for a partial match
                elif search_term_lower in title:
                    if unique_identifier not in unique_entries:
                        partial_matches.append(row)
                        unique_entries.add(unique_identifier)

    # Return exact matches if available, otherwise return partial matches
    if exact_matches:
        return exact_matches
    return partial_matches

if __name__ == "__main__":
    # Set up basic argparse
    parser = argparse.ArgumentParser(description="Generate NFO files from CSV.")
    parser.add_argument('-m', '--movies', action='store_true', help='Search only in movies.csv')
    parser.add_argument('-e', '--episodes', action='store_true', help='Search only in tvshows.csv (episodes)')
    parser.add_argument('-s', '--songs', action='store_true', help='Search only in music.csv')
    parser.add_argument('-t', '--tvshow', action='store_true', help='Search only by TV show name in tvshows.csv')
    parser.add_argument('-d', '--directory', action='store_true', help='Store NFOs in individual directories')
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
                if args.directory:
                    # If -d is used, generate NFO for all matches without asking for clarification
                    for entry in entries:
                        generate_tvshow_nfo(entry, output_dir, args.directory)
                        nfo_count += 1
                else:
                    # If no -d flag, prompt for clarification if multiple matches found
                    if len(entries) > 1:
                        print(f"Multiple matches found for '{args.search_term}':")
                        for entry in entries:
                            print(f"- {entry['show_title']} ({entry['year']})")
                        # Prompt user for the year
                        specified_year = input("Please specify the year: ").strip()

                        # Search for the entry with the specified year
                        selected_entry = next((entry for entry in entries if entry['year'] == specified_year), None)

                        if selected_entry:
                            generate_tvshow_nfo(selected_entry, output_dir, args.directory)
                            nfo_count += 1
                        else:
                            print(f"No match found for the year '{specified_year}'. Exiting.")
                            sys.exit(1)
                    else:
                        generate_tvshow_nfo(entries[0], output_dir, args.directory)
                        nfo_count += 1
            else:
                print(f"No matches found for '{args.search_term}'.")
                sys.exit(1)
        else:
            # Use the find_entries function to search across all columns
            entries = find_entries(csv_file, args.search_term)
            if entries:
                for entry in entries:
                    nfo_function(entry, output_dir, args.directory)
                    nfo_count += 1

    # Provide feedback on the number of NFO files created
    if nfo_count > 0:
        print(f"{nfo_count} NFO file{'s' if nfo_count > 1 else ''} created.")
    else:
        print("0 NFO files created. No matches found.")

#
