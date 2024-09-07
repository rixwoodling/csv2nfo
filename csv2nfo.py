#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os

def generate_movie_nfo(entry_data, output_dir="."):
    movie_tags_to_include = ['title', 'year', 'dateadded', 'actor1', 'actor2', 'actor3']  # Add actors as needed
    nfo_content = "<movie>\n"
    
    for tag in movie_tags_to_include:
        if tag.startswith('actor'):
            actor_number = tag[-1]  # Get the actor number from 'actor1', 'actor2', etc.
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
    
    output_path = os.path.join(output_dir, f"{entry_data['title']}.nfo")
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_tvshow_nfo(entry_data, output_dir="."):
    tvshow_tags_to_include = ['title', 'year', 'dateadded', 'season', 'episode']
    nfo_content = "<tvshow>\n"
    
    for tag in tvshow_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</tvshow>"
    
    output_path = os.path.join(output_dir, f"{entry_data['title']}.nfo")
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_music_nfo(entry_data, output_dir="."):
    music_tags_to_include = ['title', 'year', 'dateadded', 'album', 'artist']
    nfo_content = "<music>\n"
    
    for tag in music_tags_to_include:
        if tag in entry_data:
            nfo_content += f"<{tag}>{entry_data[tag]}</{tag}>\n"

    nfo_content += "</music>"
    
    output_path = os.path.join(output_dir, f"{entry_data['title']}.nfo")
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv2nfo.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1]
    
    # Define the CSV files to search in the 'csv' directory
    csv_dir = "csv"
    csv_files = {
        os.path.join(csv_dir, "movies.csv"): generate_movie_nfo,
        os.path.join(csv_dir, "tvshows.csv"): generate_tvshow_nfo,
        os.path.join(csv_dir, "music.csv"): generate_music_nfo
    }

    # Iterate through each CSV file and apply the corresponding function
    for csv_file, nfo_function in csv_files.items():
        entries = find_entries(csv_file, search_term)
        if entries:
            for entry in entries:
                nfo_function(entry)
