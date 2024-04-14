from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Shows a message error
    """
    message: str
