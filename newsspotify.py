# import libraries
import spotipy
import webbrowser
import json
import urllib.request
import geocoder
from nltk.corpus import stopwords
import spotipy.util as util
import random

# the variable key now contains my API key
with open("news_key.txt", "r") as file:
    key = file.read()

# this is the url for the news api
url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + key

# request is when im asking for data
request = urllib.request.Request(url)
# response is the answer i get for asking for data
response = urllib.request.urlopen(request)

# converting the HTTPResponse object to a python dictionary
headlines = json.loads(response.read())

# make an empty list of my titles
article_titles = []
for headline in headlines['articles']:
    article_titles.append(headline['title'])

list_of_words = []
# go through each title
for title in article_titles:
    # go through each word
    for word in title.lower().split(" "):
        # is the word not a stopword?
        # is the word not a number?
        if word not in stopwords.words('english') and word.isalpha():
            list_of_words.append(word)

credentials = "spotify_keys.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)

client_id = api_tokens["client_id"]
client_secret = api_tokens["client_secret"]
redirectURI = api_tokens["redirect"]
username = api_tokens["username"]

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-library-read'
token = util.prompt_for_user_token(username, scope, client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)


# start a list of songs for my headline playlist
songs_for_playlist = []
# have for loop run 50 times
for keyword in range(48):
    # pick a random keyword
    new_keyword = random.choice(list_of_words)
    # search for artists based on my keyword, only give me one artist
    searchResults = sp.search(q="artist:" + new_keyword, type="track", limit=1)
    # if the search returns anything
    if len(searchResults['tracks']['items']) > 0:
        songs_for_playlist.append(searchResults['tracks']['items'][0]['uri'])
    
searchResults = sp.search(q="artist:" + "dylan", type="track", limit=1)
searchResults['tracks']['items'][0]['uri']

my_playlist = sp.user_playlist_create(user=username, name="Todays News", public=True,
                                      description="Songs for the news")
results = sp.user_playlist_add_tracks(username, my_playlist['id'], songs_for_playlist)
print(results)

webbrowser.open(my_playlist['external_urls']['spotify'])