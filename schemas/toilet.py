from typing import Optional, List, Union
from model import Session, Toilet, OpeningHours
from datetime import time
from pydantic import BaseModel as PydanticBaseModel, validator
from schemas.opening_hours import OpeningHoursSchema


class BaseModel(PydanticBaseModel):
    """ Helper function that transforms empty strings into None.
    """
    class Config:
        orm_mode = True

    @validator('*')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v
    

class ToiletSchema(BaseModel):
    """ Defines how a new Toilet to be inserted should be represented. 
    """
    latitude: float = -23.003171
    longitude: float = -43.321731
    classification: int = 5
    description: Optional[str] = "Banheiro no Shopping Città América"
    toiletType: str = "Público"
    user: str = "xxxxx@xxxxxx.com"
    openingHours: List[OpeningHoursSchema] = [ 
        '{"weekday":0,"openClosed":"O","openingTime":"10:00:00","closingTime":"22:00:00"}',
        '{"weekday":1,"openClosed":"O","openingTime":"10:00:00","closingTime":"22:00:00"}',
        '{"weekday":2,"openClosed":"O","openingTime":"10:00:00","closingTime":"22:00:00"}',
        '{"weekday":3,"openClosed":"O","openingTime":"10:00:00","closingTime":"22:00:00"}',
        '{"weekday":4,"openClosed":"O","openingTime":"10:00:00","closingTime":"22:00:00"}',
        '{"weekday":5,"openClosed":"C","openingTime":null,"closingTime":null}',
        '{"weekday":6,"openClosed":"C","openingTime":null,"closingTime":null}'
          ]


class ToiletSearchSchema(BaseModel):
    """ Defines how the search will be done.
    """
    lat: float = -23.003171
    long: float = -43.321731


class ToiletsListSchema(BaseModel):
    """ Defines how a Toilets List will be presented.
    """
    toilets:List[ToiletSchema]

def show_toilets(toilets: List[Toilet], session: Session):
    """ Returns a List of Toilets, using ToiletViewSchema.
    """
    result = []
    for toilet in toilets:
        result.append(show_toilet(toilet, toilet.openingHours, session))
    
    session.close()

    return {"toilets": result}


class ToiletViewSchema(BaseModel):
    """ Defines how a Toilet will be showed: toilet + opening hours
    """
    id: int = 1
    latitude: float = -23.003171
    longitude: float = -43.321731
    classification: int = 5
    description: Optional[str] = "Banheiro no Shopping Città América"
    toiletType: str = "Público"
    user: str = "xxxxx@xxxxxx.com"
    openingHours: List[OpeningHoursSchema] = []


class ToiletDeleteSchema(BaseModel):
    """ Defines information to delete a toilet 
    """
    message: str
    latitude: float
    longitude: float 

def show_toilet(toilet: Toilet, openingHours: List[OpeningHours], session: Session):
    """ Shows Toilet using ToiletViewSchema
    """
    result = [{
        "id": toilet.id,
        "latitude": toilet.latitude,
        "longitude": toilet.longitude,
        "classification": toilet.classification,
        "description": toilet.description,
        "toiletType": toilet.toiletType,
        "user": toilet.user
    }]
    openingHoursList = []
    for openingHour in openingHours:
        if isinstance(openingHour.openingTime, time):
           openingHour.openingTime = openingHour.openingTime.isoformat()

        if isinstance(openingHour.closingTime, time):
           openingHour.closingTime = openingHour.closingTime.isoformat()

        openingHoursList.append({
            "id": openingHour.id,
            "weekday": openingHour.weekday,
            "openClosed": openingHour.openClosed,
            "openingTime": openingHour.openingTime,
            "closingTime": openingHour.closingTime,
        })

    result.append({"openingHours": openingHoursList})
    session.close()
    return {"toilet": result}

