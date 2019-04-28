#!/usr/bin/env python3
'''
main.py

Core Flask logic for the Nightlife application
'''

# Python libraries (note: these dependencies are handled through Docker, your local machine may not have these.)
import json, os, operator, datetime
#from utils import *
from flask import Flask, request, redirect, url_for, flash, abort, jsonify, render_template, session
#from models import db, Event, Review
#from forms import NewEventForm
import flask
from pymongo import MongoClient

# Establish flask application on startup
app = flask.Flask(__name__, static_folder="../static", template_folder="../templates")



# Establish database at run time
# Get the MongoDB client

#client = MongoClient('mongodb://dontspoilendgame:thanos123@cluster0-spqqu.mongodb.net')
client = MongoClient('mongodb://dontspoilendgame:thanos123@cluster0-shard-00-00-spqqu.mongodb.net:27017,cluster0-shard-00-01-spqqu.mongodb.net:27017,cluster0-shard-00-02-spqqu.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')

# Get the MongoDB database we are using
db = client.homelessData

# Get the MongoDB database collection we are using
# data = db.hmis
data = db.test
data_out = db.test_out

class CreateDictionary:
    """
    A class that creates a dictionary with set keys initialized to None. Provides an easy and streamlined way to create a
    dictionary that is in the correct format to be used to search in the MongoDB database.
    """
    def __init__(self, gender=None, age=None, veteran=None, disabled=None, pets=None, family=None, food=None, beds=None, clinic=None):
        self.gender = gender
        self.age = age
        self.veteran = veteran
        self.disabled = disabled
        self.pets = pets
        self.family = family
        self.food = food
        self.beds = beds
        self.clinic = clinic
        self.current_dict = {"Gender": self.gender, "Age": self.age, "Veteran": self.veteran, "Disabled": self.disabled, "Pets": self.pets, "Family": self.family, "Food": self.food, "Beds": self.beds, "Clinic": self.clinic}
        print("Current_dict = " + str(self.current_dict))

    def __repr__(self):
        # How the object will be printed
        return '{}'.format(self.current_dict)

    def update_dictionary(self):
        # Update the dictionary in order to get rid of empty string and 'N/A' values and keys from the webpage
        for k, v in list(self.current_dict.items()):
            if v == None:
                del self.current_dict[k]

    def add_val(self, key, value):
        self.current_dict[key] = value

    def get_dictionary(self):
        # Return the dictionary in the format to search the database
        return self.current_dict

@app.route("/")
@app.route("/about", methods=['POST', 'GET'])
def aboutForm():
    return flask.render_template("about.html")

@app.route("/index", methods=['POST', 'GET'])
def index():
    """
    The default page which is a search page that allows the client to send various amounts of information
    to the server in order to check whether or not the requested resource is in the database. Redirects to
    the results page with the specified parameters.
    """
    print("entering aboutForm")
    # Request the information from the webpage that the user entered/selected
    gender = flask.request.form.get("gender")
    age = flask.request.form.get("age")
    veteran = flask.request.form.get("veteran")
    disabled = flask.request.form.get("disabled")
    pets = flask.request.form.get("pets")
    family = flask.request.form.get("family")
    diction = CreateDictionary(gender, age, veteran, disabled, pets, family)
    # Update the dictionary to get rid of any values and keys that weren't entered
    #diction.update_dictionary()
    flask.session["current_dict"] = diction.get_dictionary()
    print("update_dictionary = " + str(diction))
    # data_list = []
    # # Search the database for data that matches the new dictionary
    # for i in data.find(diction.get_dictionary()):
    #     # Append any found database entries into an empty list
    #     data_list.append(i)
    # print(data_list)
    return flask.render_template("index.html")

def formatBed(my_list):
    '''
    Formats the list into a usable form for the HTML
    '''
    flask.g.results = []
    flask.g.empty = False

    count = 0
    for i in my_list:
        flask.g.results.append({"Restrictions":[]})
        flask.g.results[count]['Name'] = ""
        if ("Gender" in i and i['Gender'] == "F"):
            flask.g.results[count]['Restrictions'].append('female.png')
        if ("Veteran" in i and i['Veteran'] == "Y"):
            flask.g.results[count]['Restrictions'].append('veteran.png')
        if ("Disabled" in i and i['Disabled'] == "Y"):
            flask.g.results[count]['Restrictions'].append('disabled.png')
        if ("Beds" in i and i['Beds'] != "N"):
            flask.g.results[count]['Name'] = str("(" + str(i['Beds']) + ") beds open at ")
        else:
            del flask.g.results[count]
            continue
        if ("Name" in i):
            if (len(i["Name"]) > 36):
                flask.g.results[count]['Name'] += str(i["Name"][:36] + "...")
            elif (len(i["Name"]) > 0 and flask.g.results[count]['Name'] != ""):
                flask.g.results[count]['Name'] += str(i["Name"])
            else:
                flask.g.results[count]['Name'] = str(i["Name"])
        if ("Address" in i and i['Address'] != None):
            flask.g.results[count]['Address'] = i["Address"]
        if ("Phone" in i and i['Phone'] != None):
            flask.g.results[count]['Phone'] = i["Phone"]

        if len(flask.g.results[count]["Restrictions"]) == 0: #Check if there are any reservations on who can use this clinic
            flask.g.results[count]["Restrictions"].append(True)
        count += 1

    if len(flask.g.results) == 0:
        flask.g.empty = True


