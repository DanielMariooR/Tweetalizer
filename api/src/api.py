from flask import Flask, flash, redirect, request, jsonify, session
from analyze import pipeline
from flask_cors import CORS
from searchtweets import load_credentials

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'qghVT3f6pMNjCJVzpHjE'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/home', methods=['POST'])
def home():
	topic = ""
	if(request.method == 'POST'):
		data = request.get_json(force=True)
		topic = data['topic']
		session['topic'] = str(topic)
		return redirect('/result')
	return jsonify({})


@app.route('/result', methods=['GET'])
def result():
	topic = session['topic']
	result = pipeline(str(topic))
	pos = result[0]
	neg = result[1]
	return jsonify({'positive':pos, 'negative': neg})




