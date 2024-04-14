from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Time, UniqueConstraint, CheckConstraint
from datetime import datetime, time
from typing import Union

from  model import Base


class OpeningHours(Base):
    __tablename__ = 'openingHours'
    __table_args__ = (
        UniqueConstraint('toiletId', 'weekday', name='toilet_weekday'),
        CheckConstraint('weekday BETWEEN 0 AND 6', name='check_weekday'),
        CheckConstraint("openClosed IN ('O','C')", name='check_open_closed'),
        CheckConstraint("openingTime < closingTime", name='check_opening_closing'),
        CheckConstraint(
            "(openingTime IS NULL AND closingTime IS NULL) OR (openingTime IS NOT NULL AND closingTime IS NOT NULL)", 
            name='check_opening_closing_null'),
    )

    id = Column(Integer, primary_key=True)
    # Like weekday function: 0 for monday ... until 6 (sunday)
    weekday = Column(Integer)
    # (O)pen or (C)losed
    openClosed = Column(String(1))
    openingTime = Column(Time)
    closingTime = Column(Time)
    insertDate = Column(DateTime, default=datetime.now())

    # Relationship between Toilets and OpeningHours
    toiletId = Column(Integer, ForeignKey("toilet.pk_toilet"), nullable=False)

    def __init__(self, weekday:int, openClosed:str, 
                 openingTime:time, closingTime:time,
                 insertDate:Union[DateTime, None] = None):
        """
        Insert opening hours information of a Toilet

        Arguments:
            weekday: monday is 0, tuesday is 1... until sunday (6)
            open_closed: (O)pen or (C)losed - 1 char
            openingTime: time when a toilet opens.
            closingTime: time when a toilet closes.
            insertDate: insert date                         
        """
        self.weekday = weekday
        self.openClosed = openClosed
        self.openingTime = openingTime
        self.closingTime = closingTime
        
        if insertDate:
            self.insertDate = insertDate
