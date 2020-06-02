#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(30)), nullable=False)
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, unique=False, default=True)
    seeking_description = db.Column(db.String(500))
    show_venue = db.relationship('Show', backref='Venue', lazy=True)
    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.genres} {self.seeking_talent} >'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(30)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, unique=False, default=True)
    seeking_description = db.Column(db.String(500))
    show_artist = db.relationship('Show',cascade="all,delete", backref='Artist', lazy=True)
    def __repr__(self):
       return f'<Artist {self.id} {self.name} {self.city} {self.genres} {self.seeking_talent} >'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    __tabelname__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id", ondelete="CASCADE"))
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id", ondelete="CASCADE"))
    start_time = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
       return f'<Show {self.id}, {self.artist_id}, {self.venue_id}, {self.start_time}>'

    #__used the relationship one to many by wjdan altaleb.

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venues = Venue.query.all()
  
  
  venue_city_and_state = ''
  

  for venue in venues:
    upcoming_shows = venue.query.filter().all()
  
    if venue_city_and_state == venue.city + venue.state:
      
      data[len(data) -1]['venues'].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(upcoming_shows),
      })
    else:
      venue_city_and_state = venue.city + venue.state
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(upcoming_shows),
    }]

      })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  #------
  targted_venue = Venue.query.filter(Venue.name.ilike('%'+ request.form['search_term']+'%'))
  venue_count = len(list(targted_venue))
  response = {
    'count': venue_count,
    'data': targted_venue
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  
  shows = db.session.query(Artist,Show).with_entities(Artist.id,Artist.name,Artist.image_link,Show.start_time).outerjoin(Show).filter(Show.venue_id==venue_id).all()
  artist = Artist.query.filter_by(id=2).all()
 # print(shows)
 # shows = venue.join(show1).join(artist).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in shows:
    data = {
           "artist_id": show[0],
           "artist_name": show[1],
           "artist_image_link": show[2],
           "start_time": format_datetime(str(show[3]))
        }
    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    "website": venue.website,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "past_shows": past_shows,
    
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
   venue = Venue(
     name = request.form['name'],
     city = request.form['city'],
     state = request.form['state'],
     address = request.form['address'],
     phone = request.form['phone'],
     genres = request.form.getlist('genres'),
     facebook_link = request.form['facebook_link'],
     website = request.form['website'],
     seeking_description = request.form['seeking_description'],
     #seeking_talent = request.form['seeking_talent'],


   )    
   db.session.add(venue)
   db.session.commit()
   flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()
  return render_template('pages/home.html') 
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return None


  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  #db.session.query(Artist.name)
  # ab=db.session.query(Artist.name).all()
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data=[]
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name,
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  #------
  targted_artist = Artist.query.filter(Artist.name.ilike('%'+ request.form['search_term']+'%'))
  artist_count = len(list(targted_artist))
  response = {
    'count': artist_count,
    'data': targted_artist
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  shows = db.session.query(Venue,Show).with_entities(Venue.id,Venue.name,Venue.image_link,Show.start_time).outerjoin(Show).filter(Show.artist_id==artist_id).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  for show in shows:
    data = {
          "venue_id": show[0],
          "venue_name": show[1],
          "venue_image_link": show[2],
          "start_time": format_datetime(str(show[3]))
        }

    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "website": artist.website,
    "seeking_talent": artist.seeking_talent,
    "seeking_description": artist.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  artist1 = {
    "id" : artist.id,
    "name" : artist.name,
    "city" : artist.city,
    "state" : artist.state,
    "phone" : artist.phone,
    "genres" : artist.city,
    "image_link" : artist.image_link,
    "facebook_link" : artist.facebook_link,
    "website" : artist.website,
    "seeking_talent" : artist.seeking_talent,
    "seeking_description" : artist.seeking_description,
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist1)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  try:
    
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist. genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
   # artist.seeking_talent = request.form['seeking_talent']
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue= Venue.query.get(venue_id)
  venue = {
        "id" : venue.id,
        "name" : venue.name,
        "city" : venue.city,
        "state" : venue.state,
        "genres" : venue.genres,
        "address" : venue.address,
        "phone" : venue.phone,
        "image_link" : venue.image_link,
        "facebook_link" : venue.facebook_link,
        "website" : venue.website,
        "seeking_talent" : venue.seeking_talent,
        "seeking_description" : venue.seeking_description,
  }
 
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  try:
    venue.name = request.form['name'],
    venue.city = request.form['city'],
    venue.state = request.form['state'],
    venue.address = request.form['address'],
    venue.phone = request.form['phone'],
    venue.genres = request.form.getlist('genres'),
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    #venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  
  finally:
    db.session.close()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
 # art = ArtistForm()
  error = False
  
  try:
   # art = Artist(
   #  name = 'lllll',
   # city = 'ddd',
   # phone = 'ddddd',
   # state = 'dd',
    #genres = 'l',
   # facebook_link = 'l',
   artist = Artist(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    phone = request.form['phone'],
    genres = request.form.getlist('genres'),
    facebook_link = request.form['facebook_link']
  )    
   db.session.add(artist)
   db.session.commit()
   flash('Artist ' + request.form['name'] + ' was successfully listed!')
     #db.session.add(art)
     #db.session.commit()
    
 # art = Artist(name=name,city=city,state=state,phone=phone,genres=genres,facebook_link=facebook_link)
   
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    if error:
     print('not work')
  return render_template('pages/home.html') 

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  shows = db.session.query(Artist).join(Show).join(Venue).with_entities(Venue.id,Venue.name,Artist.id,Artist.name,Artist.image_link,Show.start_time, Show.id).all()

  data1 = []

  for show in shows:
    data = {
        "venue_id": show[0],
        "venue_name": show[1],
        "artist_id": show[2],
        "artist_name": show[3],
        "artist_image_link": show[4],
        "start_time": format_datetime(str(show[5]))
    }
    data1.append(data)

  
  return render_template('pages/shows.html', shows=data1)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  #  venues = Venue.query.all()
  #  for user in users:
  #    print(user.id)
   form = ShowForm()
   return render_template('forms/new_show.html', form=form )

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
   show = Show(
    artist_id = request.form['artist_id'],
    venue_id = request.form['venue_id'],
    start_time = request.form['start_time'],
  )    
   db.session.add(show)
   db.session.commit()
   flash('show ' + request.form['artist_id'] + ' was successfully listed!')

  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['artist_id'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
