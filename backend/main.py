'''
main.py

Core Flask logic for the Nightlife application
'''

# Python libraries (note: these dependencies are handled through Docker, your local machine may not have these.)
import json, os, operator
from utils import *
from flask import Flask, request, redirect, url_for, flash, abort, jsonify, render_template
from models import db, Event, Review
from forms import NewEventForm
import flask
from pymongo import MongoClient

# Establish flask application on startup
app = flask.Flask(__name__, static_folder="static", template_folder="templates")



# Establish database at run time
# Get the MongoDB client

client = MongoClient('mongodb+srv://dontspoilendgame:thanos123@cluster0-spqqu.mongodb.net/test')

# Get the MongoDB database we are using
db = client.homelessData

# Get the MongoDB database collection we are using
orgs = db.hmis

@app.route("/")
@app.route("/index")


# def get_rating(party_id):
#    '''
#    Helper function used to get the average rating from the Rating model given a party id.

#    Input:
#        party_id: int, id of event
#    Returns:
#        rating: float
#    '''
#    result = db.session.query(db.func.avg(Review.rating).label('average')).filter(Review.party_id==party_id)
#    return result[0][0]


# @app.route("/api/healthcheck", methods=['GET'])
# def healthcheck():
#    '''
#    API endpoint to check system health. 
#    NOT used by end-users, for developer access only.

#    Input:
#        N/A, Endpoint decorator
#    Returns:
#        Flask response object (JSON load)
#    '''
#    return jsonify({ 'data': 'System is up and running' })

# @app.route("/api/reset_db", methods=['GET'])
# def reset_db():
#    '''
#    API endpoint to reset database tables (equivalent to an SQL drop/create or truncate)
#    NOT used by end-users, for developer access only.

#    Input:
#        N/A, Endpoint decorator
#    Effects:
#        Resets database
#    Returns:
#        Flask response object (JSON load), HTTP response code
#    '''
#    try:
#        db.drop_all()
#        db.create_all()
#        response = jsonify({ 'message': 'Successfully reset db' })
#        response.status_code = 200
#    except:
#        response = jsonify({ 'message': 'Reset db failed check output' })
#        response.status_code = 400
#    return response

# @app.route("/api/event/gen_events/<int:n>", methods=['GET'])
# def gen_events(n):
#    '''
#    API endpoint used to generate test-events in the run-time system. Generates "fake" events with random information.
#    NOT used by end-users, for developer access only.

#    Input:
#        n: int, number of test events to generate
#    Effects:
#        Generates database entries
#    Returns:
#        Flask response object (JSON load), HTTP response code
#    '''
#    event_list = generate_test_events(n)
#    for e in event_list:
#        db.session.add(e)
#    db.session.commit()
#    response = jsonify({ 'message': 'success' })
#    response.status_code = 200
#    return response

# @app.route("/api/event/gen_campus_events/<int:n>", methods=['GET'])
# def gen_campus_events(n):
#    event_list = generate_campus_test_events(n)
#    for e in event_list:
#        db.session.add(e)
#    db.session.commit()
#    response = jsonify({ 'message': 'success' })
#    response.status_code = 200
#    return response

# @app.route("/api/event/<int:id>", methods=['GET'])
# def get_event(id):
#    '''
#    API endpoint used to get JSON data about a single event given its ID.
#    Depreciated, soley developer use. NOT for end-users.

#    Input:
#        id: int, event id
#    Returns:
#        Flask response object (JSON load), HTTP response code
#    '''
#    event = Event.query.get(id)
#    if event is None:
#        response = jsonify({'message': 'invalid event ID'})
#        response.status_code = 400
#        return response

#    event_dict = event_to_dict(event)
#    event_dict['rating'] = get_rating(id)
#    response = jsonify(event_dict)
#    response.status_code = 200
#    return response


# @app.route("/api/event/all", methods=['GET'])
# def get_all():
#    '''
#    API endpoint used by view.html and top-parties.html to get event JSON data.
#    Creates JSON dict of all events, and their average ratings. This payload is then returned to the front-end through an AJAX call.

#    Input:
#        id: int, event id
#    Returns:
#        Flask response object (JSON load), HTTP response code
#    '''
#    all_events = Event.query.all()
#    json_list = []
#    for row in all_events:
#        event_dict = event_to_dict(row)

#        if get_rating(row.id) == None: event_dict['rating'] = 0 # Sentinel value, if the event has no ratings, we give it an average rating of 0, which displays a value of "no ratings" on the front-end
#        else: event_dict['rating'] = get_rating(row.id)

#        json_list.append(event_dict)

#    json_list.sort(key=operator.itemgetter('rating'), reverse=True) # Sort JSON dict by the average event rating

#    response = jsonify({'events':json_list})
#    response.status_code = 200

#    return response

# @app.route("/api/event/create", methods=['POST','PUT'])
# def create_event():
#    '''
#    API Endpoint to create an event for a host. Sent via POST request.
#    Uses WTForm validation to validate event data.

#    Input:
#        N/A, Endpoint decorator
#    Effects:
#        Inserts Event row (upon success)
#    Returns:
#        - Page redirection [upon success]
#        - Flask response object (JSON load), HTTP response code [upon failure]
#    '''

#    form = NewEventForm(request.form)

#    # Form submission from the user

#    if request.method == 'POST' or request.method == 'PUT':

#        if form.validate(): # WTForm validation

#            eprint("Form successfully validated")

#            name = form.eventNameInput.data
#            host = form.eventHostInput.data
#            theme = form.eventThemeInput.data
#            description = form.eventDescriptionInput.data
#            time_start = form.eventStartTimeEntry.data
#            time_end = form.eventEndTimeEntry.data
#            street = form.eventAddressInput.data
#            city = form.eventCityInput.data
#            state = form.eventStateInput.data
#            zipcode = form.eventZipInput.data
           
#            address = "{}, {}, {} {}".format(street, city, state, zipcode)
#            eprint("POST address: " + address)
#            geo_tuple = geocode(address)  # GMS Geocoding using the form address
#            eprint(geo_tuple)
           

#            # Creating a geometric point which can be displayed on google maps
#            lat = geo_tuple[0]
#            lng = geo_tuple[1]
#            new_event = Event(name=name, geo='POINT({} {})'.format(lat, lng), lat=lat, lng=lng, address=address, host=host, theme=theme, description=description, time_start=time_start, time_end=time_end)


#            # Inserting event into the database

#            db.session.add(new_event)
#            db.session.commit()

#            response = jsonify({ 'message': 'validation/upload success' })
#            response.status_code = 200
#            return redirect('/')
       
       
#        # Form validation failure, return JSON response

#        else:
#            eprint(form.errors)
#            response = jsonify({'validation failed': form.errors})
#            response.status_code = 400
#        return response

# @app.route("/api/event/add_rating", methods=['POST'])
# def add_rating():
#    '''
#    API endpoint to add a rating from user input on the view.html page
#    This is accessed when a user clicks "submit rating" after selecting the range slider on a party infowindow.

#    Input:
#        N/A, Endpoint decorator
#    Effects:
#        Inserts rating row
#    Returns:
#        HTML redirect
#    '''

#    rating = request.form['partyRatingSlider']
#    eventId = request.form['eventId']

#    r1 = Review(party_id=eventId, rating=rating)
#    db.session.add(r1)
#    db.session.commit()

#    return redirect('index.html')