from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import NewArtist
from app.models import Artist, Venue, Event


@app.route("/populate_db")
def populate_db():
  u1 = Artist(first_name="Doug", last_name="Turnbull", about_me="Professor")
  u2 = Artist(first_name="Toby", last_name="Dragon", about_me="Professor")
  u3 = Artist(first_name="John", last_name="Barr", about_me="Professor")
  db.session.add_all([u1, u2, u3])
  db.session.commit()


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
