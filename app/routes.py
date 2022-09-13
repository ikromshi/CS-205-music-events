from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import NewArtist


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

@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
  form = NewArtist()
  if form.validate_on_submit():
    # flash('New user created: {}; location: {}'.format(
    #   form.name.data, form.hometown.data))
    return render_template("new_artist.html", form=form, name=form.name.data, hometown=form.hometown.data, description=form.description.data)
  return render_template('new_artist.html', form=form)
