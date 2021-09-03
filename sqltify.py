#!/usr/bin/env python3

import os
import requests
import sqlite3
import sys
import time

SAVED_TRACKS_URL = 'https://api.spotify.com/v1/me/tracks'
TOKEN = os.environ['SPOTIFY_TOKEN']

def get_my_tracks(token):
    with requests.Session() as s:
        url = SAVED_TRACKS_URL

        while url:
            res = s.request('GET', url, headers={'Authorization': f'Bearer {token}'})
            if res.status_code == 429:
                time.sleep(int(res.headers['Retry-After']))
                continue
            elif res.status_code != 200:
                raise Exception('request failed', res.status_code, res.json())
            body = res.json()
            yield from body['items']
            url = body['next']

def write_database(filename, tracks):
    con = sqlite3.connect(filename)
    cur = con.cursor()

    cur.execute('PRAGMA foreign_keys = 1')
    cur.execute('''CREATE TABLE track (
                id TEXT PRIMARY KEY,
                title TEXT,
                album TEXT,
                added TEXT,
                duration_ms INTEGER
            )''')
    cur.execute('''CREATE TABLE artist (
                id TEXT PRIMARY KEY,
                name TEXT
            )''')
    cur.execute('''CREATE TABLE artistry (
            track_id TEXT,
            artist_id TEXT,
            FOREIGN KEY (track_id) REFERENCES track(id),
            FOREIGN KEY (artist_id) REFERENCES artist(id)
        )''')

    for t in tracks:
        cur.execute('INSERT INTO track VALUES (?, ?, ?, ?, ?)', (t['track']['id'], t['track']['name'], t['track']['album']['name'], t['added_at'], t['track']['duration_ms']))
        cur.executemany('INSERT OR IGNORE INTO artist VALUES (?, ?)', ((a['id'], a['name']) for a in t['track']['artists']))
        cur.executemany('INSERT INTO artistry VALUES (?, ?)', ((t['track']['id'], a['id']) for a in t['track']['artists']))

    con.commit()
    con.close()

if __name__ == '__main__':
    write_database('sqltify.db', get_my_tracks(TOKEN))
