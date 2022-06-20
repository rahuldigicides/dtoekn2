import json

# import requests
import os
import base64
import datetime
import random
import string
from pydantic import  BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pymysql 

# ! MY simple TOken 
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from fastapi import FastAPI,Depends,HTTPException,status, Security









# ! Database 
db_name="digisides"
db_user="root"
db_password=""
db_host="127.0.0.1"
db_port="3306"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/hello') 
def hello():
    return {"server":"uvicorn main:app --host 127.0.0.1 --port 8000"}


# ! Auth Handle File 
class AuthHandler():
    security = HTTPBearer()
   
    secret = 'SECRET'

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=60),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

auth_handler = AuthHandler()


@app.get('/check') 
async def checkToken(username=Depends(auth_handler.auth_wrapper)):
    return { "username":username ,"token":"this is token"}
