import secrets 
import string
import database
from pytube import YouTube
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from configparser import ConfigParser

def fetch_playlist(url,playlist_id):	
	parser = ConfigParser()
	parser.read('config.py')
	youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = parser.get('creds', 'token'))
	request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,maxResults = 50)
	response = request.execute()
	playlist_items = []
	while request is not None:
	    response = request.execute()
	    playlist_items += response["items"]
	    request = youtube.playlistItems().list_next(request, response)
	return [(give_random_id(),t['snippet']['title'],t['snippet']['thumbnails']['medium']['url'],
			audio_url(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'),t['snippet']['description'],playlist_id)
			for t in playlist_items]
def audio_url(link):
	video = YouTube(link)
	return video.streams.filter(type='audio').first().url
def add_youtube_playlist_to_database(url ,title, thumbnail):
	query = parse_qs(urlparse(url).query, keep_blank_values=True)
	playlist_id = query["list"][0]
	database.add_playlist([(playlist_id,title, thumbnail)])
	result = fetch_playlist(url,playlist_id)
	database.add(result)
def add_youtube_video_to_database(url):
	yt = YouTube(url)
	video = (give_random_id(), yt.title, yt.thumbnail_url,video.streams.filter(type='audio').first().url,yt.description)
	database.add([video,])
def add_audio_book(title, thumbnail, url, description): 
	random_token = give_random_id()
	video = (random_token, title, thumbnail, url, description)
def give_random_id():
	alphabet = string.ascii_lowercase + string.digits 
	result = secrets.choice(string.ascii_lowercase) + (''.join(secrets.choice(string.digits) for i in range(3)))
	return result
