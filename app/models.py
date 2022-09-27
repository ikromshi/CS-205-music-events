from app import db
from datetime import datetime


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    about_me = db.Column(db.String(140))
    song_to_art = db.relationship("SongToArtist", backref="artist", lazy="dynamic")
    events = db.relationship("ArtistToEvent", backref="artists", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.first_name)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True)
    size = db.Column(db.Integer, index=True)
    events = db.relationship("Event", backref="location", lazy="dynamic")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
    artists = db.relationship("ArtistToEvent", backref="events", lazy="dynamic")


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    song_to_art = db.relationship("SongToArtist", backref="song", lazy="dynamic")


class SongToArtist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"))