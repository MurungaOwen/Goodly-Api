from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.user import User
app = FastAPI()


origins = [
    "http://localhost:8080",
    "https://goodly.up.railway.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from controllers.userController import register_user
@app.post('/users')
async def create_user(user: User):
    """store user in db"""
    user_email = user.email
    user_id = register_user(user_email)
    return {"new_id": user_id}
    


