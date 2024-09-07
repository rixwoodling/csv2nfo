#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os
import argparse

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
    
    output_path = os.path.join(output_dir, "tvshow.nfo")
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())

def generate_episode_nfo(entry_data, output_dir="."):
    # Function to generate episode NFO
    pass

def generate_music_artist_nfo(entry_data, output_dir="."):
    # Function to generate music artist NFO
    pass

def generate_song_nfo(entry_data, output_dir="."):
    # Function to generate song NFO
    pass

def find_entries(csv_file, search_term):
    matches = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if search_term.lower() in row['title'].lower():
                matches.append(row)
    return matches

def process_csv(csv_file, search_term, nfo_function, max_matches=None):
    entries = find_entries(csv_file, search_term)
    if max_matches and len(entries) > max_matches:
        print(f"Error: Found {len(entries)} matches. Please refine your search.")
        return
    for entry in entries:
        nfo_function(entry)

def process_all_csvs(search_term):
    csv_dir = "csv"
    
    # Process movies
    csv_file = os.path.join(csv_dir, "movies.csv")
    process_csv(csv_file, search_term, generate_movie_nfo)
    
    # Process TV episodes
    csv_file = os.path.join(csv_dir, "tvshows.csv")
    process_csv(csv_file, search_term, generate_episode_nfo)
    
    # Process songs
    csv_file = os.path.join(csv_dir, "music.csv")
    process_csv(csv_file, search_term, generate_song_nfo)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate NFO files based on CSV data")
    parser.add_argument("search_term", help="The term to search for in the CSV files")
    parser.add_argument("-m", "--movie", action="store_true", help="Generate movie NFOs")
    parser.add_argument("-t", "--tvshow", action="store_true", help="Generate TV show NFO")
    parser.add_argument("-e", "--episode", action="store_true", help="Generate episode NFOs")
    parser.add_argument("-a", "--artist", action="store_true", help="Generate music artist NFOs")
    parser.add_argument("-s", "--song", action="store_true", help="Generate song NFOs")
    
    args = parser.parse_args()
    search_term = args.search_term

    csv_dir = "csv"
    
    # Logic to handle flags
    if args.movie:
        csv_file = os.path.join(csv_dir, "movies.csv")
        process_csv(csv_file, search_term, generate_movie_nfo)
    
    elif args.tvshow:
        csv_file = os.path.join(csv_dir, "tvshows.csv")
        entries = find_entries(csv_file, search_term)
        if len(entries) == 0:
            print(f"Error: No TV show found for '{search_term}'.")
        elif len(entries) > 1:
            print(f"Error: Found {len(entries)} TV shows for '{search_term}'. Please refine your search to return only one result.")
            for entry in entries:
                print(f"- {entry['title']} ({entry['year']})")
        else:
            generate_tvshow_nfo(entries[0])  # Generate NFO if exactly one match is found
    
    elif args.episode:
        csv_file = os.path.join(csv_dir, "tvshows.csv")
        process_csv(csv_file, search_term, generate_episode_nfo)
    
    elif args.artist:
        csv_file = os.path.join(csv_dir, "music.csv")
        entries = find_entries(csv_file, search_term)
        if len(entries) == 0:
            print(f"Error: No music artist found for '{search_term}'.")
        elif len(entries) > 1:
            print(f"Error: Found {len(entries)} music artists for '{search_term}'. Please refine your search to return only one result.")
            for entry in entries:
                print(f"- {entry['title']} ({entry['year']})")
        else:
            generate_music_artist_nfo(entries[0])  # Generate NFO if exactly one match is found
    
    elif args.song:
        csv_file = os.path.join(csv_dir, "music.csv")
        process_csv(csv_file, search_term, generate_song_nfo)
    
    else:
        # Default case: Search for all matching results in movies, episodes, and songs
        process_all_csvs(search_term)

#
