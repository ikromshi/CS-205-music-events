from app import app, db
from app.models import Artist, Venue, Event, User

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Artist': Artist, 'Venue': Venue, 'Event': Event}