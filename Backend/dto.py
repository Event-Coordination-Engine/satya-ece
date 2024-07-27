from pydantic import BaseModel
from datetime import datetime

class UserRegistrationDto(BaseModel):
    name : str
    email :str
    phone_number : str
    password :str

class LoginDto(BaseModel):
    email:str
    password:str

class LoginResponseDto(BaseModel):
    user_id :int
    name : str
    email : str
    phone_number :str
    role:str
    registered_date:datetime

