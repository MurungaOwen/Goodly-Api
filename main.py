from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.user import User, Message
from datetime import datetime
app = FastAPI()


origins = [
    "http://localhost:8080",
    "https://goodly.up.railway.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


from controllers.paymentController import stk_push, store_donation_data
@app.post("/payment/mpesa/stk")
def pay_via_mpesa(payment_data: dict):
    amount = payment_data["amount"]
    phone_number = payment_data["phone_number"]
    try:
        result = stk_push(phone_number, amount)
        print("results is {}".format(result))
        if result.get("ResponseCode", "") == "0":
            return {"message": "Complete payment on phone"}
        return {"message": result.get('errorMessage').split("-")[1]}
    except Exception as e:
        return {"error": e}


@app.post("/mpesa")
async def process_payment_data(message: dict):
    data = message['Body']['stkCallback']['CallbackMetadata']['Item']
    amount = receipt_number = phone_number = None

    for item in data:
        if item['Name'] == 'Amount':
            amount = item['Value']
        elif item['Name'] == 'MpesaReceiptNumber':
            receipt_number = item['Value']
        elif item['Name'] == 'PhoneNumber':
            phone_number = item['Value']
        elif item['Name'] == 'TransactionDate':
            transaction_date = datetime.strptime(str(item['Value']), "%Y%m%d%H%M%S")
    transaction_details = {
        "amount": amount,
        "receipt_number": receipt_number,
        "phone_number": phone_number,
        "transaction_date": transaction_date
    }
    try:
        results = await store_donation_data(transaction_details)
        return {"success": results}
    except Exception as e:
        return {"error": e}


    
 

