import webbrowser
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from configparser import ConfigParser
from pytube import YouTube

def playlist(url):
	query = parse_qs(urlparse(url).query, keep_blank_values=True)
	playlist_id = query["list"][0]
	parser = ConfigParser()
	parser.read('config.py')
	youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = parser.get('creds', 'token'))
	request = youtube.playlistItems().list(
	    part = "snippet",
	    playlistId = playlist_id,
	    maxResults = 50
	)
	response = request.execute()
	playlist_items = []
	while request is not None:
	    response = request.execute()
	    playlist_items += response["items"]
	    request = youtube.playlistItems().list_next(request, response)
	return [ f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'for t in playlist_items]

def audio(link):
	video = YouTube(link)
	return video.streams.filter(type='audio').first().url

def produce_audio(url):
	url_list = playlist(url)
	print(len(url_list))
	for ul in url_list[:4]:
		webbrowser.open(audio(ul))
produce_audio('https://www.youtube.com/playlist?list=PLQltO7RlbjPJnbfHLsFJWP-DYnWPugUZ7')
