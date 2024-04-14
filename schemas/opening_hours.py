from typing import Union
from datetime import time
from pydantic import BaseModel as PydanticBaseModel, validator


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
    

class OpeningHoursSchema(BaseModel):
    """ Defines how a new OpeningHours to be inserted should be represented. 
    """
    weekday: int = 0
    openClosed: str = "O"
    openingTime: Union[None, time, str] = "10:00"
    closingTime: Union[None, time, str] = "22:00"

