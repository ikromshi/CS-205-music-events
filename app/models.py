from app import db
from datetime import datetime


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    about_me = db.Column(db.String(140))
    events = db.relationship("ArtistToEvent", backref="artists", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_artist(self, name, about_me_in):
        self.name = name
        self.about_me = about_me_in


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True)
    size = db.Column(db.Integer, index=True)
    events = db.relationship("Event", backref="venue", lazy="dynamic")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    date_time = db.Column(db.DateTime, index=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
    artists = db.relationship("ArtistToEvent", backref="events", lazy="dynamic")


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