def formatFood(my_list):
    flask.g.results = []
    flask.g.empty = False
    count = 0
    for i in my_list:
        flask.g.results.append({"Restrictions":[]})
        if ("Gender" in i and i['Gender'] == "F"):
            flask.g.results[count]['Restrictions'].append('female.png')
        if ("Veteran" in i and i['Veteran'] == "Y"):
            flask.g.results[count]['Restrictions'].append('veteran.png')
        if ("Disabled" in i and i['Disabled'] == "Y"):
            flask.g.results[count]['Restrictions'].append('disabled.png')
        if ("Food" in i and i["Food"] == "N"):
            del flask.g.results[count]
            continue
        if ("Name" in i and i['Name'] != None):
            if (len(i["Name"]) > 36):
                flask.g.results[count]["Name"] = str(i["Name"][:36] + "...")
            else:
                flask.g.results[count]['Name'] = str(i["Name"])
        if ("Address" in i and i['Address'] != None):
            flask.g.results[count]['Address'] = i["Address"]
        if ("Phone" in i and i['Phone'] != None):
            flask.g.results[count]['Phone'] = i["Phone"]

        if len(flask.g.results[count]["Restrictions"]) == 0: #Check if there are any reservations on who can use this clinic
            flask.g.results[count]["Restrictions"].append(True)
        count += 1

    if len(flask.g.results) == 0:
        flask.g.empty = True

def formatClinics(my_list):
    flask.g.results = []
    flask.g.empty = False;
    count = 0
    for i in my_list:
        flask.g.results.append({"Restrictions":[]})
        if ("Gender" in i and i['Gender'] == "F"):
            flask.g.results[count]['Restrictions'].append('female.png')
        if ("Veteran" in i and i['Veteran'] == "Y"):
            flask.g.results[count]['Restrictions'].append('veteran.png')
        if ("Disabled" in i and i['Disabled'] == "Y"):
            flask.g.results[count]['Restrictions'].append('disabled.png')
        if ("Clinic" in i and i["Clinic"] == "N"):
            del flask.g.results[count]
            continue
        if ("Name" in i and i['Name'] != None):
            if (len(i["Name"]) > 36):
                flask.g.results[count]["Name"] = str(i["Name"][:36] + "...")
            else:
                flask.g.results[count]['Name'] = str(i["Name"])
        if ("Address" in i and i['Address'] != None):
            flask.g.results[count]['Address'] = i["Address"]
        if ("Phone" in i and i['Phone'] != None):
            flask.g.results[count]['Phone'] = i["Phone"]
        if len(flask.g.results[count]["Restrictions"]) == 0: #Check if there are any reservations on who can use this clinic
            flask.g.results[count]["Restrictions"].append(True)
        count += 1

    if len(flask.g.results) == 0:
        flask.g.empty = True

@app.route("/search", methods=['POST'])
def search():
    '''
    Checks through the session dictionary to make sure we are passing it the values that need to be
    displayed on the HTML page.
    '''
    button = flask.request.form.get("sub")
    data_list = []
    out_dict = flask.session["current_dict"].copy()
    out_dict["Service"] = button
    out_dict["Time"] = str(datetime.datetime.now())
    x = data_out.insert_one(out_dict)
    for key, value in list(flask.session["current_dict"].items()):
        if (key == "Veteran" and value == "Y"):
            del flask.session["current_dict"]['Veteran']
        if (key == "Disabled" and value == "Y"):
            del flask.session["current_dict"]['Disabled']
        if (key == "Pets" and value == "N"):
            del flask.session["current_dict"]['Pets']
        if (key == "Family" and value == "Y"):
            del flask.session["current_dict"]['Family']
        if (key == "Gender" and value == "F"):
            del flask.session["current_dict"]['Gender']
        if (key == "Age" and value == "Y"):
            del flask.session["current_dict"]['Age']
    for k, v in list(flask.session["current_dict"].items()):
            if v == None:
                del flask.session["current_dict"][k]
    for i in data.find(flask.session["current_dict"]):
        data_list.append(i)
    if (button == "beds"):
        flask.g.request = "Bedding"
        formatBed(data_list)
        return flask.render_template("userselection.html")
    elif (button == "food"):
        flask.g.request = "Food"
        formatFood(data_list)
        return flask.render_template("userselection.html")
    elif (button == "clinic"):
        flask.g.request = "Clinic"
        formatClinics(data_list)
        return flask.render_template("userselection.html")
    return flask.render_template("userselection.html")



@app.route("/ees", methods=['GET'])
def eesMap():
    return flask.render_template("ees.html")

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

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
