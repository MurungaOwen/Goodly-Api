from pydantic import BaseModel

class User(BaseModel):
    """user details gathered from webhook of clerk"""
    email: str
    donations_total: float

class Payment(BaseModel):
    """For storing payment data"""
    amount: int
    user_id: str
