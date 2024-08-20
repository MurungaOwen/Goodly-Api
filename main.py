from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.user import User, Message
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
@app.post('/webhooks/clerk/user')
async def clerk_webhook(payload: dict):
    """Handle Clerk webhook events"""
    event_type = payload.get('type')
    data = payload.get('data')
    
    new_user = None
    
    if event_type == 'user.created':
        if data and 'email_addresses' in data and len(data['email_addresses']) > 0:
            user_email = data['email_addresses'][0]['email_address']
            new_user = await register_user(user_email)
            print(f"Email is {user_email}")
        else:
            pass
    else:
        raise HTTPException(status_code=400, detail="Unsupported event type")
    
    return {"new_user_added": new_user}

from controllers.messageController import create_message
@app.post("/users/contact")
async def create_contactMessage(contactData: dict):
    # contact_data_json = contactData.model_dump()
    contact_data_json = contactData
    results = await create_message(contact_data_json)
    print(results)
    return {"success": "message_sent", "msgId": results}


    


