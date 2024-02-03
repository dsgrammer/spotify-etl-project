import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os


os.environ['SPOTIPY_CLIENT_ID'] = '9cdef0bc741e471385b100af843c28c5'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'a0820dd07a3e4d8facb51bb5ed5130a2'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'


# Function for getting all the user's saved (favorite) tracks
def get_all_saved_tracks(fav_df, user, limit_step=50):
    for offset in range(0, 10000000000000000000000, limit_step):
        r = user.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )
        # print(r)
        for idx, item in enumerate(r['items']):
            d = item['track']
            band_id = d['artists'][0]['id']
            band_name = d['artists'][0]['name']
            album_name = d['album']['name']
            release_date = d['album']['release_date']
            total_tracks = d['album']['total_tracks']
            album_id = d['album']['id']
            track_id = d['id']
            track_name = d['name']
            duration_ms = d['duration_ms']
            explicit = d['explicit']
            added_at = item['added_at']

            temp_df = pd.DataFrame({'artist_id': band_id, 'artist_name': band_name, 'album_name': album_name,
                                    'album_release_date': release_date,
                                    'album_total_tracks': total_tracks, 'album_id': album_id, 'track_id': track_id,
                                    'track_name': track_name, 'duration_ms': duration_ms,
                                    'explicit': explicit, 'added_at': added_at}, index=['added_at'])

            # For concat(), need to explicitly caste boolean/datetime values as boolean and datetime
            temp_df['explicit'] = temp_df['explicit'].astype('boolean')
            # temp_df['added_at'] = temp_df['added_at'].astype('datetime64')
            temp_df['added_at'] = temp_df['added_at'].apply(pd.to_datetime)

            fav_df = pd.concat([fav_df, temp_df], ignore_index=True)

        if offset > int(r['total']):
            break

    return fav_df


def main():
    fav_df = pd.DataFrame(columns=["artist_id", "artist_name", "album_id", "album_name", "album_release_date",
                                   "album_total_tracks", "track_id", "track_name", "duration_ms", "explicit",
                                   "added_at"])

    # Set token and login credentials
    # URL to all scopes available
    # https://developer.spotify.com/documentation/web-api/concepts/scopes
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    user = sp

    # Get all user saved (favorite) tracks
    fav_df = get_all_saved_tracks(fav_df, user)

    fav_df.to_csv(r'~/PycharmProjects/spotifyScripts/testCsvs/fav_list2.csv', encoding='utf-8-sig')
    print('-----------------------------------')
    print('Saved to .csv in project directory.')
    print('-----------------------------------')
    print(fav_df.head())


if __name__ == "__main__":
    main()
