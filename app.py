from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from flask import request

from model import Session, Toilet, OpeningHours
from schemas import *

from datetime import datetime


info = Info(title="ToiGet Toilets API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentation", description="Swagger Documentation")
toilet_tag = Tag(name="Toilet", description="Insert, update, view and delete toilets")


@app.get('/', tags=[home_tag])
def home():
    """ Redirects to /openapi/swagger - Swagger Documentation
    """
    return redirect('/openapi/swagger')


@app.post('/toilet', tags=[toilet_tag],
          responses={"200": ToiletViewSchema, "409": ErrorSchema, "400": ErrorSchema, "422": ErrorSchema})
def add_toilet(form: ToiletSchema):
    """ Insert a toilet

    Returns toilet and opening hours.
    """

    toilet = Toilet(
        latitude=form.latitude,
        longitude=form.longitude,
        classification=form.classification,
        description=form.description,
        toiletType=form.toiletType,
        user=form.user)
    
    openingHoursList = []
    for openingHour in form.openingHours:
        openingHour = OpeningHours(
            weekday=openingHour.weekday,
            openClosed=openingHour.openClosed,
            openingTime=openingHour.openingTime,
            closingTime=openingHour.closingTime)
        openingHoursList.append(openingHour)

    try:
        session = Session()
        # add opening hours to toilet
        for h in openingHoursList:
            toilet.openingHours.append(h)
        # add a toilet
        session.add(toilet)
        session.commit()
        return show_toilet(toilet, toilet.openingHours, session), 200
    
    except IntegrityError as e:
        error_msg = Toilet.Toilet_Error(str(e.orig))
        return {"message": error_msg}, 409

    except Exception as e:
        # Unexpected error
        print(e)
        error_msg = "Unexpected error."
        return {"message": error_msg}, 400


@app.post('/toiletEdit', tags=[toilet_tag],
          responses={"200": ToiletViewSchema, "409": ErrorSchema, "400": ErrorSchema, "422": ErrorSchema})
def update_toilet(form: ToiletSchema):
    """ Update a toilet

    Returns toilet and opening hours.
    """
    toilet = Toilet(
        latitude=form.latitude,
        longitude=form.longitude,
        classification=form.classification,
        description=form.description,
        toiletType=form.toiletType,
        user=form.user)

    # add opening hours to toilet
    toilet.openingHours = []
    for h in form.openingHours:
        openingHour = OpeningHours(
            weekday=h.weekday,
            openClosed=h.openClosed,
            openingTime=h.openingTime,
            closingTime=h.closingTime)
        toilet.openingHours.append(openingHour)
    
    try:
        session = Session()
        # delete old record
        toilet_old = session.query(Toilet).filter(Toilet.latitude == toilet.latitude,
                                                  Toilet.longitude == toilet.longitude).first()
        count1 = session.query(Toilet).filter(Toilet.id == toilet_old.id).delete()

        if count1:
            # delete opening hours
            count2 = session.query(OpeningHours).filter(OpeningHours.toiletId == toilet_old.id).delete()
            # insert new record
            session.add(toilet)
            session.commit()
            return show_toilet(toilet, toilet.openingHours, session), 200
        else:
            # Toilet not found
            error_msg = "Toilet not found."
        return {"message": error_msg}, 404
    
    except IntegrityError as e:
        error_msg = Toilet.Toilet_Error(str(e.orig))
        return {"message": error_msg}, 409

    except Exception as e:
        # unexpected error
        print(e)
        error_msg = "Unexpected error."
        return {"message": error_msg}, 400


@app.get('/toilets', tags=[toilet_tag],
         responses={"200": ToiletsListSchema, "404": ErrorSchema})
def get_toilets():
    """ Get all toilets

    Returns a list of all toilets.
    """
    session = Session()
    toilets = session.query(Toilet).all()

    if not toilets:
        # there is no toilets
        return {"toilets": []}, 200
    else:
        # returns toilets list
        toilets_list = []
        for toilet in toilets: 
            openingHours = session.query(OpeningHours).filter(OpeningHours.toiletId == toilet.id).all()
            toilet.openingHours = openingHours
            toilets_list.append(toilet)
        return show_toilets(toilets_list, session), 200


@app.get('/toilet', tags=[toilet_tag],
         responses={"200": ToiletViewSchema, "404": ErrorSchema})
def get_toilet(query: ToiletSearchSchema):
    """ Get a toilet using latitude and longitude

    Returns toilet + opening hours
    """
    lat = query.lat
    long = query.long

    session = Session()
    # get the toilet
    toilet = session.query(Toilet).filter(Toilet.latitude == lat,
                                          Toilet.longitude == long).first()

    if not toilet:
        # if toilet not found
        error_msg = "Toilet not found."
        return {"message": error_msg}, 404
    else:
        openingHours = session.query(OpeningHours).filter(OpeningHours.toiletId == toilet.id).all()
        # returns toilet
        return show_toilet(toilet, openingHours, session), 200


@app.delete('/toilet', tags=[toilet_tag],
            responses={"200": ToiletDeleteSchema, "404": ErrorSchema})
def del_toilet(query: ToiletSearchSchema):
    """ Delete a toilet using latitude and longitude

    Returns delete confirmation
    """
    lat = query.lat
    long = query.long

    session = Session()
    # delete a toilet
    toilet = session.query(Toilet).filter(Toilet.latitude == lat,
                                          Toilet.longitude == long).first()
    if not toilet:
        # if toilet not found
        error_msg = "Toilet not found."
        return {"message": error_msg}, 404
    else:
        count1 = session.query(Toilet).filter(Toilet.id == toilet.id).delete()
        count2 = session.query(OpeningHours).filter(OpeningHours.toiletId == toilet.id).delete()
        session.commit()

    session.close()

    if count1:
        # returns delete confirmation
        return {"message": "Toilet has been deleted.", "id": toilet.id}
    else:
        # if toilet not found
        error_msg = "Toilet not found."
        return {"message": error_msg}, 404
