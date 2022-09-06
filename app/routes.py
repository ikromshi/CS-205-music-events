from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')


@app.route('/artists')
def artists():
  artists = ["John Brown's Body", "Gunpoets", "Donna The Buffalo", "The Blind Spots"]
  return render_template('artists.html',  artists=artists)

@app.route('/artist')
def artist():
  return render_template('artist.html')

@app.route('/new_artist')
def new_artist():
  return render_template('new_artist.html')
