#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os

def generate_nfo(movie_data, output_dir="."):
    nfo_content = f"""
<movie>
    <title>{movie_data['title']}</title>
    <originaltitle>{movie_data['originaltitle']}</originaltitle>
    <sorttitle>{movie_data['sorttitle']}</sorttitle>
    <tag>{movie_data['tag']}</tag>
    <set>{movie_data['set']}</set>
    <year>{movie_data['year']}</year>
    <ratings>
        <rating>
            <name>imdb</name>
            <value>{movie_data['ratings_imdb']}</value>
        </rating>
    </ratings>
    <userrating>{movie_data['userrating']}</userrating>
    <plot>{movie_data['plot']}</plot>
    <tagline>{movie_data['tagline']}</tagline>
    <runtime>{movie_data['runtime']}</runtime>
    <thumb>{movie_data['thumb']}</thumb>
    <fanart>{movie_data['fanart']}</fanart>
    <mpaa>{movie_data['mpaa']}</mpaa>
    <playcount>{movie_data['playcount']}</playcount>
    <genre>{movie_data['genre']}</genre>
    <country>{movie_data['country']}</country>
    <premiered>{movie_data['premiered']}</premiered>
    <studio>{movie_data['studio']}</studio>
    <credits>{movie_data['credits']}</credits>
    <director>{movie_data['director']}</director>
    <trailer>{movie_data['trailer']}</trailer>
    <actor>
        <name>{movie_data['actor_1_name']}</name>
        <role>{movie_data['actor_1_role']}</role>
        <order>{movie_data['actor_1_order']}</order>
        <thumb>{movie_data['actor_1_thumb']}</thumb>
    </actor>
    <actor>
        <name>{movie_data['actor_2_name']}</name>
        <role>{movie_data['actor_2_role']}</role>
        <order>{movie_data['actor_2_order']}</order>
        <thumb>{movie_data['actor_2_thumb']}</thumb>
    </actor>
    <actor>
        <name>{movie_data['actor_3_name']}</name>
        <role>{movie_data['actor_3_role']}</role>
        <order>{movie_data['actor_3_order']}</order>
        <thumb>{movie_data['actor_3_thumb']}</thumb>
    </actor>
    <uniqueid type="imdb">{movie_data['uniqueid_imdb']}</uniqueid>
    <uniqueid type="tmdb">{movie_data['uniqueid_tmdb']}</uniqueid>
    <fileinfo>
        <streamdetails>
            <video>
                <codec>{movie_data['video_codec']}</codec>
                <aspect>{movie_data['video_aspect']}</aspect>
                <width>{movie_data['video_width']}</width>
                <height>{movie_data['video_height']}</height>
                <durationinseconds>{movie_data['video_duration']}</durationinseconds>
            </video>
            <audio>
                <codec>{movie_data['audio_codec']}</codec>
                <language>{movie_data['audio_language']}</language>
                <channels>{movie_data['audio_channels']}</channels>
            </audio>
            <subtitle>
                <language>{movie_data['subtitle_language']}</language>
            </subtitle>
        </streamdetails>
    </fileinfo>
    <dateadded>{movie_data['dateadded']}</dateadded>
</movie>
"""
    output_path = os.path.join(output_dir, f"{movie_data['title']}.nfo")
    with open(output_path, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content.strip())
    print(f"NFO file created: {output_path}")

def find_movie_by_imdb_id(csv_file, imdb_id):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['uniqueid_imdb'] == imdb_id:
                return row
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_nfo.py <uniqueid_imdb>")
        sys.exit(1)

    imdb_id = sys.argv[1]
    csv_file = "movies.csv"  # Adjust this path if needed
    movie_data = find_movie_by_imdb_id(csv_file, imdb_id)

    if movie_data:
        generate_nfo(movie_data)
    else:
        print(f"No movie found with IMDb ID: {imdb_id}")


