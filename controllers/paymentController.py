import requests as rq
from decouple import config
import base64
from datetime import datetime

def get_access_token():
    # Get the consumer key and secret
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_SECRET')

    # Combine the key and secret and encode them in base64
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = rq.get(url, headers=headers)
    return response.json()["access_token"]


def stk_push(phone_number, amount):
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    business_short_code = config('MPESA_BUSINESS_SHORTCODE', default="174379")
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    
    # Password (Base64 encoded string of Shortcode + Passkey + Timestamp)
    data_to_encode = f"{business_short_code}{passkey}{timestamp}"
    password = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",  # or CustomerBuyGoodsOnline
        "Amount": amount,
        "PartyA": phone_number,  # The customer's phone number (in format 2547XXXXXXXX)
        "PartyB": business_short_code,  # The paybill number
        "PhoneNumber": phone_number,  # The same as PartyA
        "CallBackURL": "https://7bx7c5q0-8000.inc1.devtunnels.ms/mpesa",  # Update this with your callback URL
        "AccountReference": "TestAccount",  # Identifier for the transaction
        "TransactionDesc": "Payment for donation"  # Transaction description
    }

    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    response = rq.post(url, json=payload, headers=headers)
    return response.json()

print(stk_push("254114884211", 1))

