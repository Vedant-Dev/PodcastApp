import webbrowser
import secrets 
import string
import database
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from configparser import ConfigParser
from pytube import YouTube

# class Audio:
# 	def __init__(self, rowid=None,id=None, title=None, thumbnail=None, url=None, description=None):
# 		self.rowid = rowid
# 		self.id = id
# 		self.title = title
# 		self.thumbnail = thumbnail
# 		self.url = url
# 		self.description = description

def fetch_playlist(url): #returns list of tuples of Youtube playlist in form of tuple(id, title, url, description)
	#Reading configration file
	parser = ConfigParser()
	parser.read('config.py')#Replace "config.py" with your configration file with following formated file name
	'''
	[creds]
	token =  <YOUR TOKEN>
	'''
	#Reading Google's Youtube Data API v3
	query = parse_qs(urlparse(url).query, keep_blank_values=True)
	playlist_id = query["list"][0]
	youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = parser.get('creds', 'token'))
	request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,maxResults = 50)
	response = request.execute()
	playlist_items = []
	while request is not None:
	    response = request.execute()
	    playlist_items += response["items"]
	    request = youtube.playlistItems().list_next(request, response)
	return [(give_random_id(),t['snippet']['title'],t['snippet']['thumbnails']['medium']['url'],
			audio_url(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'),t['snippet']['description'])
			for t in playlist_items]
def audio_url(link): #Returns Audio URL for Youtube Video
	video = YouTube(link)
	return video.streams.filter(type='audio').first().url
def add_youtube_playlist_to_database(playlistId):#Adding Youtube Playlist to Database
	list = fetch_playlist(playlistId)
	database.addmany(list)
def add_youtube_video_to_database(url):#Adding Youtube Video to Database
	yt = YouTube(url)
	video = (give_random_id(), yt.title, yt.thumbnail_url,video.streams.filter(type='audio').first().url,yt.description)
	database.addmany([video,])
def add_audio_book(title, thumbnail, url, description):#Adding hardcoded audio to Database 
	random_token = give_random_id()
	video = (random_token, title, thumbnail, url, description)
def give_random_id():#Generates random id in following format eg. d2457
	alphabet = string.ascii_lowercase + string.digits 
	result = secrets.choice(string.ascii_lowercase) + (''.join(secrets.choice(string.digits) for i in range(3)))
	return result