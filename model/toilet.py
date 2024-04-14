from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Toilet(Base):
    __tablename__ = 'toilet'
    __table_args__ = (
        UniqueConstraint('latitude', 'longitude', name='lat_long'),
        CheckConstraint('classification BETWEEN 1 AND 5', name='check_class'),
        CheckConstraint("toiletType IN ('Público','Pago')", name='check_toilet_type'),
    )

    id = Column("pk_toilet", Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    # Classification: int (from 1 to 5 stars)
    classification = Column(Integer)
    description = Column(String(150))
    # toilet type: 'Público' or 'Pago'
    toiletType = Column(String(10))
    user = Column(String(256))
    insertDate = Column(DateTime, default=datetime.now())

    # Relationship between Toilets and OpeningHours
    openingHours = relationship("OpeningHours")

    def __init__(self, latitude:float, longitude:float, 
                 classification:int, description:str, toiletType:str,
                 user:str,
                 insertDate:Union[DateTime, None] = None):
        """
        Insert a Toilet

        Arguments:
            latitude: latitude (used for positioning on a map)
            longitude: longitude (used for positioning on a map)
            classification: toilet classification, on a scale of 1 to 5 stars
            description: optional description of the toilet
            toiletType: toilet type ('Público' or 'Pago')
            user: email of the user who inserted the toilet
            insertDate: insert date of the toilet
        """
        self.latitude = latitude
        self.longitude = longitude
        self.classification = classification
        self.description = description
        self.toiletType = toiletType
        self.user = user

        # if not informed, it will be the current date
        if insertDate:
            self.insertDate = insertDate

    def Toilet_Error(error_type:str): 
        if error_type == "UNIQUE constraint failed: toilet.latitude, toilet.longitude":
            error_msg = "Toilet already exists in this location."
        elif error_type == "CHECK constraint failed: check_class":
            error_msg = "Classification must be a number from 1 to 5."
        elif error_type == "CHECK constraint failed: check_toilet_type":
            error_msg = "Toilet type must be 'Público' or 'Pago'."
        elif error_type == "CHECK constraint failed: check_weekday":
            error_msg = "Weekday must be a number from 0 to 6."
        elif error_type == "CHECK constraint failed: check_open_closed":
            error_msg = "Must be (O)pen or (C)losed."
        elif error_type == "CHECK constraint failed: check_opening_closing":
            error_msg = "Opening time must be less than closing time."
        elif error_type == "CHECK constraint failed: check_opening_closing_null":
            error_msg = "It is not allowed that only one of the times (opening and closing) is null."
        elif error_type == "UNIQUE constraint failed: OpeningHours.toilet_id, OpeningHours.weekday":
            error_msg = "Each toilet should only have one schedule for each day of the week."
        else:
            error_msg = "Unexpected error : " + error_type
        return error_msg

