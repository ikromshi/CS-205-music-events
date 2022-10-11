# from datetime import datetime
import datetime
from app import app, db
from app.forms import NewArtist
from app.models import Artist, ArtistToEvent, Venue, Event, User
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm


@app.route("/reset_db")
def reset_db():
  clear_data()

  a1 = Artist(name="Denny", hometown="Ithaca", about_me="Piano perfomer")
  a2 = Artist(name="Donavan", hometown="Ithaca", about_me="Violin player")
  a3 = Artist(name="Tyler", hometown="Ithaca", about_me="Plays drums")
  a4 = Artist(name="Drew", hometown="Ithaca", about_me="Singer/backup dancer")
  a5 = Artist(name="Dusan", hometown="Ithaca", about_me="Choir leader")
  a6 = Artist(name="Chris", hometown="Ithaca", about_me="Opera singer")
  db.session.add_all([a1, a2, a3, a4, a5, a6])
  db.session.commit()


  e1 = Event(title="Live Music Jam", location="Ithaca Commons", date_time=datetime.datetime(2022, 7, 23, 17, 0, 0),venue_id=1)
  e2 = Event(title="Hip Hop Night", location="local station",date_time=datetime.datetime(2024, 1, 13, 7, 30, 0),venue_id=1)
  e3 = Event(title="Porchfest Again", location="Cambridge Musical Ceremony", date_time=datetime.datetime(2023, 12, 30, 19, 0, 0),venue_id=3)
  e4 = Event(title="Birthday Celebration", location="local station", date_time=datetime.datetime(2024, 1, 1, 12, 0, 0), venue_id=2)
  e5 = Event(title="New Year's Eve", location="the big stadium", date_time=datetime.datetime(2023, 12, 30, 19, 0, 0),venue_id=3)
  e6 = Event(title="Thanksgiving concert", location="the big staium", date_time=datetime.datetime(2024, 1, 1, 12, 0, 0), venue_id=2)
  e7 = Event(title="Ikrom's birthday", location="usual place", date_time=datetime.datetime(2023, 12, 30, 19, 0, 0),venue_id=3)
  e8 = Event(title="Birthday Celebration", location="the big stadium", date_time=datetime.datetime(2024, 1, 1, 12, 0, 0), venue_id=2)
  db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8])
  db.session.commit()

  aE1 = ArtistToEvent(artist_id=1, event_id=3)
  aE2 = ArtistToEvent(artist_id=1, event_id=4)
  aE3 = ArtistToEvent(artist_id=2, event_id=6)
  aE4 = ArtistToEvent(artist_id=3, event_id=5)
  aE5 = ArtistToEvent(artist_id=4, event_id=1)
  aE6 = ArtistToEvent(artist_id=5, event_id=8)
  aE7 = ArtistToEvent(artist_id=6, event_id=7)
  db.session.add_all([aE1, aE2, aE3, aE4, aE5, aE6, aE7])  
  db.session.commit()


  v1 = Venue(location="Ithaca", size=120)
  v2 = Venue(location="Ithaca", size=200)
  v3 = Venue(location="Cambridge", size=750)
  v4 = Venue(location="NYC", size=150000)
  db.session.add_all([v1, v2, v3, v4])
  db.session.commit()
  return ""

@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template('index.html')


@login_required
@app.route('/artists')
def artists():
  artists = db.session.query(Artist).all()
  return render_template('artists.html',  artists=artists)


@login_required
@app.route('/artist/<name>')
def artist(name):
  artist = db.session.query(Artist).filter_by(name=name).first()
  events = db.session.query(Event).join(ArtistToEvent, ArtistToEvent.event_id == Event.id).join(Artist, Artist.id == ArtistToEvent.artist_id).filter(Artist.name == name).all()

  return render_template('artist_page.html', title=name, artist=artist, events=events)


@login_required
@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
  form = NewArtist()
  if form.validate_on_submit():
    if (db.session.query(Artist).filter_by(name = form.name.data).first()):
      flash("This artist already exists")
      return render_template('new_artist.html', form = form)
    new_artist = Artist()
    new_artist.set_artist(name=form.name.data, hometown=form.hometown.data, about_me_in=form.about_me.data)
    db.session.add(new_artist)
    db.session.commit()
    artists = db.session.query(Artist).all()

    flash('New Artist Created: {}. '.format(form.name.data))
    return redirect('artists')
  return render_template("new_artist.html", form=form)


def clear_data():
  flash("Resetting database: deleting old data and repopulating with dummy data")
  # clear all data from all tables
  meta = db.metadata
  for table in reversed(meta.sorted_tables):
    print('Clear table {}'.format(table))
    db.session.execute(table.delete())
  db.session.commit()

  # now create Artist, Venues, Events, and ArtistToEvent Objects and persist them to the db


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)
