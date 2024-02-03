import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import os


os.environ['SPOTIPY_CLIENT_ID'] = '9cdef0bc741e471385b100af843c28c5'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'a0820dd07a3e4d8facb51bb5ed5130a2'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'


def connection():
    scope = ['user-library-read', 'user-read-recently-played']
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    user = sp

    return user


def get_recently_played(rpl_df, user):
    recent_tracks = user.current_user_recently_played(limit=50)

    for idx, item in enumerate(recent_tracks['items']):
        d = item["track"]
        track_id = d['id']
        track_name = d['name']
        duration_ms = d['duration_ms']
        explicit = d['explicit']
        played_at = item['played_at']

        temp_df = pd.DataFrame({'track_id': track_id, 'track_name': track_name, 'duration_ms': duration_ms,
                                'explicit': explicit, 'played_at': played_at}, index=['played_at'])
        temp_df['explicit'] = temp_df['explicit'].astype('boolean')
        temp_df['played_at'] = temp_df['played_at'].apply(pd.to_datetime)

        rpl_df = pd.concat([rpl_df, temp_df], ignore_index=True)

    return rpl_df


def main():
    rpl_df = pd.DataFrame(columns=["track_id", "track_name", "duration_ms", "explicit", "played_at"])

    user = connection()
    rpl_df = get_recently_played(rpl_df, user)

    rpl_df.to_csv(r'~/PycharmProjects/spotifyScripts/testCsvs/recently_played.csv', encoding='utf-8-sig')
    print('-----------------------------------')
    print('Saved to .csv in project directory.')
    print('-----------------------------------')
    print(rpl_df.head())


if __name__ == "__main__":
    main()
