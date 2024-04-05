def main(playlist_id):
    import os
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    # Define your Spotify client credentials
    client_id = "d1a4e68b7bee4bb291d1fb6458556496"
    client_secret = "cf680ef40aab402881f35e9f0bef3b21"
    redirect_uri = 'http://localhost:8000/callback'

    filename = (os.path.splitext(os.path.basename(__file__))[0])
    cache_path = ("C:\\Users\\Clayton\\AppData\\Local\\Temp\\vscode\\" +filename+ ".cache")

    # Authenticate with Spotify
    scope = 'playlist-read-private playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope,cache_path=cache_path))


    # Get tracks from the playlist
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # List to store explicit tracks
    explicit_tracks = []

    # Iterate over tracks
    for track in tracks:
        # Get track details
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        is_explicit = track['track']['explicit']
        
        if is_explicit:
            explicit_tracks.append((track_name, artist_name))

    # Prompt user to choose which explicit tracks to keep
    print("Explicit tracks found in the playlist:\n")
    for i, track in enumerate(explicit_tracks):
        print(f"{i+1}. {track[0]} by {track[1]}")
    print()

    selection = "0"

    if selection == "-1":
        tracks_to_keep = explicit_tracks
    elif selection == "0":
        tracks_to_keep = []
    else:
        selected_nums = [int(num) for num in selection.split(",")]
        tracks_to_keep = [explicit_tracks[num-1] for num in selected_nums if 1 <= num <= len(explicit_tracks)]

    # Remove explicit tracks that are not selected to be kept
    track_ids_to_remove = [track['track']['id'] for track in tracks if (track['track']['explicit'] and (track['track']['name'], track['track']['artists'][0]['name']) not in tracks_to_keep)]
    if track_ids_to_remove:
        # Remove tracks in batches of 100
        batch_size = 100
        for i in range(0, len(track_ids_to_remove), batch_size):
            batch = track_ids_to_remove[i:i+batch_size]
            sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)

    # Print the tracks to be kept
    print("\nExplicit tracks to keep:\n")
    for track in tracks_to_keep:
        print(f"{track[0]} by {track[1]}")
    print()