from pydantic import BaseModel

class User(BaseModel):
    """user details gathered from webhook of clerk"""
    email: str
    donations_total: float

class Payment(BaseModel):
    """For storing payment data"""
    amount: int
    user_id: str

class Message(BaseModel):
    """When someone is conacting us """
    firstname: str
    lastname: str
    subject: str
    contactinfo: str
    message: str
