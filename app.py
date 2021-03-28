from flask import Flask
import database

app = Flask(__name__)

@app.route('/audio/all')
def all_audios():
	result = {}
	k = []
	data = database.fetchall_audios()
	for audio in data:
		temp_data = {'id':audio[0], 'title':audio[1], 'thumbnail': audio[2], 'url':audio[3], 'description':audio[4], 'playlist_id':audio[5]}
		k.append(temp_data)
	result = {'result':k}
	return result

if __name__ == "__main__":
	app.run(debug=True)
