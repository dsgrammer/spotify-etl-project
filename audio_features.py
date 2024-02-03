import requests
import pandas as pd
import time
# import os

# os.environ['AUTH_URL'] = 'https://accounts.spotify.com/api/token'
# os.environ['BASE_URL'] = 'https://api.spotify.com/v1/'


# get track audio features
def get_audio_features(feature_df, track_id):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    BASE_URL = 'https://api.spotify.com/v1/'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': '9cdef0bc741e471385b100af843c28c5',
        'client_secret': 'a0820dd07a3e4d8facb51bb5ed5130a2',
    })
    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']
    # used for authenticating all API calls
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    # pull all tracks from this album
    for track in track_id:
        track_id = track
        r = requests.get(BASE_URL + 'audio-features/' + track_id,
                         headers=headers)
        d = r.json()
        time.sleep(1)

        track_id = d['id']
        danceability = d['danceability']
        energy = d['energy']
        key = d['key']
        loudness = d['loudness']
        mode = d['mode']
        speechiness = d['speechiness']
        acousticness = d['acousticness']
        instrumentalness = d['instrumentalness']
        liveness = d['liveness']
        valence = d['valence']
        tempo = d['tempo']
        time_signature = d['time_signature']

        # save data in pd dataframe
        temp_df = pd.DataFrame({'track_id': track_id, 'danceability': danceability, 'energy': energy,
                                'key': key, 'loudness': loudness, 'mode': mode, 'speechiness': speechiness,
                                'acousticness': acousticness,
                                'instrumentalness': instrumentalness, 'liveness': liveness, 'valence': valence,
                                'tempo': tempo,
                                'time_signature': time_signature}, index=[1])
        feature_df = pd.concat([feature_df, temp_df], ignore_index=True)
    return feature_df


def main():
    # BASE_URL = 'https://api.spotify.com/v1/'
    track_df = pd.read_csv(r'~/PycharmProjects/spotifyScripts/testCsvs/fav_list2.csv')
    track_id = track_df.loc[:, 'track_id']
    feature_df = pd.DataFrame(
        columns=["track_id", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                 "instrumentalness",
                 "liveness", "valence", "tempo", "time_signature"])
    feature_df = get_audio_features(feature_df, track_id)

    feature_df.to_csv(r'~/PycharmProjects/spotifyScripts/testCsvs/audio-features.csv', encoding='utf-8-sig')
    print('-----------------------------------')
    print('Saved to .csv in project directory.')
    print('-----------------------------------')


if __name__ == "__main__":
    main()
