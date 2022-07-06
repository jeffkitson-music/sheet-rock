import spotify_auth
import csv
import spotify_playlist


# Variables
book = "What's That Sound? Covach & Flory (6th ed.)"
class_name = "History of Rock (6th)"
csv_filename = "<INSERT CSV FILENAME HERE>"

# Dictionaries and Lists
full_track_list = {'playlist_id': "", "tracks": []}  # remember to split this in half!
tracks_by_era = {}
tracks_by_chapter = {}
chapter_titles = ["front matter"]  # included "front matter" so chapters align with indexes


def main():
    # Step 1: Refresh Auth Token
    token = spotify_auth.refresh()
   
    # Not working yet!
    #else:
     #   print("Spotify credentials not configured!")
      #  spotify_auth.setup() 

    # Step 2: Load CSV data
    headers, track_data = load_csv(csv_filename)
    print(f"Headers: {headers}") 

    # Step 3: Set-up track dictionaries
    process_tracks(track_data)

    # Step 4: Make Playlists
    # Personal preference on ordering(because they appear last to first): Chapters, Eras, Complete
    make_chapter_playlists(token)
    make_era_playlists(token)
    make_complete_playlist(token)


def load_csv(filename):
    headers = []
    rows = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        playlist_reader = csv.reader(csvfile)

        # extracting field names through first row
        headers = next(playlist_reader)

        # extracting each data row one by one
        for row in playlist_reader:
            rows.append(row)
    return headers, rows


def process_tracks(track_data):
    # Efficient! One Loop!
    # NEW HEADERS Track #,Era,Chapter,Chapter Title,Artist,Song Title,Page,Year,Spotify Link
    for track in track_data:
        uil = f"spotify:track:{track[-1].split('/')[-1]}"
        # Add to full list
        full_track_list['tracks'].append(uil)

        # Add to Era List
        if not track[1] in tracks_by_era:
            tracks_by_era[track[1]] = {'playlist_id': "", "tracks": []}  # was []
        tracks_by_era[track[1]]["tracks"].append(uil)

        # Add to Chapter Lists
        if not track[2] in tracks_by_chapter:
            tracks_by_chapter[track[2]] = {'playlist_id': "", "title": track[3], "tracks": []}  # was []
        tracks_by_chapter[track[2]]["tracks"].append(uil)

    print(full_track_list)
    print(tracks_by_era)
    print(tracks_by_chapter)
    return


def make_chapter_playlists(token):
    # Remember: Reverse order!
    for ch in reversed(tracks_by_chapter):
        tracks_by_chapter[ch]["playlist_id"] = spotify_playlist.make(
            f"Ch. {int(ch)}: {tracks_by_chapter[ch]['title']} ", book, token)
        spotify_playlist.add_tracks(tracks_by_chapter[ch]["playlist_id"], tracks_by_chapter[ch]["tracks"], token)


def make_era_playlists(token):
    for era in reversed(tracks_by_era):
        tracks_by_era[era]["playlist_id"] = spotify_playlist.make(era,
                                                                  f"{book}, Era: The {era}",
                                                                  token)
        spotify_playlist.add_tracks(tracks_by_era[era]["playlist_id"], tracks_by_era[era]["tracks"], token)


def make_complete_playlist(token):
    full_track_list["playlist_id"] = spotify_playlist.make(f"{class_name} Complete", book, token)
    # Gotta split the list - spotify limits 100 tracks/request
    full_split = [full_track_list["tracks"][:50], full_track_list["tracks"][50:]]

    # Make them!
    spotify_playlist.add_tracks(full_track_list["playlist_id"], full_split[0], token)
    spotify_playlist.add_tracks(full_track_list["playlist_id"], full_split[1], token)


if __name__ == "__main__":
    main()
