#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import argparse

# Function to ensure 'nfo' directory exists
def ensure_nfo_directory_exists():
    output_dir = "nfo"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Function to generate tvshow.nfo
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

# Function to find entries in a specific column only
def find_entries_by_column(csv_file, search_term, column):
    matches = {}
    
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Iterate through each row and search only in the specified column
            for row in reader:
                if column in row:
                    title = row[column].strip().lower()
                    # Only add unique titles
                    if search_term.lower() in title:
                        matches[title] = row  # Keep the last entry for each unique title
    return matches

if __name__ == "__main__":
    # Set up basic argparse
    parser = argparse.ArgumentParser(description="Generate NFO files from CSV.")
    parser.add_argument('-t', '--tvshow', action='store_true', help='Search only in tvshows.csv (tvshow)')
    parser.add_argument('search_term', help='The search term for filtering entries')
    args = parser.parse_args()

    # Ensure 'nfo' directory exists
    output_dir = ensure_nfo_directory_exists()

    # Define the CSV files to search in the 'csv' directory
    csv_dir = "csv"

    if args.tvshow:
        csv_file = os.path.join(csv_dir, "tvshows.csv")
        # Search only the 'show_title' column for TV shows
        entries = find_entries_by_column(csv_file, args.search_term, column='show_title')
    else:
        print("No flag specified")
        sys.exit()

    # Generate NFO files for each unique TV show
    if entries:
        for title, entry in entries.items():
            generate_tvshow_nfo(entry, output_dir)
        print(f"tvshow.nfo file created for '{args.search_term}'.")
    else:
        print("0 NFO files created. No matches found.")

#
