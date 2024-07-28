from database import Base,engine,SessionLocal
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from dto import UserRegistrationDto,LoginDto,LoginResponseDto
from models import User
import re
import json
from password_encrypt_decrypt import password_encrypt,password_decrypt

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/user/register")
def user_registration(user : UserRegistrationDto, database : db_dependency):
    user_obj = database.query(User).filter(user.email == User.email).first()
    if user_obj:
        raise HTTPException(status_code=400, detail="Email already exist")
    if not user.name:
        raise HTTPException(status_code=400, detail="Name should not be empty")
    if not user.email:
        raise HTTPException(status_code=400, detail="Email should not be empty")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password should not be empty")
    if not user.phone_number:
        raise HTTPException(status_code=400, detail="Phone number should not be empty")
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    password_regex = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,20}$'
    if not re.match(password_regex, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    phone_number_regex = r'^\+?[\d\s\-\(\)\.]{6,15}$'
    if not re.match(phone_number_regex, user.phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    encrypted_password = password_encrypt(user.password)

    user_details = User(name = user.name, email = user.email, password = encrypted_password, 
                        phone_number = user.phone_number)
    database.add(user_details)
    database.commit()
    result = {
        "status_code":201,
        "message":"User registered successfully"
    }
    return json.dumps(result)

@app.post("/user/login")
def user_login(login_user: LoginDto, database:db_dependency):
    user_obj = database.query(User).filter(login_user.email == User.email).first()
    if not user_obj:
        raise HTTPException(status_code=404,detail="Email not exist")

    decrypt_password = password_decrypt(login_user.password,user_obj.password.encode('utf-8'))
    if not decrypt_password:
        raise HTTPException(status_code=404,detail="Wrong password")
    
    login_response = LoginResponseDto(name=user_obj.name, email= user_obj.email,user_id=user_obj.user_id,
                                    role=user_obj.role,phone_number=user_obj.phone_number,
                                    registered_date=user_obj.registered_date)

    result = {
        "status_code":200,
        "response":{
            "user_id":login_response.user_id,
            "name":login_response.name,
            "email":login_response.email,
            "role":login_response.role,
            "phone_number":login_response.phone_number,
            "registered_date":login_response.registered_date.isoformat()
        }
    }

    return json.dumps(result)

