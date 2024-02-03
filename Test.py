import requests
import pandas as pd
import time


# get album details
def get_album_details(track_df, album_id):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
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
    BASE_URL = 'https://api.spotify.com/v1/'

    # pull all tracks from this album
    for album in album_id:
        album_id = album
        r = requests.get(BASE_URL + 'albums/' + album_id + '/tracks',
                         headers=headers)
        d = r.json()
        time.sleep(1)

        i = 0
        for track in d['items']:
            if track['type'] == 'track':
                track_id = d['items'][i]['id']
                track_name = d['items'][i]['name']
                duration_ms = d['items'][i]['duration_ms']
                explicit = d['items'][i]['explicit']

                # save data in pd dataframe
                # track_df = track_df.append({'album_id':album_id,'track_id': track_id,'track_name': track_name,
                #                            'duration_ms': duration_ms,'explicit': explicit},ignore_index=True)
                temp_df = pd.DataFrame({'album_id': album_id, 'track_id': track_id, 'track_name': track_name,
                                        'duration_ms': duration_ms, 'explicit': explicit}, index=[i])
                track_df = pd.concat([track_df, temp_df], ignore_index=True)
            i += 1
    return track_df


def main():
    album_df = pd.read_csv(r'~/Documents/spotify_analysis/test-csvs/album_list.csv')
    album_id = album_df.loc[:, 'album_id']
    track_df = pd.DataFrame(columns=["album_id", "track_id", "track_name", "duration_ms", "explicit"])
    track_df = get_album_details(track_df, album_id)
    track_df.to_csv(r'~/PycharmProjects/spotifyScripts/testCsvs/track_list.csv', encoding='utf-8-sig')
    print('-----------------------------------')
    print('Saved to .csv in project directory.')
    print('-----------------------------------')


if __name__ == "__main__":
    main()
