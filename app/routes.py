from datetime import datetime
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import NewArtist
from app.models import Artist, ArtistToEvent, Venue, Event


@app.route("/populate_db")
def populate_db():
  reset_db()

  a1 = Artist(name="Denny", about_me="Musician")
  a2 = Artist(name="Donavan", about_me="Musician")
  a3 = Artist(name="Tyler", about_me="Musician")
  a4 = Artist(name="Drew", about_me="Musician")
  db.session.commit()
  db.session.add_all([a1, a2, a3, a4])

  v1 = Venue(location="Ithaca", size=120)
  v2 = Venue(location="Ithaca", size=200)
  v3 = Venue(location="Cambridge", size=750)
  v4 = Venue(location="NYC", size=150000)
  db.session.commit()
  db.session.add_all([v1, v2, v3, v4])

  e1 = Event(title="Live Music Jam", location="Ithaca Commons", date_time=datetime.datetime(2022, 7, 23, 17, 0, 0),venue_id=1)
  e2 = Event(title="Hip Hop Night", location="local station",date_time=datetime.datetime(2024, 1, 13, 7, 30, 0),venue_id=1)
  e3 = Event(title="Porchfest Again", location="Cambridge Musical Ceremony", date_time=datetime.datetime(2023, 12, 30, 19, 0, 0),venue_id=3)
  e4 = Event(title="Birthday Celebration", location="drive way", date_time=datetime.datetime(2024, 1, 1, 12, 0, 0), venue_id=2)
  db.session.commit()
  db.session.add_all([e1, e2, e3, e4])


@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')


@app.route('/artists')
def artists():
  artists = db.session.query(Artist).all()
  return render_template('artists.html',  artists=artists)


@app.route('/artist/<name>')
def artist(name):
  artist = db.session.query(Artist).filter_by(name=name).first()
  events = db.session.query(Event).join(ArtistToEvent, ArtistToEvent.event_id == Event.id).join(Artist, Artist.id == ArtistToEvent.artist_id).filter(Artist.name == name).all()

  return render_template('artist_page.html', title=name, artist=artist, events=events)


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
  form = NewArtist()
  if form.validate_on_submit():
    # flash('New user created: {}; location: {}'.format(
    #   form.name.data, form.hometown.data))
    return render_template("new_artist.html", form=form, name=form.name.data, hometown=form.hometown.data, description=form.description.data)
  return render_template('new_artist.html', form=form)


def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()

  # now create Artist, Venues, Events, and ArtistToEvent Objects and persist them to the db

