from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    hometown = db.Column(db.String(64), index=True)
    about_me = db.Column(db.String(140))

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_artist(self, name, hometown, about_me_in):
        self.name = name
        self.hometown = hometown
        self.about_me = about_me_in


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    size = db.Column(db.Integer, index=True)
    events = db.relationship("Event", backref="venue", lazy="dynamic")

    def __init__(self, name, location, size):
        self.name = name
        self.location = location
        self.size = size


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    date_time = db.Column(db.DateTime, index=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))

    def __repr__(self):
        return '<Event {}>'.format(self.title)

    def __init__(self, title, date_time, location, venue_id):
        self.title = title
        self.date_time = date_time
        self.location = location
        self.venue_id = venue_id


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))

    def __repr__(self):
        return '<ArtistToEvent {}>'.format(self.id)

    def __init__(self, event_id, artist_id):
        self.event_id = event_id
        self.artist_id = artist_id


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
